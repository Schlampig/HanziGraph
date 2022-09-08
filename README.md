# HanziGraph

<br>

[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)
[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)

Visualization for information about Chinese characters via Neo4j & Text augmentation via Chinese characters and words (typos, synonym, antonym, similar entity, numeric, etc.).

## Introduction:
- I try to intergrate several open source Chinese characters or words corpora to build a visualized graph, named **HanziGraph**, for these characters, motivated by the demand to deal with character-level similarity comparison, nlp data-augumentation, and curiosity (｡･ω･｡)ﾉ 

- Furthermore, a light **Chinese Text Augmentation** code is provided based on several clean word-level corpora integrated by myself from open-source datasets like The Contemporary Chinese Dictionary and BigCilin.

<br>

## File Dependency:
```
-> corpus -> char_number: 汉字笔画材料
         |-> char_part: 汉字偏旁材料
         |-> char_pronunciation: 汉字拼音材料
         |-> char_similar: 汉字结构分类、四角编码信息、形近字、音近字材料
         |-> char_split: 汉字拆字、简繁字体对照材料
         |-> basic_dictionary_similar.json
         |-> basic_triple.xlsx
         |-> corpus_handian -> word_handian: 现代汉语词典材料、生成的json数据
                           |-> get_handian.py  # 处理汉典数据的脚本
                           |-> combine_n.py  # 合并汉典与词林名词数据的脚本
         |-> corpus_dacilin -> word_dacilin: 大词林材料、生成的json数据
                           |-> get_dacilin.py  # 处理词林数据的脚本
  |-> prepro.py  # 预处理汉字各数据集的脚本
  |-> build_graph.py  # 生成汉字图谱的脚本
  |-> text_augmentation.py  # 利用词典扩增文本的脚本
```

<br>

