from google import genai
import time
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

# id_pairs = [[4, 12], [12, 19], [19, 26], [26, 33]] # for LC003ALP100EV
# id_pairs = [[4, 12], [12, 19], [19, 26], [26, 30]] # for LC003ALP200EV
# id_pairs = [[6, 13], [13, 20]] # for LC022ALP000EV, LC022ALP000IV
# id_pairs = [[5, 13], [13, 22], [22, 33]] # for LC023ALP000EV
# id_pairs = [[6, 14], [14, 23], [23, 35]] # for LC023ALP000IV
# id_pairs = [[6, 13], [13, 23]] # for LC021ALP000EV
# id_pairs = [[6, 15], [15, 23]] # for LC021ALP000IV

# exam_names = ['LC022ALP000EV', 'LC022ALP000IV', 'LC023ALP000EV', 'LC023ALP000IV', 'LC021ALP000EV', 'LC021ALP000IV']
# exam_id_pairs = [[[6, 13], [13, 20]], [[6, 13], [13, 20]], [[5, 13], [13, 22], [22, 33]], [[6, 14], [14, 23], [23, 35]], [[6, 13], [13, 23]], [[2, 10], [10, 17]]]
# exam_names = ['LC021ALP000EV', 'LC021ALP000IV']
# exam_id_pairs = [[[6, 13], [13, 23]], [[2, 10], [10, 17]]]
# exam_names = ['LC219ALP038EV']
# marking_scheme_names = ['LC219ALP000EV']
# exam_names = ['LC219ALP038IV']
# marking_scheme_names = ['LC219ALP000IV']
# exam_id_pairs = [[[3, 7], [7, 10], [11, 15], [15, 21], [28, 33]]]
# marking_scheme_id_pairs = [[[4, 9], [9, 12], [12, 17], [17, 25], [25, 32]]]

# exam_names = ['LC033ALP032EV']
# marking_scheme_names = ['LC033ALP000EV']
# # exam_id_pairs = [[[3, 8], [42, 43], [43, 45], [45, 47], [47, 49], [49, 51]]]
# # marking_scheme_id_pairs = [[[14, 23], [23, 31], [31, 38], [38, 46], [46, 53], [53, 59]]]
# exam_id_pairs = [[[3, 6], [6, 8]]]
# marking_scheme_id_pairs = [[[14, 20], [19, 23]]]

# exam_names = ['LC032ALP000EV', 'LC032ALP000IV', 'LC034ALP000EV', 'LC034ALP000IV']
# marking_scheme_names = ['LC032ALP000EV_ms', 'LC032ALP000IV_ms', 'LC034ALP000EV_ms', 'LC034ALP000IV_ms']
# exam_id_pairs = [[[2, 4], [4, 6], [6, 8], [8, 10], [10, 11], [12, 14], [14, 16], [16, 18], [18, 19], [19, 20]], 
#                  [[2, 4], [4, 6], [6, 8], [8, 10], [10, 11], [12, 14], [14, 16], [16, 18], [18, 19], [19, 20]],
#                  [[3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 17], [17, 21], [21, 25], [25, 29], [29, 33], [33, 37]],
#                  [[3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 17], [17, 21], [21, 25], [25, 29], [29, 33], [33, 37]]]
# marking_scheme_id_pairs = [[[3, 6], [6, 10], [10, 13], [13, 16], [16, 18], [18, 22], [22, 25], [25, 28], [28, 31], [31, 34]], 
#                            [[3, 6], [6, 10], [10, 13], [13, 16], [16, 18], [18, 22], [22, 25], [25, 28], [28, 31], [31, 34]],
#                            [[5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14], [14, 15], [16, 21], [21, 27], [27, 34], [34, 38], [38, 43], [43, 48]],
#                            [[5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14], [14, 15], [16, 21], [21, 27], [27, 34], [34, 38], [38, 43], [43, 48]]]

# exam_names = ['LC034ALP000EV', 'LC034ALP000IV', 'LC014ALP000EV', 'LC014ALP000IV']
# marking_scheme_names = ['LC034ALP000EV_ms', 'LC034ALP000IV_ms', 'LC014ALP000EV_ms', 'LC014ALP000IV_ms']
# exam_id_pairs = [[[3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 17], [17, 21], [21, 25], [25, 29], [29, 33], [33, 37]],
#                  [[3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 17], [17, 21], [21, 25], [25, 29], [29, 33], [33, 37]],
#                  [[3, 6], [6, 10], [11, 12], [17, 18]],
#                  [[3, 6], [6, 10], [11, 12], [17, 18]],]
# marking_scheme_id_pairs = [[[5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14], [14, 15], [16, 21], [21, 27], [27, 34], [34, 38], [38, 43], [43, 48]],
#                            [[5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14], [14, 15], [16, 21], [21, 27], [27, 34], [34, 38], [38, 43], [43, 48]],
#                            [[18, 19], [19, 21], [21, 26]], 
#                            [[18, 19], [19, 21], [21, 26]], ]

exam_names = ['LC568ALP000EV', 'LC568ALP000IV', 'LC004ALP000EV', 'LC004ALP000IV', 'LC014ALP000EV', 'LC014ALP000IV']
marking_scheme_names = ['LC568ALP000EV_ms', 'LC568ALP000IV_ms', 'LC004ALP000EV_ms', 'LC004ALP000IV_ms', 'LC014ALP000EV_ms', 'LC014ALP000IV_ms']
exam_id_pairs = [[[3, 5], [5, 8], [8, 13], [14, 16]],
                 [[3, 5], [5, 8], [8, 13], [14, 16]],
                 [[2, 4], [4, 6], [6, 8]],
                 [[2, 4], [4, 6], [6, 8]],
                 [[3, 6], [6, 10], [11, 12], [17, 18]],
                 [[3, 6], [6, 10], [11, 12], [17, 18]],]
