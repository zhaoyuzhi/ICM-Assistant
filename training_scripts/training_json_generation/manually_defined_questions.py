
from utils import text_readlines, text_save, get_class, check_path
import random
import json

questions = [
    '图中的人物符合了\"性感裸露\"定义吗?请回答是或否, 并解释原因.',
    '这个人物是否符合\"性感裸露\"定义?请回答是或者否，并说出原因',
    '图中人物符合了\"性感裸露\"定义吗?请回答是或否，并给出理由',
    '这个人物是否符合\"性感裸露\"定义?请确认或者反对，并解释',
    '这个人物是否符合\"性感裸露\"定义?请回答是或者否，并说出原因',
    '图中人物符合\"性感裸露\"定义吗?请回答是或否, 并解释原因.',
    '图中的人物符合\"性感裸露\"定义吗?请确认或者反对，并解释',
    '这个人物是否符合了\"性感裸露\"定义?请回答是或者否，并说出原因',
    '图中人物符合了\"性感裸露\"定义吗?请回答是或否, 并解释原因.',
    '这个人物是否符合了\"性感裸露\"定义?请回答是或否, 并解释原因.'
]
questions_en = [
    'Does the person in the image violate the "sexually suggestive" definition? Please answer yes or no and explain why.',
    'Is the person in the image depicted in a sexually explicit or suggestive manner? Please answer yes or no and explain why.',
    'Does the image contain any sexually suggestive content, including the person\'s pose, facial expression, or clothing? Please answer yes or no and explain why.',
    'Is the person in the image engaging in any sexually suggestive behavior or activity? Please answer yes or no and explain why.',
    'Does the image have any sexually implicit or explicit connotations? Please answer yes or no and explain why.',
    'Is the person in the image depicted in a way that could be considered sexually attractive or appealing? Please answer yes or no and explain why.',
    'Does the image contain any elements that could be considered sexually inappropriate or offensive? Please answer yes or no and explain why.',
]
mapping = {
    'baby': '图中的婴儿只穿着内裤, 裸露了除私处之外的皮肤',
    'lower_hips': '图中的人物穿着紧身裤或瑜伽裤, 刻意地突出臀部',
    'lower_large_bare': '图中的人物下半身穿着内裤, 裸露整双腿, 上半身穿着内衣, 裸露腰部',
    'lower_leg': '图中展示了人物的下半身, 人物裸露了大腿根到脚踝的部分',
    'lower_normal': '图中展示了人物的下半身, 人物的裸露部分只限于膝盖以下到脚踝的部分, 这不是一张裸露图像',
    'lower_shoulders_and_belly': '这是一张下半身图像，图中的人物裸露了肚子, 露出了肚脐眼',
    'male_sexy': '图中的男性上半身没有穿衣服',
    'middle_crotch': '图中展示了人物的裆部特写, 人物只穿了内裤, 其余的皮肤都裸露在外',
    'middle_hips': '图中展示了人物的臀部特写, 人物刻意地翘屁股',
    'middle_leg': '图中展示了人物的下半身, 人物穿着的裤子很短, 裸露了大腿根部',
    'middle_normal': '图中展示了人物的髋部附近, 人物没有露出大腿根部, 也没有肚脐眼, 也没有刻意展示臀部, 这不是一张裸露图像',
    'middle_shoulders_and_belly': '这是一张人物髋部图像，图中的人物裸露了肚子, 露出了肚脐眼',
    'no_person': '图中不包含人物, 不存在人物性感裸露的问题',
    'sexy_kiss': '图中展示了人们亲吻的场景, 这涉及到了性感氛围',
    'stockings': '图中的女性穿着丝袜, 这涉及到了性感元素',
    'upper_backless': '图中展示了人物的上半身背部, 可见人物的背部皮肤有一半以上裸露在外',
    'upper_bust': '图中展示了女性的胸部特写, 露出了乳沟',
    'upper_large_bare': '图中的人物穿着内衣, 上半身皮肤有一半以上裸露在外, 且露出了肚脐眼',
    'upper_normal': '图中的人物只有小部分(小于一半)皮肤露出, 这不是一张裸露图像',
    'upper_shoulders_and_belly': '这是一张上半身图像，图中的人物裸露了肚子, 且露出了肚脐眼',
    'upper_small_bare': '图中展示了人物的上半身, 人物露出了双肩和整个手臂',
    'whole_backless': '图中展示了人物的全身照, 人物的背部皮肤有一半以上裸露在外',
    'whole_large_bare': '图中展示了人物的全身照, 人物的皮肤有一半以上裸露在外',
    'whole_leg': '图中展示了人物的全身照, 上半身没有裸露, 但下半身裸露了大腿根到脚踝的部分',
    'whole_normal': '图中的人物没有大面积裸露, 且没有露出关键部位',
    'whole_shoulders_and_belly': '这是一张全身图像，图中的人物裸露了肚子, 且露出了肚脐眼',
    'whole_small_bare': '图中的人物有小面积裸露'
}
all_body_positions = ['肩部', '胸部', '背部', '腹部肚脐', '裆部', '臀部', '腿部', '无']
all_body_positions_en = ['shoulder', 'breast', 'back', 'belly', 'crotch', 'hips', 'legs', 'None']
mapping_body = {
    'baby': ['肩部', '胸部', '背部', '腹部肚脐'],
    'lower_hips': ['臀部', '腿部'],
    'lower_large_bare': ['臀部', '腿部'],
    'lower_leg': ['腿部'],
    'lower_normal': ['无'],
    'lower_shoulders_and_belly': ['腹部肚脐', '腿部'],
    'male_sexy': ['肩部', '胸部', '腹部肚脐'],
    'middle_crotch': ['腹部肚脐', '裆部', '腿部'],
    'middle_hips': ['臀部'],
    'middle_leg': ['腿部'],
    'middle_normal': ['无'],
    'middle_shoulders_and_belly': ['腹部肚脐'],
    'no_person': ['无'],
    'sexy_kiss': ['无'],
    'stockings': ['腿部'],
    'upper_backless': ['背部'],
    'upper_bust': ['胸部'],
    'upper_large_bare': ['腹部肚脐', '裆部', '胸部'],
    'upper_normal': ['无'],
    'upper_shoulders_and_belly': ['腹部肚脐'],
    'upper_small_bare': ['胸部'],
    'whole_backless': ['背部', '臀部', '腿部'],
    'whole_large_bare': ['肩部', '胸部', '腹部肚脐', '裆部', '腿部'],
    'whole_leg': ['腿部'],
    'whole_normal': ['无'],
    'whole_shoulders_and_belly': ['肩部', '腹部肚脐'],
    'whole_small_bare': ['肩部', '腿部']
}

