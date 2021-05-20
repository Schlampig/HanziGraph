import pandas as pd
from tqdm import tqdm


def map_rel(s):
    d_rel_map = {"has_atom": "包含子结构", "is_atom_of": "是其子结构",
                 "has_part": "包含偏旁", "is_part_of": "是其偏旁",
                 "has_pronunciation": "拼音", "is_pronunciation_of": "是其拼音",
                 "has_number": "笔画数", "is_number_of": "是其笔画数",
                 "has_simple": "简体形式", "is_simple_to": "是其简体形式",
                 "has_traditional": "繁体形式", "is_traditional_to": "是其繁体形式",
                 "similar_to": "近似字"}
    return d_rel_map.get(s, s)


def generate_entity_and_relation_tables(load_path):
    print("Check entities and relations ...")
    dict_entity = dict()
    lst_relation = list()
    df_triple = pd.read_excel(load_path)
    for i in tqdm(range(df_triple.shape[0])):
        head = df_triple.loc[i, "head"]
        relation = df_triple.loc[i, "relation"]
        tail = df_triple.loc[i, "tail"]
        # check type
        if relation == "has_number":
            head_type = "charactor"
            tail_type = "number"
        elif relation == "is_number_of":
            head_type = "number"
            tail_type = "charactor"
        elif relation == "has_pronunciation":
            head_type = "charactor"
            tail_type = "pronunciation"
        elif relation == "is_pronunciation_of":
            head_type = "pronunciation"
            tail_type = "charactor"
        else:
            head_type = "charactor"
            tail_type = "charactor"
        # check id
        if head not in dict_entity.keys():
            head_id = len(dict_entity) + 1
            dict_entity[head] = {":ID(node)": head_id, ":LABEL": head_type, "name": head}
        else:
            if head_type != dict_entity[head][":LABEL"]:
                head_id = len(dict_entity) + 1
                dict_entity[head] = {":ID(node)": head_id, ":LABEL": head_type, "name": head}
            else:
                head_id = dict_entity[head][":ID(node)"]
        if tail not in dict_entity.keys():
            tail_id = len(dict_entity) + 1
            dict_entity[tail] = {":ID(node)": tail_id, ":LABEL": tail_type, "name": tail}
        else:
            if tail_type != dict_entity[tail][":LABEL"]:
                tail_id = len(dict_entity) + 1
                dict_entity[tail] = {":ID(node)": tail_id, ":LABEL": tail_type, "name": tail}
            else:
                tail_id = dict_entity[tail][":ID(node)"]
        # add into entity & relation lists
        lst_relation.append({":START_ID(node)": head_id, ":END_ID(node)": tail_id,
                             ":TYPE": map_rel(relation), "name": map_rel(relation)})

    # create entity table
    print("Create Entity Table ...")
    lst_e_id, lst_e_name, lst_e_label = list(), list(), list()
    for _, e in dict_entity.items():
        if e.get(":ID(node)", None) and e.get("name", None) and e.get(":LABEL", None):
            lst_e_id.append(e.get(":ID(node)", None))
            lst_e_name.append(e.get("name", None))
            lst_e_label.append(e.get(":LABEL", None))
    df_entity = pd.DataFrame({":ID(node)": lst_e_id, "name": lst_e_name, ":LABEL": lst_e_label})
    df_entity = df_entity[[":ID(node)", "name", ":LABEL"]]
    df_entity.to_csv("hanzi_entity.csv", index=False, encoding="utf-8-sig")

    # create relation table
    print("Create Relation Table ...")
    lst_r_head, lst_r_tail, lst_r_type, lst_r_name = list(), list(), list(), list()
    for r in lst_relation:
        if r.get(":START_ID(node)", None) and r.get(":END_ID(node)", None) and r.get(":TYPE", None) and r.get("name", None):
            lst_r_head.append(r.get(":START_ID(node)", None))
            lst_r_tail.append(r.get(":END_ID(node)", None))
            lst_r_type.append(r.get(":TYPE", None))
            lst_r_name.append(r.get("name", None))
    df_relation = pd.DataFrame({":START_ID(node)": lst_r_head, ":END_ID(node)": lst_r_tail, ":TYPE": lst_r_type, "name":lst_r_name})
    df_relation = df_relation[[":START_ID(node)", ":END_ID(node)", ":TYPE", "name"]]
    df_relation.to_csv("hanzi_relation.csv", index=False, encoding="utf-8-sig")

    print("Finished.")
    return None


if __name__ == "__main__":
    generate_entity_and_relation_tables("corpus/basic_triple.xlsx")