## Dataset
* [**basic_dictionary_similar.json**](https://github.com/Schlampig/HanziGraph/blob/main/corpus/basic_dictionary_similar.json): a file in json format to store a large dictionary, where each entry has the same data structure below:
```
entry (i.e. each character) = {
                               "split_to(拆字方案)": ["part(偏旁) atom(子字) ...", ...],
                               "has_atom(包含哪些子字)": [atom(子字), ...],
                               "is_atom_of(为哪些字的子字)": [char(字), ...],
                               "has_part(包含哪些偏旁部首)": [part(偏旁), ...],
                               "is_part_of(为哪些字的偏旁部首)": [char(字), ...],
                               "pronunciation(有哪些读音)": [pronunciation(带音调拼音), ...],
                               "number(笔画数)": number(笔画数),
                               "is_simple_to(是哪些繁体的简体形式)": [char(字), ...],
                               "is_traditional_to(是哪些简体的繁体形式)": [char(字), ...],
                               "similar_to(有哪些近似字)": [char(字), ...]
                               }
```
* [**basic_triple.xlsx**](https://github.com/Schlampig/HanziGraph/blob/main/corpus/basic_triple.xlsx): a file in xlsx format has (head, relation, tail) triple in each row transformed from [**basic_dictionary_similar.json**](https://github.com/Schlampig/HanziGraph/blob/main/corpus/basic_dictionary_similar.json).
* **hanzi_entity.csv** and **hanzi_relation.csv**: two necessary files in csv format to build the graph in Neo4j, transformed from [**basic_triple.xlsx**](https://github.com/Schlampig/HanziGraph/blob/main/corpus/basic_triple.xlsx), too large to upload here.
* [**corpus4n**](https://github.com/Schlampig/HanziGraph/blob/main/corpus/corpus_handian/word_handian/corpus4n.json), [**corpus4v**](https://github.com/Schlampig/HanziGraph/blob/main/corpus/corpus_handian/word_handian/corpus4v.json), [**corpus4adj**](https://github.com/Schlampig/HanziGraph/blob/main/corpus/corpus_handian/word_handian/corpus4adj.json), [**corpus4adv**](https://github.com/Schlampig/HanziGraph/blob/main/corpus/corpus_handian/word_handian/corpus4adv.json), [**corpus4typos**](https://github.com/Schlampig/HanziGraph/blob/main/corpus/corpus_handian/word_handian/corpus4typos.json) are dictionary in .json format for text augmentation function.

<br>

## Command Line:
* **prepro**: this [code](https://github.com/Schlampig/HanziGraph/blob/main/prepro.py) is used to intergrate corpora into the large dictionary, and then transfor the dictionary to the triple-based data:
```bash
python prepro.py
```
* **build_graph**: this [code](https://github.com/Schlampig/HanziGraph/blob/main/build_graph.py) is used to transfor the triple-based data into entity/relation-based data:
```bash
python build_graph.py
```
* **import data into Neo4j**: this code is used in command line to import entity/relation-based data to Neo4j:
```bash
./neo4j-import -into /your_path/neo4j-community-3.5.5/data/databases/graph.db/ --nodes /your_path/hanzi_entity.csv --relationships /your_path/hanzi_relation.csv --ignore-duplicate-nodes=true --ignore-missing-nodes=true
```
* **start up Neo4j**: open the browser, input the address http://localhost:7474/, check the graph:
```bash
./neo4j console
```
* **generate dictionaries for text augmentation**: using functions from [**get_handian.py**](https://github.com/Schlampig/HanziGraph/blob/main/corpus/corpus_handian/get_handian.py) and [**get_dacilin.py**](https://github.com/Schlampig/HanziGraph/blob/main/corpus/corpus_dacilin/get_dacilin.py), and function **create_corpus4typos** in [**prepro.py**](https://github.com/Schlampig/HanziGraph/blob/main/prepro.py) to generate dictionaries for text augmentation.

* **text augmentation**: using functions in this [code](https://github.com/Schlampig/HanziGraph/blob/main/text_augmentation.py) to generate new samples. Run the code to see examples. The detailed design method could be found [here](https://github.com/Schlampig/HanziGraph/blob/main/corpus/corpus_handian/README.md).
```bash
python text_augmentation.py
```

<br>

## Requirements
  * Python = 3.6.9
  * Neo4j = 3.5.5
  * pypinyin = 0.41.0
  * pandas = 0.22.0
  * fuzzywuzzy = 0.17.0
  * [LTP 4](https://github.com/HIT-SCIR/ltp)
  * tqdm = 4.39.0

<br>

## References
  * [pinyin-data](https://github.com/mozillazg/pinyin-data)、[phrase-pinyin-data](https://github.com/mozillazg/phrase-pinyin-data)、[pypinyin](https://pypi.org/project/pypinyin/) by Huang Huang.
  * [语言文字规范标准](http://www.moe.gov.cn/s78/A19/A19_ztzl/ztzl_yywzgfbz/) from 国家语言文字信息管理司.
  * [SimilarCharacter](https://github.com/contr4l/SimilarCharacter) by XiaoFang.
  * [CharMap](https://github.com/guo-yong-zhi/CharMap) by guo-yong-zhi.
  * [漢語拆字字典](https://github.com/kfcd/chaizi) by 開放詞典(kfcd).
  * [funNLP](https://github.com/fighting41love/funNLP) by Yang fighting41love.
  * [《现代汉语词典》（第7版）](https://github.com/CNMan/XDHYCD7th) by CNMan.
  * [chinese-xinhua 中华新华字典数据库](https://github.com/pwxcoo/chinese-xinhua) by Xiance Wu.
  * [CJKV (Chinese Japanese Korean Vietnamese) Ideograph Database](https://github.com/cjkvi) by CJKVI.

:book: [See more ...](https://github.com/Schlampig/Knowledge_Graph_Wander/blob/master/content/Dictionary.md)
<br>

## Cite this work as:
  * Chen J., He Z., Zhu Y., Xu L. (2021) [TKB<sup>2</sup>ert: Two-Stage Knowledge Infused Behavioral Fine-Tuned BERT](https://link.springer.com/chapter/10.1007/978-3-030-88483-3_35). In: Wang L., Feng Y., Hong Y., He R. (eds) Natural Language Processing and Chinese Computing. NLPCC 2021. Lecture Notes in Computer Science, vol 13029. Springer, Cham. https://doi.org/10.1007/978-3-030-88483-3_35
<br>

## Use Case
  * [2021语言与智能技术竞赛(2021 Language and Intelligence Challenge, LIC2021)](http://lic2021.ccf.org.cn/).
  * [2021 CCF BDCI 千言-问题匹配鲁棒性评测](https://aistudio.baidu.com/aistudio/competition/detail/116/0/introduction).

<br>
<img src="https://github.com/Schlampig/Knowledge_Graph_Wander/blob/master/content/daily_ai_paper_view.png" height=25% width=25% />

