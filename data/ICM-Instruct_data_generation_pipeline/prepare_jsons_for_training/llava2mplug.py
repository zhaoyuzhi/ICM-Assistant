import json

f = open('./llava_baseline.json', 'r', encoding='utf-8')
j = json.load(f)
qa_list = []
file_list = []

for d in j:
    question = d["conversations"][0]["value"].replace('<image>\n', '').replace('\n<image>', '')
    answer = d["conversations"][1]["value"]
    img_json = {}
    img_json["id"] = d["id"]
    img_json["image"] = d["image"]
    img_json["conversations"] = [
        {
            "from": "human",
            "value": question + "\n<|image|>"
        },
        {
            "from": "gpt",
            "value": answer
        }
    ]
    qa_list.append(img_json)
print(len(qa_list))

with open('mplug_baseline.json', 'a') as fp:
    json.dump(qa_list, fp, indent=4)