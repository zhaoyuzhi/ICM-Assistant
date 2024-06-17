# -*- coding: utf-8 -*-
import os

# save a list to a txt
def text_save(content, filename, mode = 'a'):
    # try to save a list variable in txt file.
    # Use the following command if Chinese characters are written (i.e., text in the file will be encoded in utf-8)
    file = open(filename, mode, encoding='utf-8')
    # file = open(filename, mode)
    for i in range(len(content)):
        file.write(str(content[i]) + '\n')
    file.close()

# read a txt expect EOF
def text_readlines(filename, mode = 'r'):
    # try to read a txt file and return a list.Return [] if there was a mistake.
    try:
        # Use the following command if there is Chinese characters are read
        file = open(filename, mode, encoding='utf-8')
        # file = open(filename, mode)
    except IOError:
        error = []
        return error
    content = file.readlines()
    # This for loop deletes the EOF (like \n)
    for i in range(len(content)):
        content[i] = content[i][:len(content[i]) - 1]
    file.close()
    return content

# read a folder, return the complete path of all files
def get_files(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    return ret

if __name__ == '__main__':

    # define the fixed question dic
    dic = {
        'chuansiwa_cn': '已知这张图像中的人物正在穿丝袜，这通常会让人感觉有性暗示，请结合这一信息描述这张图像。再评价图像的整体氛围。最后请你评价这张图像的性感程度（轻度性感，一般性感，非常性感）',
        'chuansiwa': 'Given that the person in this image is wearing stockings, which is often perceived as sexually suggestive, please describe the image in conjunction with this information. Then, describe the overall atmosphere of the image. Finally, please rate the sexiness of this image (mildly sexy, moderately sexy, very sexy)',
        'duzui_cn': '已知这张图像中的人物有嘟嘴的行为，这通常会让人感觉有性暗示，请结合这一信息描述这张图像。再评价图像的整体氛围。最后请你评价这张图像的性感程度（轻度性感，一般性感，非常性感）',
        'duzui': 'The person in this image is known to pout, which is often perceived as sexually suggestive. Please describe this image in conjunction with this information. Then, describe the overall atmosphere of the image. Finally, please rate the sexiness of this image (mildly sexy, moderately sexy, very sexy)',
        'fumotunbu_cn': '已知这张图像中的人物在抚摸臀部，这通常会让人感觉有性暗示，请结合这一信息描述这张图像。再评价图像的整体氛围。最后请你评价这张图像的性感程度（轻度性感，一般性感，非常性感）',
        'fumotunbu': 'Since the person in this image is touching their buttocks, which is often perceived as sexually suggestive, please describe the image in conjunction with this information. Then, describe the overall atmosphere of the image. Finally, please rate the sexiness of this image (mildly sexy, moderately sexy, very sexy)',
        'fumoxiongbu_cn': '已知这张图像中的人物在抚摸胸部，这通常会让人感觉有性暗示，请结合这一信息描述这张图像。再评价图像的整体氛围。最后请你评价这张图像的性感程度（轻度性感，一般性感，非常性感）',
        'fumoxiongbu': 'We know that the person in this image is touching breasts, which is often perceived as sexually suggestive, so please describe the image in conjunction with this information. Then, describe the overall atmosphere of the image. Finally, please rate the sexiness of this image (mildly sexy, moderately sexy, very sexy)',
        'lujian_cn': '已知这张图像中的人物刻意露出双肩，这通常会让人感觉有性暗示，请结合这一信息描述这张图像。再评价图像的整体氛围。最后请你评价这张图像的性感程度（轻度性感，一般性感，非常性感）',
        'lujian': 'We know that the shoulders of the person in this image are deliberately exposed, which is often perceived as sexually suggestive. Please describe this image in conjunction with this information. Then, describe the overall atmosphere of the image. Finally, please rate the sexiness of this image (mildly sexy, moderately sexy, very sexy)',
        'liaoqunzi_cn': '已知这张图像中的人物正在撩裙子，这通常会让人感觉有性暗示，请结合这一信息描述这张图像。再评价图像的整体氛围。最后请你评价这张图像的性感程度（轻度性感，一般性感，非常性感）',
        'liaoqunzi': 'Given that the person in this image is lifting her skirt, which is often perceived as sexually suggestive, please describe the image in conjunction with this information. Then, describe the overall atmosphere of the image. Finally, please rate the sexiness of this image (mildly sexy, moderately sexy, very sexy)',
        'liaoyifu_cn': '已知这张图像中的人物正在撩衣服，这通常会让人感觉有性暗示，请结合这一信息描述这张图像。再评价图像的整体氛围。最后请你评价这张图像的性感程度（轻度性感，一般性感，非常性感）',
        'liaoyifu': 'Given that the person in this image is lifting their clothes, which is often perceived as sexually suggestive, please describe the image in conjunction with this information. Then, describe the overall atmosphere of the image. Finally, please rate the sexiness of this image (mildly sexy, moderately sexy, very sexy)',
        'shishen_cn': '已知这张图像中的人物穿着湿衣，这通常会让人感觉有性暗示，请结合这一信息描述这张图像。再评价图像的整体氛围。最后请你评价这张图像的性感程度（轻度性感，一般性感，非常性感）',
        'shishen': 'Given that the person in this image is wearing a wetsuit, which is often perceived as sexually suggestive, please describe the image in conjunction with this information. Then, describe the overall atmosphere of the image. Finally, please rate the sexiness of this image (mildly sexy, moderately sexy, very sexy)',
        'shouzhixiangminganbuwei_cn': '已知这张图像中的人物手指指向敏感部位，这通常会让人感觉有性暗示，请结合这一信息描述这张图像。再评价图像的整体氛围。最后请你评价这张图像的性感程度（轻度性感，一般性感，非常性感）',
        'shouzhixiangminganbuwei': 'Please describe this image in light of the fact that the person in this image is pointing fingers at sensitive areas, which is often perceived as sexually suggestive. Then, describe the overall atmosphere of the image. Finally, please rate the sexiness of this image (mildly sexy, moderately sexy, very sexy)',
        'tushetou_cn': '已知这张图像中的人物吐舌头，这通常会让人感觉有性暗示，请结合这一信息描述这张图像。再评价图像的整体氛围。最后请你评价这张图像的性感程度（轻度性感，一般性感，非常性感）',
        'tushetou': 'Given that the figure in this image is sticking out his or her tongue, which is often perceived as sexually suggestive, please describe the image in conjunction with this information. Then, describe the overall atmosphere of the image. Finally, please rate the sexiness of this image (mildly sexy, moderately sexy, very sexy)',
        'tuoneiyi_cn': '已知这张图像中的人物正在脱内衣，这通常会让人感觉有性暗示，请结合这一信息描述这张图像。再评价图像的整体氛围。最后请你评价这张图像的性感程度（轻度性感，一般性感，非常性感）',
        'tuoneiyi': 'Given that the person in this image is taking off their clothes, which is often perceived as sexually suggestive, please describe the image in conjunction with this information. Then, describe the overall atmosphere of the image. Finally, please rate the sexiness of this image (mildly sexy, moderately sexy, very sexy)',
        'tuoyifu_cn': '已知这张图像中的人物正在脱内衣，这通常会让人感觉有性暗示，请结合这一信息描述这张图像。再评价图像的整体氛围。最后请你评价这张图像的性感程度（轻度性感，一般性感，非常性感）',
        'tuoyifu': 'Given that the person in this image is taking off their clothes, which is often perceived as sexually suggestive, please describe the image in conjunction with this information. Then, describe the overall atmosphere of the image. Finally, please rate the sexiness of this image (mildly sexy, moderately sexy, very sexy)',
        'yanshenaimei_cn': '已知这张图像中的人物眼神暧昧，这通常会让人感觉有性暗示，请结合这一信息描述这张图像。再评价图像的整体氛围。最后请你评价这张图像的性感程度（轻度性感，一般性感，非常性感）',
        'yanshenaimei': 'We know that the person in this image has ambiguous eyes, which is often perceived as sexually suggestive. Please describe this image in conjunction with this information. Then, describe the overall atmosphere of the image. Finally, please rate the sexiness of this image (mildly sexy, moderately sexy, very sexy)',
        'yaochun_cn': '已知这张图像中的人物咬唇，这通常会让人感觉有性暗示，请结合这一信息描述这张图像。再评价图像的整体氛围。最后请你评价这张图像的性感程度（轻度性感，一般性感，非常性感）',
        'yaochun': 'Since the person in this image is biting his lip, which is often perceived as sexually suggestive, please describe the image in conjunction with this information. Then, describe the overall atmosphere of the image. Finally, please rate the sexiness of this image (mildly sexy, moderately sexy, very sexy)',
        'yaoshouzhi_cn': '已知这张图像中的人物咬手指，这通常会让人感觉有性暗示，请结合这一信息描述这张图像。再评价图像的整体氛围。最后请你评价这张图像的性感程度（轻度性感，一般性感，非常性感）',
        'yaoshouzhi': 'It is known that the person in this image is biting his finger, which is often perceived as sexually suggestive. Please describe the image in conjunction with this information. Then, describe the overall atmosphere of the image. Finally, please rate the sexiness of this image (mildly sexy, moderately sexy, very sexy)'
    }

    # read
    folder_path = 'data'
    imglist = get_files(folder_path)

    # save to a list
    savelist = []
    for i in range(len(imglist)):
        
        # get the path
        imgname = imglist[i].replace(folder_path, '')[1:]
        imgname = imgname.replace('\\', '/')

        # identify label
        label = imgname.split('/')[-2]
        q_en = dic[label]
        q_cn = dic[label + '_cn']

        # save to a list
        savelist.append(imgname)
        savelist.append(q_en)

    text_save(savelist, 'list_file.txt', mode = 'a')