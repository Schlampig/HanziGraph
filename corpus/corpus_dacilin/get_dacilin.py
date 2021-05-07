import re
import json
from tqdm import tqdm


LST_REL = ["别名", "别称", "简称", "同义词", "本名", "艺名", "又称", "又名", "全称", "全名", "其他名称", "中文学名",
           "学名", "古称", "其他译名", "俗称", "旧称", "中文简称", "亦称", "昵称", "另名", "泛称", "其他称呼", "【别 名】",
           "真名", "曾用名", "古时称", "笔名", "俗名", "也称", "又称为", "美称", "网名", "现名", "小名", "代称", "雅称",
           "自称", "上古称谓", "现今称谓", "同类称谓", "中古称谓", "署名", "也称为", "通用名", "同名", "同义", "尊称",
           "现称", "中文别名", "化学名", "病名", "同义词", "或称", "曾译名", "人称", "其他名字", "同称", "原称", "爱称",
           "始称", "另称", "乃称", "改称", "原名", "又被称为", "称之为", "后世尊称", "谦称", "今名", "素称", "谐称",
           "亦名", "号称", "译名", "曾称", "概念全称", "美名", "世称", "医学称呼", "一般称为", "化名", "同义旧称", "曾名",
           "别名名称", "明代称", "清代称", "中文全名", "小名", "药名", "谥称", "简称", "更名后"]
LST_REL = list(set(LST_REL))
DICT_REL = {k: True for k in LST_REL}


def check_relation(load_path):
    """
    观察大词林中出现的关系种类。
    :param load_path: triple.txt, 大词林三元组数据集
    :return: None, 以打印方式呈现
    """
    with open(load_path, "r") as f:
        lst_rel = list()
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            line_split = line.split(";")
            if len(line_split) == 3:
                relation = line_split[1]
                if "名" in relation or "称" in relation or "同义" in relation:
                    if relation not in lst_rel:
                        lst_rel.append(relation)
    for rel in lst_rel:
        print(rel)
    return None


def clean_entity(s):
    """
    清洗大词林中的实体，例如切分开多个并列的实体，去除多余的字或符号等。
    :param s: string, 当前实体
    :return: lst_s = [entity_1, entity_2, ...], 干净实体（可能有多个）
    """
    lst_s = list()
    s = s.lower()
    s = re.sub("[\[(（【]", "[", s)
    if "[" in s:
        s = s.split("[")[0]
    s = re.sub("\s+", ",", s)
    s = re.sub("[，,、；;./\\\\]", ",", s)
    if re.search("[,]+", s) and "等" in s[-1]:
        s = s.rstrip("等")
    s = s.rstrip("……")
    for w in s.split(","):
        w = w.strip()
        w = w.replace("“", "").replace("”", "")
        if len(w) > 1:  # delete word with single char
            if re.search("[a-z]+", w):
                if len(re.search("[a-z]+", w).group()) < len(w):
                    lst_s.append(w)
            else:
                lst_s.append(w)
    return lst_s


def get_dacilin(load_path):
    """
    根据大词林三元组数据生成名词的近/反义词的json数据集。
    :param load_path: triple.txt, 大词林三元组数据集
    :param save_path: corpus4n_cilin.json, 大词林名词近义/反义词数据集（其实没有反义词，但格式是统一的）
    :return: None
    """
    global DICT_REL
    print("Find Synonym ...")
    with open(load_path, "r") as f:
        dict_synonym = dict()
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            line_split = line.split(";")
            if len(line_split) == 3:
                head, relation, tail = line_split[0], line_split[1], line_split[2]
                if len(relation) > 0 and len(head) > 0 and len(tail) > 0:
                    relation = re.sub("\s+", "", relation)
                    if relation in DICT_REL.keys():
                        heads = clean_entity(head)
                        tails = clean_entity(tail)
                        for h in heads:
                            for t in tails:
                                if (h not in t) and (t not in h):
                                    if h in dict_synonym.keys():
                                        if t not in dict_synonym[h]:
                                            dict_synonym[h].append(t)
                                    else:
                                        dict_synonym[h] = [t]
    # format finetune
    print("Format Fine-tune ...")
    d_n_new = dict()
    for k, lst_v in tqdm(dict_synonym.items()):
        if k not in d_n_new.keys():
            d_n_new[k] = {"synonym": lst_v, "antonym": list()}
        else:
            d_n_new[k]["synonym"] += lst_v
            d_n_new[k]["synonym"] = list(set(d_n_new[k]["synonym"]))
        for v in lst_v:
            lst_v_neighbor = [neighbor for neighbor in lst_v if neighbor != v]
            lst_v_neighbor.append(k)
            lst_v_neighbor = list(set(lst_v_neighbor))
            if v not in d_n_new.keys():
                d_n_new[v] = {"synonym": lst_v_neighbor, "antonym": list()}
            else:
                d_n_new[v]["synonym"] += lst_v_neighbor
                d_n_new[v]["synonym"] = list(set(d_n_new[v]["synonym"]))
    # save
    print("Save data...")
    with open("corpus4n_cilin.json", "w") as f:
        json.dump(d_n_new, f, ensure_ascii=False, indent=2)
    return None


if __name__ in "__main__":
    # check_relation(load_path="word_dacilin/triple.txt")
    get_dacilin(load_path="word_dacilin/triple.txt")
