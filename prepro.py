# -*- coding:utf-8 -*-
import os
import re
import ast
import json
import pandas as pd
from pypinyin import pinyin
from fuzzywuzzy import fuzz
from tqdm import tqdm


def create_part_dictionary():
    """
    合并、生成部首词典
    :return: dict_part: {部首: True, ...}
    """
    part_path = "corpus/char_part/hanzi_pianpang.json"
    with open(part_path, "r") as f:
        dict_part = json.load(f)
    return dict_part


def create_number_dictionary():
    """
    合并、生成笔画数词典
    :return: dict_number: {字: 笔画数, ...}
    """
    root_path = "corpus/char_number/"
    dict_number = dict()
    for file_name in os.listdir(root_path):
        if file_name.endswith(".txt"):
            load_path = os.path.join(root_path, file_name)
            try:
                with open(load_path, "r") as f:
                    d = "".join([line.strip() for line in f.readlines()])
            except:
                with open(load_path, "r", encoding="gbk") as f:
                    d = "".join([line.strip() for line in f.readlines()])
            d = d.replace("'", "\"").replace("dict = ", "")
            d = ast.literal_eval(d)
            for k, v in d.items():
                dict_number.update({k: int(v)})
    return dict_number


def create_corner_dictionary():
    """
    生成四角编码字典
    :return: dict_corner: {字: 四角码}, dict_corner_idx: {四角码: [字, ...]}
    """
    corner_dir = "corpus/char_similar/"
    dict_corner = dict()
    for file_name in os.listdir(corner_dir):
        if "四角" in file_name:
            load_path = os.path.join(corner_dir, file_name)
            with open(load_path, "r") as f:
                for line in f.readlines():
                    line = re.sub("\s+", "", line)
                    line = line.replace("'", "\"").replace("，", ",").replace("：", ":")
                    line_split = line.split(":")
                    if len(line_split) == 2:
                        k = re.search(r"\".+\"", line_split[0])
                        v = re.search(r"\".+\"", line_split[1])
                        if k and v:
                            k = k.group().replace("\"", "")
                            v = v.group().replace("\"", "")
                            dict_corner.update({k: v})
    # 生成四角码索引字典
    dict_corner_idx = dict()
    for w, idx in dict_corner.items():
        if idx in dict_corner_idx.keys():
            if w not in dict_corner_idx[idx]:
                dict_corner_idx[idx].append(w)
        else:
            dict_corner_idx[idx] = [w]
    return dict_corner, dict_corner_idx


def create_structure_dictionary():
    """
    生成结构分类字典
    :return: dict_structure: {字: 结构分类}
    """
    structure_dir = "corpus/char_similar/"
    dict_structure = dict()
    for file_name in os.listdir(structure_dir):
        if "结构" in file_name:
            load_path = os.path.join(structure_dir, file_name)
            with open(load_path, "r") as f:
                for line in f.readlines():
                    line = re.sub("\s+", "", line)
                    line = line.replace("'", "\"").replace("，", ",").replace("：", ":")
                    line_split = line.split(":")
                    if len(line_split) == 2:
                        k = re.search(r"\".+\"", line_split[0])
                        v = re.search(r"\".+\"", line_split[1])
                        if k and v:
                            k = k.group().replace("\"", "")
                            v = v.group().replace("\"", "")
                            dict_structure.update({k: v})
    return dict_structure


def create_form_similar_dictionary():
    """
    生成形近字字典
    :return: dict_form: {字: [形近字, ...]}
    """
    form_dir = "corpus/char_similar"
    dict_form = dict()
    for file_name in os.listdir(form_dir):
        if "形近" in file_name:
            load_path = os.path.join(form_dir, file_name)
            with open(load_path, "r", encoding="gbk") as f:
                for line in f.readlines():
                    line = line.strip()
                    line_split = line.split(" ")
                    if len(line_split) == 2:
                        c = line_split[0]
                        for w in line_split[1]:
                            if c in dict_form.keys():
                                if w not in dict_form[c]:
                                    dict_form[c].append(w)
                            else:
                                dict_form[c] = [w]
    return dict_form


def create_phone_similar_dictionary():
    """
        生成音近字字典
        :return: dict_form: {字: [音近字, ...]}
        """
    phone_dir = "corpus/char_similar"
    dict_phone = dict()
    for file_name in os.listdir(phone_dir):
        if "音近" in file_name:
            load_path = os.path.join(phone_dir, file_name)
            with open(load_path, "r", encoding="gbk") as f:
                for line in f.readlines():
                    line = line.strip()
                    line_split = line.split(" ")
                    if len(line_split) == 2:
                        c = line_split[0]
                        for w in line_split[1]:
                            if c in dict_phone.keys():
                                if w not in dict_phone[c]:
                                    dict_phone[c].append(w)
                            else:
                                dict_phone[c] = [w]
    return dict_phone


