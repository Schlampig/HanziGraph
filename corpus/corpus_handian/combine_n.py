import json
from tqdm import tqdm


def combine_handian_and_cilin(load_handian, load_cilin):
    # load
    with open(load_handian, "r") as f:
        d_handian = json.load(f)
    with open(load_cilin, "r") as f:
        d_cilin = json.load(f)
    # combine
    for k, d_k in tqdm(d_cilin.items()):
        if k not in d_handian.keys():
            d_handian[k] = d_k
        else:
            # combine synonym
            if len(d_handian[k]["synonym"]) == 0:
                d_handian[k]["synonym"] = d_k["synonym"]
            else:
                d_handian[k]["synonym"].extend(d_k["synonym"])
            d_handian[k]["synonym"] = list(set(d_handian[k]["synonym"]))
            # combine antonym
            if len(d_handian[k]["antonym"]) == 0:
                d_handian[k]["antonym"] = d_k["antonym"]
            else:
                d_handian[k]["antonym"].extend(d_k["antonym"])
            d_handian[k]["antonym"] = list(set(d_handian[k]["antonym"]))
    # save
    with open("corpus4n.json", "w") as f:
        json.dump(d_handian, f, ensure_ascii=False, indent=2)
    print("OK.")
    return None


if __name__ == "__main__":
    combine_handian_and_cilin("同义反义词/corpus4n_handian.json", "../kg/dacilin/corpus4n_cilin.json")