import os
import re
import json
from collections import Counter
from tqdm import tqdm


def txt2json(load_path):
    """
    生成现代汉语词典json格式的数据，只保留动词、名词、形容词、副词。
    :param load_path: handian.txt, 现代汉语词典txt数据
    :return: handian.json, 现代汉语词典只保留动词、名词、形容词、副词的json数据
    """
    lst_len = list()
    with open(load_path, "r") as f:
        d_all = dict()
        for line in f.readlines():
            line = re.sub("\s+", "", line)
            lst_pos = re.findall("〈([动名形副])〉", line)
            if len(lst_pos) > 0:
                if re.search("【.+?】", line):
                    word = re.search("【.+?】", line).group()
                    word = word.strip("【】")
                    lst_len.append(len(word))
                lst_pos = list(set(lst_pos))
                if len(word) > 1:
                    d_all.update({word: {"pos": lst_pos}})
    save_path = load_path.replace(".txt", ".json")
    with open(save_path, "w") as f:
        json.dump(d_all, f, ensure_ascii=False, indent=2)
    print("词长及该词长的词数为： ", Counter(lst_len))
    print("词汇量：", len(d_all))
    return None


# NOTE: 省略根据handian.json获取里面每个词的基础释义与维基释义的爬虫脚本: handian.json -> handian_crawl.json


def json2corpus(load_path, save_dir=""):
    """
    现代汉语词典只保留动词、名词、形容词、副词的json数据按词性分存。
    :param load_path: handian_crawl.json, 整合动、名、形、副近义/反义词的json数据
    :param save_dir: 动、名、形、副近义/反义词各自json数据的存储路径
    :return: corpus4x.json, 动、名、形、副近义/反义词各自的json数据
    """
    dict_n, dict_v, dict_adj, dict_adv = dict(), dict(), dict(), dict()
    with open(load_path, "r") as f:
        dict_char = json.load(f)
        for char, char_info in dict_char.items():
            if "动" in char_info["pos"]:
                if len(char_info["antonym"]) > 0 or len(char_info["synonym"]) > 0:
                    dict_v.update({char: {"antonym": char_info["antonym"], "synonym": char_info["synonym"]}})
            if "形" in char_info["pos"]:
                if len(char_info["antonym"]) > 0 or len(char_info["synonym"]) > 0:
                    dict_adj.update({char: {"antonym": char_info["antonym"], "synonym": char_info["synonym"]}})
            if "副" in char_info["pos"]:
                if len(char_info["antonym"]) > 0 or len(char_info["synonym"]) > 0:
                    dict_adv.update({char: {"antonym": char_info["antonym"], "synonym": char_info["synonym"]}})
            if "名" in char_info["pos"]:
                dict_n.update({char: char_info})
    with open(os.path.join(save_dir, "corpus4v.json"), "w") as f:
        json.dump(dict_v, f, ensure_ascii=False, indent=2)
    with open(os.path.join(save_dir, "corpus4adj.json"), "w") as f:
        json.dump(dict_adj, f, ensure_ascii=False, indent=2)
    with open(os.path.join(save_dir, "corpus4adv.json"), "w") as f:
        json.dump(dict_adv, f, ensure_ascii=False, indent=2)
    with open(os.path.join(save_dir, "corpus4n_raw.json"), "w") as f:
        json.dump(dict_n, f, ensure_ascii=False, indent=2)
    print("OK.")
    return None


####################################################################################################
def clean_n(s):
    lst_s = list()
    for c in s.split("、"):
        c = c.strip("“”")
        if len(c) > 0:
            if c[0] in ["对", "是", "指", "作"]:
                c = c[1:]
                if len(c) > 0:
                    lst_s.append(c)
            else:
                lst_s.append(c)
    return lst_s