def _is_chinese_char(char):
    res = False
    cp = ord(char)
    if ((cp >= 0x4E00 and cp <= 0x9FD5) or (cp >= 0x3400 and cp <= 0x4DB5) or (cp >= 0x20000 and cp <= 0x2A6D6) or (cp >= 0x2A700 and cp <= 0x2B734) or (cp >= 0x2B740 and cp <= 0x2B81D) or (cp >= 0x2B820 and cp <= 0x2CEA1) or (cp >= 0xF900 and cp <= 0xFAFF) or (cp >= 0x2F800 and cp <= 0x2FA1F) or (cp >= 0x2F00 and cp <= 0x2FDF) or (cp >= 0x2E80 and cp <= 0x2EFF) or (cp >= 0x31C0 and cp <= 0x31EF) or (cp >= 0x2FF0 and cp <= 0x2FFF)):
        res = True
    return res


def create_character_dictionary(dict_part, dict_number, is_save=False):
    """
    根据简繁拆字数据集构建基础字典
    :param dict_part: {部首: True, ...}
    :param dict_number: {字: 笔画数, ...}
    :return: dict_pronunciation: {拼音(含声调): [字, ...]}
             dict_char: {字: char_info}
             where char_info = {"split_to": ["part atom atom", ...],
                                "has_atom": [atom, ...],
                                "is_atom_of": [char, ...],
                                "has_part": [part, ...],
                                "is_part_of": [char, ...],
                                "pronunciation": [读音, ...],
                                "number": 笔画数,
                                "is_simple_to": [char, ...],
                                "is_traditional_to": [char, ...]}
    """
    ft_file_path = "corpus/char_split/chaizi-ft.txt"
    jt_file_path = "corpus/char_split/chaizi-jt.txt"
    map_file_path = "corpus/char_split/fanjian_suoyin.txt"

    dict_pronunciation = dict()
    # dict_ft = {"繁体char": {"split_to": ["第i种拆法", ...], "has_atom": [atom, ...], "has_part": [part, ...]}}
    #           where "第i种拆法" = "atom atom ..." 以空格隔开
    print("Get dict_ft ...")
    dict_ft = dict()
    with open(ft_file_path, "r") as f:
        for line in tqdm(f.readlines()):
            line = line.strip().split("\t")
            char = line[0].strip()
            if not _is_chinese_char(char):
                continue
            # add pronunciation information
            lst_pron = pinyin(char, heteronym=True)[0]
            if lst_pron[0] != char:
                dict_ft[char] = {"pronunciation": lst_pron}
                for pron in lst_pron:
                    if pron not in dict_pronunciation.keys():
                        dict_pronunciation[pron] = [char]
                    else:
                        if char not in dict_pronunciation[pron]:
                            dict_pronunciation[pron].append(char)
            else:
                dict_ft[char] = dict()
            # add part/atom information
            lst_atom, lst_part = list(), list()
            for s in line[1:]:
                for c in s.split():
                    c = c.strip()
                    if c in dict_part.keys():
                        lst_part.append(c)
                    else:
                        lst_atom.append(c)
            if "split_to" not in dict_ft[char].keys():
                dict_ft[char].update({"split_to": line[1:],
                                      "has_atom": list(set(lst_atom)),
                                      "has_part": list(set(lst_part))})
            else:
                dict_ft[char]["split_to"].extend(line[1:])
                dict_ft[char]["split_to"] = list(set(dict_ft[char]["split_to"]))
                dict_ft[char]["has_atom"].extend(lst_atom)
                dict_ft[char]["has_atom"] = list(set(dict_ft[char]["has_atom"]))
                dict_ft[char]["has_part"].extend(lst_part)
                dict_ft[char]["has_part"] = list(set(dict_ft[char]["has_part"]))
    # dict_jt = {"简体char": {"split_to": ["第i种拆法", ...], "has_atom": [atom, ...], "has_part": [part, ...]}}
    #           where "第i种拆法" = "atom atom ..." 以空格隔开
    print("Get dict_jt ...")
    dict_jt = dict()
    with open(jt_file_path, "r") as f:
        for line in tqdm(f.readlines()):
            line = line.strip().split("\t")
            char = line[0].strip()
            if not _is_chinese_char(char):
                continue
            # add pronunciation information
            lst_pron = pinyin(char, heteronym=True)[0]
            if lst_pron[0] != char:
                dict_jt[char] = {"pronunciation": lst_pron}
                for pron in lst_pron:
                    if pron not in dict_pronunciation.keys():
                        dict_pronunciation[pron] = [char]
                    else:
                        if char not in dict_pronunciation[pron]:
                            dict_pronunciation[pron].append(char)
            else:
                dict_jt[char] = dict()
            # add part/atom information
            lst_atom, lst_part = list(), list()
            for s in line[1:]:
                for c in s.split():
                    c = c.strip()
                    if c in dict_part.keys():
                        lst_part.append(c)
                    else:
                        lst_atom.append(c)
            if "split_to" not in dict_jt[char].keys():
                dict_jt[char].update({"split_to": line[1:],
                                      "has_atom": list(set(lst_atom)),
                                      "has_part": list(set(lst_part))})
            else:
                dict_jt[char]["split_to"].extend(line[1:])
                dict_jt[char]["split_to"] = list(set(dict_jt[char]["split_to"]))
                dict_jt[char]["has_atom"].extend(lst_atom)
                dict_jt[char]["has_atom"] = list(set(dict_jt[char]["has_atom"]))
                dict_jt[char]["has_part"].extend(lst_part)
                dict_jt[char]["has_part"] = list(set(dict_jt[char]["has_part"]))
    # add simple2traditional/traditional2simple relationships
    print("Get simple/traditional mapping ...")
    with open(map_file_path, "r") as f:
        for line in tqdm(f.readlines()):
            line = line.strip().split("\t")
            ft_now, jt_now = line[0], line[1]
            # traditional char
            if ft_now in dict_ft.keys():
                if dict_ft[ft_now].get("is_traditional_to", None):
                    if jt_now not in dict_ft[ft_now]["is_traditional_to"]:
                        dict_ft[ft_now]["is_traditional_to"].append(jt_now)
                else:
                    dict_ft[ft_now].update({"is_traditional_to": [jt_now]})
            else:
                dict_ft.update({ft_now: {"is_traditional_to": [jt_now]}})
            # simple char
            if jt_now in dict_jt.keys():
                if dict_jt[jt_now].get("is_simple_to", None):
                    if ft_now not in dict_jt[jt_now]["is_simple_to"]:
                        dict_jt[jt_now]["is_simple_to"].append(ft_now)
                else:
                    dict_jt[jt_now].update({"is_simple_to": [ft_now]})
            else:
                dict_jt.update({jt_now: {"is_simple_to": [ft_now]}})
    # dict_atom/dict_part = {"atom": [char, char, ...]}/{"part": [char, char, ...]}
    print("Get atom/part information ...")
    dict_atom, dict_part = dict(), dict()
    for c, d in dict_ft.items():  # get traditional atom and part
        for atom in d.get("has_atom", list()):
            if atom in dict_atom.keys():
                if c not in dict_atom[atom]:
                    dict_atom[atom].append(c)
        for part in d.get("has_part", list()):
            if part in dict_part.keys():
                if c not in dict_part[part]:
                    dict_part[part].append(c)
    for c, d in dict_jt.items():  # get simple atom and part
        for atom in d.get("has_atom", list()):
            if atom in dict_atom.keys():
                if c not in dict_atom[atom]:
                    dict_atom[atom].append(c)
        for part in d.get("has_part", list()):
            if part in dict_part.keys():
                if c not in dict_part[part]:
                    dict_part[part].append(c)
    for char in dict_ft:  # add is_atom_of/is_part_of attribute to dict_ft
        if char in dict_atom.keys():
            dict_ft[char].update({"is_atom_of": dict_atom[char]})
        if char in dict_part.keys():
            dict_ft[char].update({"is_part_of": dict_part[char]})
    for char in dict_jt:  # add is_atom_of/is_part_of attribute to dict_jt
        if char in dict_atom.keys():
            dict_jt[char].update({"is_atom_of": dict_atom[char]})
        if char in dict_part.keys():
            dict_jt[char].update({"is_part_of": dict_part[char]})
    # combine dict_ft and dict_jt
    print("Combine dict_ft and dict_jt ...")
    dict_char = {**dict_ft, **dict_jt}
    # add char number information
    print("Add number information ...")
    for k in tqdm(dict_char.keys()):
        if k in dict_number.keys():
            dict_char[k].update({"number": dict_number[k]})
    # save
    if is_save:
        print("Save dictionaries ...")
        with open("corpus/basic_dictionary.json", "w") as f:
            json.dump(dict_char, f, ensure_ascii=False, indent=2)
        with open("corpus/char_pronunciation/dict_pronunciation.json", "w") as f:
            json.dump(dict_pronunciation, f, ensure_ascii=False, indent=2)
    return dict_char, dict_pronunciation


