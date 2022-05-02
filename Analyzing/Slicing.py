import sqlite3
import random
import pandas as pd
import jieba.analyse
import os
import sys
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER

def jiebaSlice(content):
    words = jieba.posseg.cut(content)
    slicedWords = []
    for word, flag in words:
        slicedWords.append(word)
    return slicedWords
    
def ckipSlice(content):
    # Download data
    # 下面這邊的，可以想清楚再下載沒關係，因為真的有點大XDD
    # data_utils.download_data("./") 

    # Load model without GPU
    # 啊如果，真的載下來了，記得把路徑改成 ./data
    ws = WS("/Users/garychen/Documents/ckiptagger/data")
    pos = POS("/Users/garychen/Documents/ckiptagger/data")
    ner = NER("/Users/garychen/Documents/ckiptagger/data")
    
    sentence_list = [f'{content}']
    
    word_sentence_list = ws(sentence_list)
    pos_sentence_list = pos(word_sentence_list)
    entity_sentence_list = ner(word_sentence_list, pos_sentence_list)

    # Release model
    del ws
    del pos
    del ner
    
    result = []
    # Show results
    def print_word_pos_sentence(word_sentence, pos_sentence):
        assert len(word_sentence) == len(pos_sentence)
        all_word = []
        for word, pos in zip(word_sentence, pos_sentence):
            # print(f"{word}({pos})", end="\u3000")
            all_word.append(word)
        return all_word

    for i, sentence in enumerate(sentence_list):
        result = (print_word_pos_sentence(word_sentence_list[i],  pos_sentence_list[i]))
    
    return result

cnx = sqlite3.connect('../Scraping/Data/FilteredArticles.db')
df = pd.read_sql_query("SELECT * FROM FilteredArticles", cnx)
length = df.shape[0]


test_article = df['content'][random.randint(0,length)]

# 看你這邊想要用哪一種。
# result = ckipSlice(test_article)
result = jiebaSlice(test_article)
countFreuency = [[x,result.count(x)] for x in set(result)]

print(countFreuency)