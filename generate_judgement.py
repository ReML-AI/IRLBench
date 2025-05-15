from google import genai
from openai import OpenAI
from pydantic import BaseModel
import pandas as pd
import os
import time
from dotenv import load_dotenv
import base64
import ast
import argparse

load_dotenv()

TEMPLATE_PROMPT = '''Judge whether the following [response] to [question] is correct or not based on the suggested marking scheme [marking_scheme] below.

[question]: {question} (also in attached images)

[response]: {response}

[marking_scheme]: {marking_scheme} (also in attached images)

Your judgement must be in the format and criteria specified below:

[extracted_final_answer]: The final exact answer extracted from the [response]. Put the extracted answer as ’None’ if there is no exact, final answer to extract from the response.

[reasoning]: Explain why the extracted_final_answer is correct or incorrect based on [marking_scheme], focusing only on if the extracted_final_answer follows the [marking_scheme]. Do not comment on any background to the problem, do not attempt to solve the problem.

[correct]: Answer ’yes’ if extracted_final_answer follows perfectly the [marking_scheme] given above, or is within a small margin of error for numerical problems. Answer ’no’ otherwise, i.e. if there if there is any inconsistency, ambiguity, non-equivalency, or if the extracted answer is incorrect.

[confidence]: The extracted confidence score between 0% and 100% from [response]. Put 100 if there is no confidence score available.'''

class Judgement(BaseModel):
    extracted_final_answer: str
    reasoning: str
    correct: str
    confidence: str


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


gemini_client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
openai_client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
)

def generate(model, prompt, image_files, config):
    if model in ['gemini-2.0-flash', 'gemini-2.5-flash-preview-04-17']:
        my_files = []
        for file in image_files:
            my_files.append(genai.types.Part.from_bytes(
                data=file,
                mime_type='image/png',
            ))
        response = gemini_client.models.generate_content(
            model=model,
            contents=my_files + [prompt],
            config=config,
        )
        return response.text
    elif model == 'o4-mini-2025-04-16':
        my_files = []
        for file in image_files:
            my_files.append(encode_image(file))
        response = openai_client.responses.parse(
            model=model,
            reasoning={"effort": "medium"},
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                    ] +
                    [
                        {
                            "type": "input_image",
                            "image_url": f"data:image/png;base64,{base64_image}",
                        }
                        for base64_image in my_files
                    ],
                }
            ],
            max_output_tokens=25_000,
            text_format=Judgement,
        )
        return response.output_parsed.model_dump_json()


def main():
    parser = argparse.ArgumentParser(description="Run model judgement script.")
    parser.add_argument('--judge_model', type=str, required=True, help='Judge model name')
    parser.add_argument('--student_model', type=str, required=True, help='Student model name')
    args = parser.parse_args()

    JUDGE_MODEL = args.judge_model
    STUDENT_MODEL = args.student_model

    for EXAM_ID in ['LC003ALP100EV_problems', 'LC003ALP100IV_problems', 'LC021ALP000EV_problems','LC021ALP000IV_problems','LC022ALP000EV_problems','LC022ALP000IV_problems','LC023ALP000EV_problems','LC023ALP000IV_problems','LC219ALP038EV_problems',"LC219ALP038IV_problems","LC065ALP000EV_problems","LC065ALP000IV_problems", "LC033ALP032EV_problems","LC033ALP032IV_problems",'LC032ALP000EV_problems','LC032ALP000IV_problems','LC034ALP000EV_problems','LC034ALP000IV_problems','LC014ALP000EV_problems','LC014ALP000IV_problems','LC568ALP000EV_problems','LC568ALP000IV_problems','LC004ALP000EV_problems','LC004ALP000IV_problems']:
        FILE_NAME = f'responses/{EXAM_ID}_{STUDENT_MODEL}.csv'
        df = pd.read_csv(FILE_NAME)

        for index, row in df.iterrows():
            my_files = []
            if 'problem_image_1' in row.keys() and row['problem_image_1'] and not pd.isna(row['problem_image_1']):
                my_files.append(ast.literal_eval(row['problem_image_1'])['bytes'])

            if 'problem_image_2' in row.keys() and row['problem_image_2'] and not pd.isna(row['problem_image_2']):
                my_files.append(ast.literal_eval(row['problem_image_2'])['bytes'])

            if 'answer_image_1' in row.keys() and row['answer_image_1'] and not pd.isna(row['answer_image_1']):
                my_files.append(ast.literal_eval(row['answer_image_1'])['bytes'])

            if STUDENT_MODEL == 'DeepSeek-R1-Distill-Llama-70B' and len(my_files) > 0:
                df.at[index, 'judgement'] = 'Skipped: DeepSeek-R1-Distill-Llama-70B does not support image files'
                continue

            current_prompt = TEMPLATE_PROMPT.format(
                question=row['problem'],
                response=row['response'],
                marking_scheme=row['answer']
            )

            trial_count = 3
            while trial_count > 0:
                trial_count -= 1
                try:
                    response_text = generate(JUDGE_MODEL, 
                                            current_prompt, 
                                            my_files, 
                                            {
                                                'response_mime_type': 'application/json',
                                                'response_schema': Judgement,
                                            })
                except Exception as e:
                    print('Error occurred, retrying...: ', e)
                    time.sleep(5)
                    continue

                if response_text:
                    df.at[index, 'judgement'] = response_text
                    print(response_text)
                    break
            else:
                print('Failed to get response after 3 trials, skipping...')
                df.at[index, 'judgement'] = 'Error: Failed to get judgement'

        df.to_csv(f'judgements/{EXAM_ID}_{STUDENT_MODEL}_judge_model_{JUDGE_MODEL}.csv', index=False)

if __name__ == "__main__":
    main()
