from tqdm import tqdm
import os
import time
import datasets
from io import BytesIO
from openai import OpenAI
import base64
from dotenv import load_dotenv
import argparse

load_dotenv()

def generate(model, prompt, images):
    content = [{"type": "text", "text": prompt}] + [{"type": "image_url", "image_url": {"url": image}} for image in images]
    chat_response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": content,
        }],
        max_completion_tokens= 8192,
    )
    result = chat_response.choices[0].message.content

    return result

def convert_to_str(img):
    if img is not None:
        buf = BytesIO()
        img.save(buf, format='PNG')  # or use img.format if you want to preserve original format
        img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    else:
        img_str = None
    return img_str


client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
)

def main():
    parser = argparse.ArgumentParser(description="Run model response generation script.")
    parser.add_argument('--model', type=str, required=True, help='Model name to use for response generation')
    args = parser.parse_args()

    MODEL = args.model

    ds = datasets.load_dataset("ReliableAI/IRLBench")

    for EXAM_ID in ['LC003ALP100EV_problems', 'LC003ALP100IV_problems', 'LC021ALP000EV_problems','LC021ALP000IV_problems','LC022ALP000EV_problems','LC022ALP000IV_problems','LC023ALP000EV_problems','LC023ALP000IV_problems','LC219ALP038EV_problems',"LC219ALP038IV_problems","LC065ALP000EV_problems","LC065ALP000IV_problems", "LC033ALP032EV_problems","LC033ALP032IV_problems",'LC032ALP000EV_problems','LC032ALP000IV_problems','LC034ALP000EV_problems','LC034ALP000IV_problems','LC014ALP000EV_problems','LC014ALP000IV_problems','LC568ALP000EV_problems','LC568ALP000IV_problems','LC004ALP000EV_problems','LC004ALP000IV_problems']:
        df = ds[EXAM_ID].to_pandas()
        for index, row in tqdm(enumerate(ds[EXAM_ID])):
            prompt = row['problem']
            prompt += '''
Your response should be in the following format:
Answer: {your answer to the above problem}
Confidence: {your confidence score between 0% and 100% for your answer}'''
            my_files = []
            if row['problem_image_1']:
                image_base64 = convert_to_str(row['problem_image_1'])
                my_files.append(f"data:image/png;base64,{image_base64}")

            if row['problem_image_2']:
                image_base64 = convert_to_str(row['problem_image_2'])
                my_files.append(f"data:image/png;base64,{image_base64}")

            trial_count = 3
            while trial_count > 0:
                trial_count -= 1
                try:
                    response_text = generate(MODEL, prompt, my_files)
                except Exception as e:
                    print('Error occurred: ', e)
                    time.sleep(5)
                    continue

                if response_text:
                    df.at[index, 'response'] = response_text
                    print(response_text)
                    break
            else:
                print('Failed to get response after 3 trials, skipping...')
                df.at[index, 'response'] = 'Error: Failed to get response'

            df.to_csv(f'responses/{EXAM_ID}_{MODEL.replace("/", "--")}.csv', index=False)

if __name__ == "__main__":
    main()
