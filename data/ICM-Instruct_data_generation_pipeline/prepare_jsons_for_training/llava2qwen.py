import json

f = open('./llava_baseline.json', 'r', encoding='utf-8')
j = json.load(f)
qa_list = []
file_list = []

for d in j:
    question = d["conversations"][0]["value"].replace('<image>\n', '').replace('\n<image>', '')
    answer = d["conversations"][1]["value"]
    img_json = {}
    img_json["conversations"] = [
        {
            "from": "user",
            "value": "Picture 1: <img>" + img_base_path + "</img>\n" + question
        },
        {
            "from": "assistant",
            "value": answer
        }
    ]
    img_json["id"] = d["id"]
    img_json["image"] = d["image"]
    qa_list.append(img_json)
print(len(qa_list))

with open('qwen_baseline.json', 'a') as fp:
    json.dump(qa_list, fp, indent=4)