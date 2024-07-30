print("\033[92mSetting up tagging environment...\033[0m")

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from transformers import pipeline
import re

from time import sleep

filename = '../youtube-scraper/out/raw-4.csv'
model = 'deepset/bert-base-german-cased-hatespeech-GermEval18Coarse'
content = []
with open(filename, "r") as file_content:
    for line in file_content.readlines():
        line = re.sub('[\s]+', ' ', line)
        if not re.search('[a-zA-Z]', line) or len(line) < 10:
            continue
        line = line.strip()
        content.append(line)

pipe = pipeline("text-classification", model=model)

string_to_file = ''
total_lines = len(content)
processed_count = 0

print(f"\033[92mDone! Using the model: '{model}'\033[0m")
sleep(2)

for index, line in enumerate(content):
    try:
        out = pipe(line)
        label = out[0]['label']
        score = out[0]['score']

        if label == 'OFFENSE':
            print(f"\033[91m[{int(((index + 1) / total_lines) * 100)}%]\033[0m \033[33mTagged comment {index + 1}/{total_lines}\033[0m - \033[32m{label}\033[0m {score} {line}")
        elif label == 'OTHER':
            print(f"\033[91m[{int(((index + 1) / total_lines) * 100)}%]\033[0m \033[33mTagged comment {index + 1}/{total_lines}\033[0m - \033[36m{label}\033[0m {score} {line}")
        else:
            print(f"\033[91m[{int(((index + 1) / total_lines) * 100)}%]\033[0m \033[33mTagged comment {index + 1}/{total_lines} - {label} {score} {line}")

        string_to_file += f"{label}\t{score}\t{line}\n"
        processed_count += 1
    except Exception as e:
        print(f"Error processing line {index + 1}: {line}. Error: {str(e)}")
        continue

output_filename = 'out/hate-speech.csv'
with open(output_filename, 'w') as writefile:
    writefile.write(string_to_file.strip())

print(f"\033[92mTagging process completed: Results saved to '{output_filename}'.\033[0m")
sleep(2)