mapping_body_en = {
    'baby': ['shoulder', 'chest', 'back', 'belly'],
    'lower_hips': ['hips', 'legs'],
    'lower_large_bare': ['hips', 'legs'],
    'lower_leg': ['legs'],
    'lower_normal': ['None'],
    'lower_shoulders_and_belly': ['belly', 'legs'],
    'male_sexy': ['shoulder', 'breast', 'belly'],
    'middle_crotch': ['belly', 'crotch', 'legs'],
    'middle_hips': ['hips'],
    'middle_leg': ['legs'],
    'middle_normal': ['None'],
    'middle_shoulders_and_belly': ['belly'],
    'no_person': ['None'],
    'sexy_kiss': ['None'],
    'stockings': ['legs'],
    'upper_backless': ['back'],
    'upper_bust': ['breast'],
    'upper_large_bare': ['belly', 'crotch', 'breast'],
    'upper_normal': ['None'],
    'upper_shoulders_and_belly': ['belly'],
    'upper_small_bare': ['breast'],
    'whole_backless': ['back', 'hips', 'legs'],
    'whole_large_bare': ['shoulder', 'breast', 'belly', 'crotch', 'legs'],
    'whole_leg': ['legs'],
    'whole_normal': ['None'],
    'whole_shoulders_and_belly': ['shoulder', 'belly'],
    'whole_small_bare': ['shoulder', 'leg']
}
yes_list = ['baby',
            'lower_hips',
            'lower_large_bare',
            'lower_leg',
            'lower_shoulders_and_belly',
            'male_sexy',
            'middle_crotch',
            'middle_hips',
            'middle_leg',
            'middle_shoulders_and_belly',
            'sexy_kiss',
            'stockings',
            'upper_backless',
            'upper_bust',
            'upper_large_bare',
            'upper_normal',
            'upper_shoulders_and_belly',
            'upper_small_bare',
            'whole_backless',
            'whole_large_bare',
            'whole_leg',
            'whole_shoulders_and_belly',
            'whole_small_bare']
no_list = ['lower_normal', 'middle_normal', 'no_person', 'whole_normal']
all_list = ['baby',
            'lower_hips',
            'lower_large_bare',
            'lower_leg',
            'lower_shoulders_and_belly',
            'male_sexy',
            'middle_crotch',
            'middle_hips',
            'middle_leg',
            'middle_shoulders_and_belly',
            'sexy_kiss',
            'stockings',
            'upper_backless',
            'upper_bust',
            'upper_large_bare',
            'upper_normal',
            'upper_shoulders_and_belly',
            'upper_small_bare',
            'whole_backless',
            'whole_large_bare',
            'whole_leg',
            'whole_shoulders_and_belly',
            'whole_small_bare',
            'lower_normal', 'middle_normal', 'no_person', 'whole_normal']
