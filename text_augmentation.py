import os
import re
import json
from random import shuffle, choice
from ltp import LTP
from tqdm import tqdm

# settings
ltp = LTP()
with open("corpus/corpus4typos.json", "r") as f:
    dict_typos = json.load(f)
with open("corpus/corpus_handian/word_handian/corpus4v.json", "r") as f:
    dict_v = json.load(f)
with open("corpus/corpus_handian/word_handian/corpus4adj.json", "r") as f:
    dict_adj = json.load(f)
with open("corpus/corpus_handian/word_handian/corpus4adv.json", "r") as f:
    dict_adv = json.load(f)
with open("corpus/corpus_handian/word_handian/corpus4n.json", "r") as f:
    dict_n = json.load(f)
    

def twist_num(q):
    global ltp
    lst_q = list()
    ltp_word, hidden = ltp.seg([q])
    ltp_pos = ltp.pos(hidden)
    for word, w_pos in zip(ltp_word[0], ltp_pos[0]):
        pos = w_pos.lower()
        if pos == "m":
            word_new = ""
            for char in word:
                if char in ['一', '二', '三', '四', '五', '六', '七', '八', '九']:
                    lst_candi = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
                    lst_candi.remove(char)
                    candi = choice(lst_candi)
                elif char in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    lst_candi = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
                    lst_candi.remove(char)
                    candi = choice(lst_candi)
                else:
                    candi = char
                word_new += candi
            word = word_new
        lst_q.append(word)
    q_new = "".join(lst_q)
    q_tag = True if q_new != q else False
    return q_new, q_tag


def update_typos(char):
    global dict_typos
    if char in dict_typos.keys():
        if "similar_phone" in dict_typos[char] and "number" in dict_typos[char]:
            for candi in dict_typos[char]["similar_phone"]:
                if candi[1] == dict_typos[char]["number"]:
                    return candi[0], True
            if len(dict_typos[char]["similar_phone"]) > 0:
                return choice(dict_typos[char]["similar_phone"])[0], True
        if "similar_form" in dict_typos[char] and "number" in dict_typos[char]:
            for candi in dict_typos[char]["similar_form"]:
                if candi[1] == dict_typos[char]["number"]:
                    return candi[0], True
            if len(dict_typos[char]["similar_form"]) > 0:
                return choice(dict_typos[char]["similar_form"])[0], True                   
    return char, False
    

def twist_typos(q):
    global ltp
    lst_candi = list()
    ltp_word, hidden = ltp.seg([q])
    ltp_pos = ltp.pos(hidden)
    for w, w_pos in zip(ltp_word[0], ltp_pos[0]):
        pos = w_pos.lower()
        if ("n" in pos) or (pos == "i") or (pos == "j") or (pos == "r"):
            lst_candi.append([w, len(w)])
    if len(lst_candi) == 0:
        return q, False
    lst_candi.sort(key=lambda x:x[1], reverse=True)
    for word, _ in lst_candi:
        lst_word = list(word)
        lst_idx = list(range(len(lst_word)))
        shuffle(lst_idx)
        for i in lst_idx:
            char_old = lst_word[i]
            char_new, flag = update_typos(char_old)
            if flag:
                lst_word[i] = char_new
                word_update = "".join(lst_word)
                q = q.replace(word, word_update, 1)
                return q, True
    return q, False


def twist_synonym(q, pos_tag="v"):
    global dict_v, dict_adj, dict_adv, dict_n, ltp
    # set conditions
    if pos_tag == "v":
        dict_now = dict_v
        condition = "\"v\" in pos"
    elif pos_tag == "adj":
        dict_now = dict_adj
        condition = "pos in [\"a\", \"b\"]"
    elif pos_tag == "adv":
        dict_now = dict_adv
        condition = "pos in [\"d\"]"
    elif pos_tag == "n":
        dict_now = dict_n
        condition = "\"n\" in pos"
    else:
        return q, False
    # get candidates
    lst_candi = list()
    ltp_word, hidden = ltp.seg([q])
    ltp_pos = ltp.pos(hidden)
    for w, w_pos in zip(ltp_word[0], ltp_pos[0]):
        pos = w_pos.lower()
        if eval(condition):
            lst_candi.append(w)
    if len(lst_candi) == 0:
        return q, False
    shuffle(lst_candi)
    # update candidates
    for word in lst_candi:
        if word in dict_now.keys():
            if len(dict_now[word]["synonym"]) > 0:
                word_update = choice(dict_now[word]["synonym"])
                q = q.replace(word, word_update, 1)
                return q, True
    return q, False


def twist_antonym(q, pos_tag="v"):
    global dict_v, dict_adj, dict_adv, dict_n, ltp
    # set conditions
    if pos_tag == "v":
        dict_now = dict_v
        condition = "\"v\" in pos"
    elif pos_tag == "adj":
        dict_now = dict_adj
        condition = "pos in [\"a\", \"b\"]"
    elif pos_tag == "adv":
        dict_now = dict_adv
        condition = "pos in [\"d\"]"
    elif pos_tag == "n":
        dict_now = dict_n
        condition = "\"n\" in pos"
    else:
        return q, False
    # get candidates
    lst_candi = list()
    ltp_word, hidden = ltp.seg([q])
    ltp_pos = ltp.pos(hidden)
    for w, w_pos in zip(ltp_word[0], ltp_pos[0]):
        pos = w_pos.lower()
        if eval(condition):
            lst_candi.append(w)
    if len(lst_candi) == 0:
        return q, False
    shuffle(lst_candi)
    # update candidates
    for word in lst_candi:
        if word in dict_now.keys():
            if len(dict_now[word]["antonym"]) > 0:
                word_update = choice(dict_now[word]["antonym"])
                q = q.replace(word, word_update, 1)
                return q, True
    return q, False


def show_fix_input():
    print(twist_num("这是十二亿元的问题吗"))
    print(twist_num("42个苹果就是宇宙的终极答案吗"))
    print(twist_typos("命运之夜的结局是皆大欢喜的吗"))
    print(twist_synonym("他最后是快乐地接受了这个悲惨的结局吗", "v"))
    print(twist_synonym("他最后是快乐地接受了这个悲惨的结局吗", "adj"))
    print(twist_synonym("他最后是快乐地接受了这个悲惨的结局吗", "adv"))
    print(twist_synonym("他最后是快乐地接受了这个悲惨的结局吗", "n"))
    print(twist_antonym("他最后是快乐地接受了这个悲惨的结局吗", "v"))
    print(twist_antonym("他最后是快乐地接受了这个悲惨的结局吗", "adj"))
    print(twist_antonym("他最后是快乐地接受了这个悲惨的结局吗", "adv"))
    print(twist_antonym("他最后是快乐地接受了这个悲惨的结局吗", "n"))
    return None


if __name__ == "__main__":
    show_fix_input()
    show_self_defined_input("公积金提取记录单到哪儿打印")
    
    
    