def add_similar_char(dict_char, dict_form=None, dict_phone=None, dict_corner=None, dict_corner_idx=None, top_k=-1, is_save=False):
    """

    :param dict_char: dictionary generated in create_character_dictionary()
    :param dict_form: dictionary generated in create_form_similar_dictionary()
    :param dict_phone: dictionary generated in create_phone_similar_dictionary()
    :param dict_corner: dictionary generated in create_corner_dictionary()
    :param dict_corner_idx: dictionary generated in create_corner_dictionary()
    :param is_save: save newly generated dictionary or not
    :return: dict_char: {字: char_info}
             where char_info = {"split_to": ["part atom atom", ...],
                                "has_atom": [atom, ...],
                                "is_atom_of": [char, ...],
                                "has_part": [part, ...],
                                "is_part_of": [char, ...],
                                "pronunciation": [读音, ...],
                                "number": 笔画数,
                                "is_simple_to": [char, ...],
                                "is_traditional_to": [char, ...],
                                "similar_to": [char, ...]}
    """
    if dict_form is None:
        dict_form = create_form_similar_dictionary()
    if dict_phone is None:
        dict_phone = create_phone_similar_dictionary()
    if dict_corner is None or dict_corner_idx is None:
        dict_corner, dict_corner_idx = create_corner_dictionary()
    if dict_char is None:
        raise KeyError("[ERROR] dict_char not found!")
    print("Add similar characters ...")
    for char in tqdm(dict_char.keys()):
        lst_similar = list()
        # 形近字
        if char in dict_form.keys():
            lst_similar.extend(dict_form.get(char))
        # 音近字
        if char in dict_phone.keys():
            lst_similar.extend(dict_phone.get(char))
        # 四角相同字
        if char in dict_corner.keys():
            if dict_corner.get(char) in dict_corner_idx.keys():
                lst_similar.extend(dict_corner_idx.get(dict_corner.get(char)))
        # 新增相似字入dict_char
        lst_similar = list(set(lst_similar))
        if len(lst_similar) > 0:
            if "similar_to" in dict_char[char].keys():
                dict_char[char]["similar_to"].extend(lst_similar)
                dict_char[char]["similar_to"] = list(set(dict_char[char]["similar_to"]))
            else:
                dict_char[char].update({"similar_to": lst_similar})
            for neighbor in lst_similar:
                if neighbor in dict_char.keys():
                    if "similar_to" in dict_char[neighbor].keys():
                        if char not in dict_char[neighbor]["similar_to"]:
                            dict_char[neighbor]["similar_to"].append(char)
                    else:
                        dict_char[neighbor].update({"similar_to": [char]})
    # rank and filter similar words
    if top_k > 0:
        print("Filter Top {} similar words ...".format(top_k))
        print("[WARNING] This operation is extremely slow, which is not necessary.")
        for char, d_info in tqdm(dict_char.items()):
            if "similar_to" in d_info:
                lst_rank = list()
                for candidate in d_info.get("similar_to"):
                    score = compare_char(char, candidate, dict_char=dict_char, dict_corner=dict_corner)
                    lst_rank.append([candidate, score])
                lst_rank.sort(key=lambda x: x[1], reverse=True)
                lst_rank = [x[0] for x in lst_rank[:min(top_k, len(lst_rank)-1)]]
                dict_char[char]["similar_to"] = lst_rank
    # save
    if is_save:
        print("Save updated dictionaries ...")
        with open("corpus/basic_dictionary_similar.json", "w") as f:
            json.dump(dict_char, f, ensure_ascii=False, indent=2)
    return dict_char


