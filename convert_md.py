import argparse
import os
import json
from uuid import uuid4
from re import search
#added script arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="path to the md file")
ap.add_argument("-o", "--output", required=True, help="path to the json processed file")
ap.add_argument("-t", "--topic", required=True, help="topic of the questions")
args = vars(ap.parse_args())

md_file = os.path.sep.join([args["input"]])
out_file = os.path.sep.join([args["output"]])
topic = args["topic"]

text = None
with open(md_file, 'r') as f:
    text = f.read()

#print(text)

lines = text.strip().split("\n")

output_json = []
line_fields = ["question", "topic", "choices", "id", "complexity"]
answer_fields = ["content", "isCorrect", "id"]

for line in lines:
    line_dict = dict()
    values = line.strip().split(":")
    if "|" not in line:
        line_dict[line_fields[0]] = values[1]
        line_dict[line_fields[1]] = str(topic)
        line_dict[line_fields[3]] = str(uuid4())
        output_json.append(line_dict)
    else:
        answer_list = []
        answers = values[1].strip().split("|")
        print(answers)
        for ans in answers:
            answer_dict = dict()
            print(ans)
            isCorrect = False
            if search("yes", ans):
                isCorrect = True
                ans = ans.replace("yes", "", 1)
                answer_dict[answer_fields[0]] = ans.strip()
            else:
                answer_dict[answer_fields[0]] = ans.strip()
            answer_dict[answer_fields[1]] = isCorrect
            answer_dict[answer_fields[2]] = str(uuid4())
            answer_list.append(answer_dict)

        line_dict[line_fields[2]] = answer_list
        temp = output_json[-1]
        temp.update(line_dict)
        output_json[-1] = temp
    
    
with open(out_file,'w') as f:
    json.dump(output_json,f,indent=4)

            