# prompting example

prompting_llm_example = '根据以下例句生成10个表意相似的句子: ' + questions[0]


def update_mapping_from_txt(filename, trainlist_name, n_sample):
    trainlist = text_readlines(trainlist_name)
    class_list = get_class(trainlist)
    n_class = len(class_list)
    for c in class_list:
        mapping[c] = []
    content = text_readlines(filename)
    for class_id in range(n_class):
        for sample_id in range(n_sample):
            mapping[class_list[class_id]].append(content[class_id * n_sample + sample_id])
    return mapping

def generate_llava_train_json(img_list):
    trainlist = text_readlines(img_list)
    # print(trainlist)
    f = open('/home/mywu/mywu/models/LLaVa-COCO-Finetune-150k/llava_v1_5_mix665k.json', 'r')
    val_json = json.load(f)
    id = 0
    prefix_q0_en = 'Please check if the following sentences describe the image correctly, answers in yes or no:'
    prefix_q0_cn = '请判断该图片是否满足下列描述，回答是或者否：'
    prefix_q1_en = 'Please select the positions of bodies in the image, which show bare or sexual innuendo: (multi choice)'
    prefix_q1_cn = '请从下列选项中选出该图片中人物性感或者裸露的身体部位：（多选）'
    prefix_q2_en = 'Please descrbe the level of nudity'
    prefix_q2_cn = '请从下列选项中选择图中人物裸露的程度：非常裸露，一般裸露，不裸露'
    prefix_q3_en = 'Please descrbe the level of sexy'
    prefix_q3_cn = '请从下列选项中选择图中人物性感的程度：非常性感，一般性感，不性感'
    answer_q0_cn = ['是', '否']
    answer_q0_en = ['Yes', 'No']

    answer_q1_cn = ['肩部', '胸部', '背部', '腹部肚脐', '裆部', '臀部', '腿部', '无']
    answer_q2_cn = ['非常裸露', '一般裸露', '不裸露']
    answer_q3_cn = ['非常性感', '一般性感', '不性感']
    answer_q1_en = ['shoulder', 'bust', 'beck', 'belly', 'crotch', 'hips', 'legs', 'None']
    answer_q2_en = ['Severe nudity', 'Moderate nudity', 'Not nudity']
    answer_q3_en = ['Very sexy', 'Moderate sexy', 'Not sexy']
    very_sexy_list = [
        'lower_hips',
        'lower_large_bare',
        'male_sexy',
        'middle_crotch',
        'middle_hips',
        'sexy_kiss',
        'stockings',
        'upper_backless',
        'upper_bust',
        'upper_large_bare',
        'whole_backless',
        'whole_large_bare',
    ]
    mid_sexy_list = ['whole_shoulders_and_belly', 'whole_small_bare', 'lower_shoulders_and_belly',
                     'middle_shoulders_and_belly', 'middle_leg', 'lower_leg', 'whole_leg', 'upper_shoulders_and_belly',
                     'upper_small_bare', ]
    not_sexy_list = ['baby', 'upper_normal', 'lower_normal', 'middle_normal', 'no_person', 'whole_normal']
    very_bare_list = ['baby',
                      'lower_large_bare',
                      'male_sexy',
                      'middle_crotch',
                      'middle_hips',
                      'stockings',
                      'upper_backless',
                      'upper_bust',
                      'upper_large_bare',
                      'whole_large_bare',
                      ]
    mid_bare_list = ['middle_leg', 'lower_leg',
                     'lower_shoulders_and_belly', 'whole_leg',
                     'whole_shoulders_and_belly',
                     'whole_small_bare', 'upper_shoulders_and_belly',
                     'upper_small_bare',
                     'whole_backless', 'middle_shoulders_and_belly', ]
    not_bare_list = ['sexy_kiss', 'lower_hips', 'upper_normal', 'lower_normal', 'middle_normal', 'no_person',
                     'whole_normal']
    for img_path in trainlist:
        class_name = img_path.split('/')[0]
        # for q0
        descriptions_yes = random.choice(mapping[class_name])
        another_class = random.choice(all_list)
        while another_class == class_name:
            another_class = random.choice(all_list)
        descriptions_no = random.choice(mapping[class_name])
        flg = id % 2
        if flg == 0:
            descriptions = descriptions_yes
            gt = answer_q0_en[flg]
        else:
            descriptions = descriptions_no
            gt = answer_q0_en[flg]
        # for q1
        body_positions = mapping_body_en[class_name]
        choices = random.sample(all_body_positions_en, 4)
        while len(set(body_positions) & set(choices)) == 0:
            choices = random.sample(all_body_positions_en, 4)
        gt_list = set(body_positions) & set(choices)
        questions_choice = str(choices)[1:-1]
        gt_choice = str(gt_list)[1:-1]
        # for q2 q3
        if class_name in very_bare_list:
            gt_bare = 'Severe nudity'
        elif class_name in mid_bare_list:
            gt_bare = 'Moderate nudity'
        else:
            gt_bare =  'Not nudity'
        if class_name in very_sexy_list:
            gt_sexy = 'Very sexy'
        elif class_name in mid_sexy_list:
            gt_sexy = 'Moderate sexy'
        else:
            gt_sexy = 'Not sexy'
        img_json = {}
        img_json["id"] = "identity_" + str(id)
        id += 1
        img_json["image"] = 'sexy_check/' + img_path
        img_json["conversations"] = [
            {
                "from": "human",
                "value": "<image>\n" + prefix_q0_en + descriptions
            },
            {
                "from": "gpt",
                "value": gt
            },
            {
                "from": "human",
                "value": prefix_q1_en + questions_choice
            },
            {
                "from": "gpt",
                "value": gt_choice
            },
            {
                "from": "human",
                "value": prefix_q2_en
            },
            {
                "from": "gpt",
                "value": gt_bare
            },
            {
                "from": "human",
                "value": prefix_q3_en
            },
            {
                "from": "gpt",
                "value": gt_sexy
            }
        ]
        # print(img_json)
        val_json.append(img_json)
        # if id > 50: break
    print(random.choice(val_json))
    print(random.choice(val_json))
    print(random.choice(val_json))
    print(random.choice(val_json))
    print(random.choice(val_json))
    with open(img_list[:-4] + '.json', 'w') as fp:
        json.dump(val_json, fp)