def json2triple(load_path, save_path):
    """
    将字典中每个字的信息转换为三元组，便于建图谱
    :param load_path: path to load dict_char generated in create_character_dictionary()
    :param save_path: path to save the created list
    :return: None, lst = [[head, relation, tail], ...] is saved
    """
    assert load_path.endswith(".json") and save_path.endswith(".xlsx")
    print("Get triples ...")
    writer = pd.ExcelWriter(save_path)
    lst = list()
    with open(load_path, "r") as f:
        dict_char = json.load(f)
        for head, d in tqdm(dict_char.items()):
            for tail in d.get("has_atom", list()):
                lst.append([head, "has_atom", tail])
            for tail in d.get("is_atom_of", list()):
                lst.append([head, "is_atom_of", tail])
            for tail in d.get("has_part", list()):
                lst.append([head, "has_part", tail])
            for tail in d.get("is_part_of", list()):
                lst.append([head, "is_part_of", tail])
            for tail in d.get("pronunciation", list()):
                lst.append([head, "has_pronunciation", tail])
                lst.append([tail, "is_pronunciation_of", head])
            if d.get("number", None):
                lst.append([head, "has_number", d.get("number")])
                lst.append([d.get("number"), "is_number_of", head])
            for tail in d.get("is_simple_to", list()):
                lst.append([head, "is_simple_to", tail])
                lst.append([tail, "has_simple", head])
            for tail in d.get("is_traditional_to", list()):
                lst.append([head, "is_traditional_to", tail])
                lst.append([tail, "has_traditional", head])
            for tail in d.get("similar_to", list()):
                lst.append([head, "similar_to", tail])
                lst.append([tail, "similar_to", head])  # 其实不用算，因为add_similar_char已算过，不过下文会去重
    # delete repeated rows
    lst_head, lst_relation, lst_tail = list(), list(), list()
    for triple in lst:
        lst_head.append(triple[0])
        lst_relation.append(triple[1])
        lst_tail.append(triple[2])
    print("Remove repeated rows ...")
    df = pd.DataFrame({"head": lst_head, "relation": lst_relation, "tail": lst_tail})
    df = df[["head", "relation", "tail"]]
    df.drop_duplicates(keep='first', inplace=True)
    # save
    print("Save triple-based excel file ...")
    print("[WARNING] This operation might need 60 seconds.")
    df.to_excel(writer, index=0)
    writer.save()
    return None


