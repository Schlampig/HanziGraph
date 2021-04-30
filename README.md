# HanziGraph
Visualization for information about Chinese characters via Neo4j.

## Intorduction:
I try to intergrate several open source Chinese characters or words corpora to build a visualized graph for these characters, motivated by the demand to deal with character-level similarity comparison, nlp data-augumentation, and curiosity (｡･ω･｡)ﾉ

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
  |-> corpus_handian -> word_handian: 现代汉语词典材料 (todo)
                    |-> get_handian.py (todo)
  |-> corpus_dacilin -> word_dacilin: 大词林材料 (todo)
                    |-> get_dacilin.py (todo)              
  |-> prepro.py
  |-> build_graph.py (todo)
  |-> text_augmentation.py  (todo)
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
* [**basic_triple.xlsx**](https://github.com/Schlampig/HanziGraph/blob/main/corpus/basic_triple.xlsx): a file in xlsx format has (head, relation, tail) triple in each row transformed from **basic_dictionary_similar.json**.
* **hanzi_entity.csv** and **hanzi_relation.csv**: two necessary files in csv format to build the graph in Neo4j, transformed from **basic_triple.xlsx** (todo).

<br>

## Command Line:
* **prepro**: this [code](https://github.com/Schlampig/HanziGraph/blob/main/prepro.py) is used to intergrate corpora into the large dictionary, and then transfor the dictionary to the triple-based data:
```bash
python prepro.py
```
* **build_graph**: this code(todo) is used to transfor the triple-based data into entity/relation-based data:
```bash
python build_graph.py
```
* **import data into Neo4j**: this code is used in command line to import entity/relation-based data to Neo4j:
```bash
./neo4j-import -into /your_path/neo4j-community-3.5.5/data/databases/graph.db/ --nodes /Users/schwein/neo4j-data/hanzi_entity.csv --relationships /Users/schwein/neo4j-data/hanzi_relation.csv --ignore-duplicate-nodes=true --ignore-missing-nodes=true
```
* **start up Neo4j**: open the browser, input the address http://localhost:7474/, check the graph:
```bash
./neo4j console
```

<br>

## Requirements
  * Python = 3.6.9
  * Neo4j = 3.5.5
  * pypinyin = 0.41.0
  * pandas = 0.22.0
  * fuzzywuzzy = 0.17.0
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

<br>

<img src="https://github.com/Schlampig/Knowledge_Graph_Wander/blob/master/content/daily_ai_paper_view.png" height=25% width=25% />