def filter_img_list(img_list):
    trainlist = text_readlines(img_list)
    new_trainlist = []
    for l in trainlist:
        if 'jpg' in l or 'jpeg' in l or 'png' in l or 'JPG' in l or 'JPEG' in l or 'PNG' in l:
            new_trainlist.append(l)
    text_save(new_trainlist, 'vallist.txt')


if __name__ == '__main__':
    # use answers_en.txt and questions_en list for english data
    # filter_img_list('vallist.txt')
    mapping = update_mapping_from_txt(filename='answers_en.txt', trainlist_name='_trainlist.txt', n_sample=11)
    generate_llava_train_json('_trainlist.txt')

    #   {  llava examples
    #     "id": "000000033471",
    #     "image": "coco/train2017/000000033471.jpg",
    #     "conversations": [
    #       {
    #         "from": "human",
    #         "value": "<image>\nWhat are the colors of the bus in the image?"
    #       },
    #       {
    #         "from": "gpt",
    #         "value": "The bus in the image is white and red."
    #       },
    #       {
    #         "from": "human",
    #         "value": "What feature can be seen on the back of the bus?"
    #       },
    #       {
    #         "from": "gpt",
    #         "value": "The back of the bus features an advertisement."
    #       },
    #       {
    #         "from": "human",
    #         "value": "Is the bus driving down the street or pulled off to the side?"
    #       },
    #       {
    #         "from": "gpt",
    #         "value": "The bus is driving down the street, which is crowded with people and other vehicles."
    #       }
    #     ]
    #   }

    # {
    #      'id': 'identity_46912',
    #      'image': '../../data/sexy_check/upper_shoulders_and_belly/upper_shoulders_and_belly_2022072011061758004_v2.jpg',
    #      'conversations': [
    #                        {'from': 'human','value': '<image>\n请判断该图片是否满足下列描述，回答是或者否：这是一张上半身图像，图中的人物裸露了肚子，且露出了肚脐眼'},
    #                        {'from': 'gpt', 'value': '是'},
    #                        {'from': 'human', 'value': "请从下列选项中选出该图片中人物性感或者裸露的身体部位：（多选）'裆部', '腹部肚脐', '臀部', '无'"},
    #                        {'from': 'gpt', 'value': "'腹部肚脐'"},
    #                        {'from': 'human', 'value': '请从下列选项中选择图中人物裸露的程度：非常裸露，一般裸露，不裸露'},
    #                        {'from': 'gpt', 'value': '一般裸露'},
    #                        {'from': 'human', 'value': '请从下列选项中选择图中人物性感的程度：非常性感，一般性感，不性感'},
    #                        {'from': 'gpt', 'value': '一般性感'}
    #                        ]
    # }