def compare_char(char_a, char_b, dict_char=None, dict_corner=None, dict_structure=None):
    """
    规则方法对比两个字的相似度
    :param char_a: 字
    :param char_b: 字
    :param dict_char: dictionary generated in create_character_dictionary()
    :param dict_corner: dictionary generated in create_corner_dictionary()
    :param dict_structure: dictionary generated in create_structure_dictionary()
    :return: score: float in [0, 1] to show the similarity between char_a and char_b
    """
    if dict_corner is None:
        dict_corner, dict_corner_idx = create_corner_dictionary()
    if dict_structure is None:
        dict_structure = create_structure_dictionary()
    if dict_char is None:
        raise KeyError("[ERROR] dict_char not found!")
    # 结构类型比较
    score_structure = 1 if dict_structure.get(char_a, "-1") == dict_structure.get(char_b, "-2") else 0
    # 四角比较
    corner_a = dict_corner.get(char_a, None)
    corner_b = dict_corner.get(char_b, None)
    if corner_a is not None and corner_b is not None and len(corner_a) == len(corner_b):
        score_corner = sum(1 if corner_a[i] == corner_b[i] else 0 for i in range(len(corner_a)))/float(len(corner_a))
    else:
        score_corner = 0
    # 拼音比较
    score_pinyin = 1 if pinyin(char_a)[0] == pinyin(char_b)[0] else 0
    # 偏旁比较
    lst_part_a = dict_char[char_a].get("has_part", list()) if char_a in dict_char else list()
    lst_part_b = dict_char[char_b].get("has_part", list()) if char_b in dict_char else list()
    if char_b in lst_part_a:
        score_part = 1
    elif char_a in lst_part_b:
        score_part = 1
    else:
        score_part = fuzz.ratio(lst_part_a, lst_part_b) / 100.
    # 子字比较
    lst_atom_a = dict_char[char_a].get("has_atom", list()) if char_a in dict_char else list()
    lst_atom_b = dict_char[char_b].get("has_atom", list()) if char_b in dict_char else list()
    if char_b in lst_atom_a:
        score_atom = 1
    elif char_a in lst_atom_b:
        score_atom = 1
    else:
        score_atom = fuzz.ratio(lst_atom_a, lst_atom_b) / 100.
    score_final = 0.05*score_structure + 0.25*score_corner + 0.4*score_pinyin + 0.12*score_part + 0.18*score_atom
    return score_final


def run():
    """
    从各源文件中整合、清理、得到汉字三元组Excel文件。
    :return: None
    """
    print("Begin ...")
    d_part = create_part_dictionary()
    d_number = create_number_dictionary()
    d_char, d_pron = create_character_dictionary(d_part, d_number)
    _ = add_similar_char(d_char, is_save=True)
    json2triple(load_path="corpus/basic_dictionary_similar.json", save_path="corpus/basic_triple.xlsx")
    print("Finished.")
    return None


if __name__ == "__main__":
    run()