marking_scheme_id_pairs  = [[[4, 6], [5, 9], [9, 11], [11, 14]],
                            [[4, 6], [5, 9], [9, 11], [11, 14]],
                            [[9, 14], [14, 18], [14, 20]],
                            [[9, 14], [14, 18], [14, 20]],
                            [[18, 19], [19, 21], [21, 26]], 
                            [[18, 19], [19, 21], [21, 26]], ]

exam_names = ['LC034ALP000EV']
marking_scheme_names = ['LC034ALP000EV_ms']
exam_id_pairs = [[[33, 35], [35, 37]]]
marking_scheme_id_pairs = [[[43, 46], [45, 48]]]

for EXAM_NAME, MS_NAME, id_pairs, ms_id_pairs in zip(exam_names, marking_scheme_names, exam_id_pairs, marking_scheme_id_pairs):
    # time.sleep(3)
    problems = ''

    for id_pair, ms_id_pair in zip(id_pairs, ms_id_pairs):
        my_files = []
        for i in range(id_pair[0], id_pair[1]):
            ## format to 2 digits:
            number = str(i).zfill(2)
            my_file = client.files.upload(file=f"exam_images/{EXAM_NAME}/{EXAM_NAME}_page-00{number}.jpg")
            my_files.append(my_file)

        for i in range(ms_id_pair[0], ms_id_pair[1]):
            ## format to 2 digits:
            number = str(i).zfill(2)
            my_file = client.files.upload(file=f"exam_images/{MS_NAME}/{MS_NAME}_page-00{number}.jpg")
            my_files.append(my_file)

        prompt = '''I will give you an exam paper and the corresponding marking scheme from the official Leaving Certificate Exam of Ireland, containing several problems written in either English or Irish. They are extracted from PDF files as images.
Your task is to extract each problem and the corresponding marking scheme/answer.

Here are some guidelines you should follow
- For each problem found, use the following format:
Problem 1: <problem statement>
Answer 1: <answer to problem 1>

Problem 2: <problem statement>
Answer 2: <answer to problem 2>

...

- For each problem you identify, make sure to keep the original content, including the equations in LaTeX. Remove any redundant context, personal commentary, anecdotes, or unrelated information. But make sure not to change the meaning of the problem and keep all necessary mathematical or technical details.
- For each problem you identify, find the corresponding marking scheme/answer based on question number/part.
- If multiple problems that you extract are related, make sure to include all the context in each problem statement as they will be looked at independently.

Here are a few examples.


Example 1

Marking scheme:
Question 1: A sample of Ra–224 decays to form Pb–208, an isotope of lead. 
(a) How many alpha-particles are released?
4 
(b) How many beta-particles are released? 
2 

Output:
Problem 1: A sample of Ra–224 decays to form Pb–208, an isotope of lead. 
How many alpha-particles are released?
Answer 1: 4

Problem 2: A sample of Ra–224 decays to form Pb–208, an isotope of lead. 
How many beta-particles are released? 
Answer 2: 2

Example 2

Marking scheme:
Question 1: A spectrometer can be used to measure the wavelength of light.
(i) Identify a different colour of light that could be used to produce a greater angle of 
separation.
red / orange / yellow
(ii) Explain how the number of lines per mm on a diffraction grating affects the angle of 
separation. 
increased number of lines per mm means increased angle

Question 2: All matter and energy in the universe must abide by one or more of the four fundamental forces of nature.
(i) Which force is the weakest of the four forces? 
gravitational force
(ii) Which force is responsible for binding the nucleus?
strong force

Output:
Problem 1: A spectrometer can be used to measure the wavelength of light.
Identify a different colour of light that could be used to produce a greater angle of 
separation.
Answer 1: red / orange / yellow

Problem 2: A spectrometer can be used to measure the wavelength of light.
Explain how the number of lines per mm on a diffraction grating affects the angle of 
separation.
Answer 2: increased number of lines per mm means increased angle

Problem 3: All matter and energy in the universe must abide by one or more of the four fundamental forces of nature.
Which force is the weakest of the four forces? 
gravitational force
Answer 3: gravitational force

Problem 4: All matter and energy in the universe must abide by one or more of the four fundamental forces of nature.
Which force is responsible for binding the nucleus?
Answer 4: strong force


Please analyze the following exam and extract all math problems. Here are the guidelines one more time for your reference
- For each problem found, use the following format:
Problem 1: <problem statement>
Answer 1: <answer to problem 1>

Problem 2: <problem statement>
Answer 2: <answer to problem 2>

...

- For each problem you identify, make sure to keep the original content, including the equations in LaTeX. Remove any redundant context, personal commentary, anecdotes, or unrelated information. But make sure not to change the meaning of the problem and keep all necessary mathematical or technical details.
- For each problem you identify, find the corresponding marking scheme/answer based on question number/part.
- If multiple problems that you extract are related, make sure to include all the context in each problem statement as they will be looked at independently.

Output:'''

        trial_count = 3
        while trial_count > 0:
            trial_count -= 1
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=my_files + [prompt],
                )
            except Exception as e:
                print('Error occurred, retrying...: ', e)
                time.sleep(5)
                continue

            if response.text:
                problems += response.text + '\n'
                print(response.text)
                break
            else:
                print('Empty response, retrying...')
                time.sleep(5)

    with open(f'results/{EXAM_NAME}_problems.txt', 'w') as f:
        f.write(problems)
