#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
/Users/charleslai/PycharmProjects/faker_flask/faker/models.mode_predictor.py was created on 2018/11/13.
file in :relativeFile
Author: Charles_Lai
Email: lai.bluejay@gmail.com
"""
import os, sys
import jieba
from faker.utils.log_utils import exe_time_v0
from faker.utils import DATA_DIR

STOPWORD_PATH = DATA_DIR + "stopwords_cn.txt"
MODEL_PATH = DATA_DIR + "model/"

def load_model(model_path):
    # 加载模型
    # 加载windows模型
    import fastText.FastText as ff
    classifier = ff.load_model(model_path)

    return classifier

# 读取文件


def read_file(path):
    content = list()
    with open(path, "r+") as fp:
        for line in fp:
            content.append(line.strip())
    return content

# 分词，预处理


def deal_datas(content, stopword):
    seg_list = []
    segs = jieba.lcut(content)  # 分词
    segs = filter(lambda x: len(x) > 1, segs)
    segs = filter(lambda x: x not in stopword, segs)
    for i in segs:
        seg_list.append(i)
    str_con = ' '.join(seg_list)
    return str_con


class Predictor(object):
    def __init__(self, stopword_path=STOPWORD_PATH, model_save_path=MODEL_PATH):
        self.stopword_path = stopword_path
        self.model_save_path = model_save_path
        self.classifier_dict = dict()
        self.stopword = None
        self.init()

    @exe_time_v0
    def init(self):
        self.stopword = read_file(self.stopword_path)
        for model in os.listdir(self.model_save_path):
            tmp = load_model(self.model_save_path+model)
            self.classifier_dict[model] = tmp

    @exe_time_v0
    def prediction(self, texts):
        stopword = self.stopword
        final_results = list()
        for model, clf in self.classifier_dict.items():
            # z这个位置源文件就是加载目录下的多个文件。
            text_list = []
            text_list.append(deal_datas(texts, stopword))
            classifier = clf
            # 预测文件
            pre_dic = {}
            # 同时每个texts在这里被预测，然后覆盖lable。
            label = classifier.predict(text_list, k=3)
            pre_dic[texts] = label
            txtcalss = model.split('_')[1].replace('add', '区域分类').replace('sub', '学科分类').replace('work', '行业分类').replace('ch', '中图分类')
            for i, j in pre_dic.items():
                z = 1
                for p in j[0][0]:
                    p = p.replace('__label__', '')
                    p = p.replace(',', '')

                    if z == 1:
                        pre_dic["classname"] = txtcalss
                        pre_dic["classno"] = p
                        # print(p+',')
                        final_results.append(pre_dic)
                    # out = i + '	' + p
                    z = z + 1
                    break
            return final_results
            # fpl.write('\t')


if __name__ == '__main__':
    current_path = sys.argv[1]
    #current_path ='D:\Workspacess\python\pythonWorkSpace\TEXT_CLASSIFY'

    # sys.argv[1]
    stopword_path = current_path+'\\datas\\infos\\stopwords\\中文.txt'
    #nput_file = current_path + '/datas/inputfiles/'
    #input_str = input('请输入要分类的文本：')
    #input_str = '当你累的时候你会想起谁？'
    input_str = sys.argv[2]
    result_save_path = current_path + '/datas/results/'
    model_save_path_book = current_path + '/datas/model/book/'
    model_save_path_bookPatcher = current_path + '/datas/model/bookPatcher/'
    predictor = Predictor(stopword_path=stopword_path,
                          model_save_path=model_save_path_book)
    print(predictor.prediction(input_str))