def find_noun_basic(s):
    """
    从名词的basic定义中找出定义类描述，抽取该描述短语/词汇作为当前名词的同义词。
    :param s: string, 输入的名词描述
    :return: list, 该名词的同义短语/词汇
    """
    lst_n = list()
    if isinstance(s, str) and len(s) > 0:
        s = re.sub("\s+", "", s)
        if re.search("(?<=又称为)\w+?(?=[，。；：（])", s):
            n = clean_n(re.search("(?<=又称为)\w+?(?=[，。；：（])", s).group())
            if len(n) > 0:
                lst_n += n
        if re.search("(?<=简称为)\w+?(?=[，。；：（])", s):
            n = clean_n(re.search("(?<=简称为)\w+?(?=[，。；：（])", s).group())
            if len(n) > 0:
                lst_n += n
        if re.search("(?<=也叫)\w+?(?=[，。；：（])", s):
            n = clean_n(re.search("(?<=也叫)\w+?(?=[，。；：（])", s).group())
            if len(n) > 0:
                lst_n += n
        if re.search("(?<=意指)\w+?(?=[，。；：（])", s):
            n = clean_n(re.search("(?<=意指)\w+?(?=[，。；：（])", s).group())
            if len(n) > 0:
                lst_n += n
        if re.search("(?<=泛指)\w+?(?=[，。；：（])", s):
            n = clean_n(re.search("(?<=泛指)\w+?(?=[，。；：（])", s).group())
            if len(n) > 0:
                lst_n += n
        if re.search("(?<=[对是指作])\w+?(?=的简称[，。；：（])", s):
            n = clean_n(re.search("(?<=[对是指作])\w+?(?=的简称[，。；：（])", s).group())
            if len(n) > 0:
                lst_n += n
        if re.search("(?<=[对是指作])\w+?(?=的别称[，。；：（])", s):
            n = clean_n(re.search("(?<=[对是指作])\w+?(?=的别称[，。；：（])", s).group())
            if len(n) > 0:
                lst_n += n
        if re.search("(?<=[对是指作])\w+?(?=的称呼)", s):
            n = clean_n(re.search("(?<=[对是指作])\w+?(?=的称呼)", s).group())
            if len(n) > 0:
                lst_n += n
        if re.search("(?<=[对是指作])\w+?(?=的尊称)", s):
            n = clean_n(re.search("(?<=[对是指作])\w+?(?=的尊称)", s).group())
            if len(n) > 0:
                lst_n += n
        if re.search("(?<=[对是指作])\w+?(?=的通称)", s):
            n = clean_n(re.search("(?<=[对是指作])\w+?(?=的通称)", s).group())
            if len(n) > 0:
                lst_n += n
        if re.search("(?<=见〖)\w+?(?=〗)", s):
            n = clean_n(re.search("(?<=见〖)\w+?(?=〗)", s).group())
            if len(n) > 0:
                lst_n += n
        if re.search("(?<=又叫)\w+?(?=[，。；：（等])", s):
            n = clean_n(re.search("(?<=又叫)\w+?(?=[，。；：（等])", s).group())
            if len(n) > 0:
                lst_n += n
        if re.search("(?<=又叫作)\w+?(?=[，。；：（等])", s):
            n = clean_n(re.search("(?<=又叫作)\w+?(?=[，。；：（等])", s).group())
            if len(n) > 0:
                lst_n += n
    return lst_n


def find_noun_wiki(s):
    """
        从名词的wiki定义中找出定义类描述，抽取该描述短语/词汇作为当前名词的同义词。
        :param s: string, 输入的名词描述
        :return: list, 该名词的同义短语/词汇
        """
    lst_n = list()
    if isinstance(s, str) and len(s) > 0:
        s = re.sub("\s+", "", s)
        if re.search("(?<=意思是)\w+?(?=[，。；：（])", s):
            n = clean_n(re.search("(?<=意思是)\w+?(?=[，。；：（])", s).group())
            if len(n) > 0:
                lst_n += n
        if re.search("(?<=专指)\w+?(?=[，。；：（])", s):
            n = clean_n(re.search("(?<=专指)\w+?(?=[，。；：（])", s).group())
            if len(n) > 0:
                lst_n += n
        if re.search("(?<=原指)\w+?(?=[，。；：（])", s):
            n = clean_n(re.search("(?<=原指)\w+?(?=[，。；：（])", s).group())
            if len(n) > 0:
                lst_n += n
        if re.search("(?<=解释为)\w+?(?=[，。；：（])", s):
            n = clean_n(re.search("(?<=解释为)\w+?(?=[，。；：（])", s).group())
            if len(n) > 0:
                lst_n += n
        if re.search("(?<=指)\w+?(?=[，。；：（])", s):
            n = clean_n(re.search("(?<=指)\w+?(?=[，。；：（])", s).group())
            if len(n) > 0:
                lst_n += n
    return lst_n


def get_new_noun(load_path):
    """
    基于基础释义与维基释义，生成精准的名词近义/反义词json数据。
    :param load_path: corpus4n_raw.json, 名词的近义/反义/基础释义/维基释义json数据
    :return: corpus4n_handian.json, 名词的近义/反义json数据（基础释义与维基释义已整合入近义/反义中）
    """
    count_word = 0
    dict_n_new = dict()
    with open(load_path, "r") as f:
        dict_n = json.load(f)
        for word, word_info in tqdm(dict_n.items()):
            basic_mean = word_info.get("basic_mean")
            wiki_mean = word_info.get("wiki_mean")
            lst_synonym = word_info.get("synonym")
            for mean in basic_mean:
                lst_mean = find_noun_basic(mean)
                lst_synonym += lst_mean
            for mean in wiki_mean:
                lst_mean = find_noun_wiki(mean)
                lst_synonym += lst_mean
            lst_synonym = list(set(lst_synonym))
            lst_synonym = [w for w in lst_synonym if w != word]
            # update new dictionary
            lst_antonym = word_info.get("antonym", list())
            if len(lst_synonym) > 0 or len(lst_antonym) > 0:
                dict_n_new.update({word: {"synonym": lst_synonym, "antonym": lst_antonym}})
                count_word += 1
                for neighbor in lst_synonym:
                    lst_neighbor = [w for w in lst_synonym if w != neighbor]
                    lst_neighbor += [word]
                    dict_n_new.update({neighbor: {"synonym": lst_neighbor, "antonym": lst_antonym}})
                    count_word += 1
    save_path = load_path.replace("_raw.json", "_handian.json")
    with open(save_path, "w") as f:
        json.dump(dict_n_new, f, ensure_ascii=False, indent=2)
    print("Collect {} noun with synonym and antonym.".format(count_word))
    return None


if __name__ == "__main__":
    # txt2json(load_path="word_handian/handian.txt")
    # json2corpus(load_path="word_handian/handian_crawl.json", save_dir="")
    get_new_noun(load_path="word_handian/corpus4n_raw.json")
