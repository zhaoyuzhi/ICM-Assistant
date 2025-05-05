import json
import cv2

from tqdm import tqdm
f = open('./llava_r1.json', 'r', encoding='utf-8')
j = json.load(f)
qa_list = []
file_list = []

for d in tqdm(j):
    try:
        question = d["conversations"][0]["value"].replace('<image>\n', '').replace('\n<image>', '')
        answer = d["conversations"][1]["value"]
        img_json = {}
        img_json["messages"] = [
            {
                "role": "user",
                "content": "<image>" + question
            },
            {
                "role": "assistant",
                "content": answer
            },

        ]
        img_json["images"] = d["image"]
        # img_json["id"] = d["id"]
        # img_json["image"] =
        # im = cv2.imread('/home/lxe5wipa/lxe5wipauser09/dataset/icm/data/' + d["image"])
        # h, w, c = im.shape
        # img_json["width"] = w
        # img_json["height"] = h
        # print('height: ', h)
        qa_list.append(img_json)
    except:
        print('reading error')
        break
print(len(qa_list))

with open('swift_baseline.json', 'a') as fp:
    json.dump(qa_list, fp, indent=4)
