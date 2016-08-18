import re
import nltk
import glob
from nltk.stem.lancaster import LancasterStemmer
from nltk.parse import stanford
parser = stanford.StanfordParser()
st = LancasterStemmer()

def tokens_ids_anno(filename):
    with open(filename) as f:
        doc = f.readlines()
        result =[]
        sent = {}
        sent['tokens'] = []
        for line in doc:
            if line.startswith('#'):
                continue
            elif len(line) == 1:
                result.append(sent)
                sent = {}
                sent['tokens'] = []
            else:
                splitted_line = re.split("\t", line)
                splitted_line.remove("\n")
                sent['tokens'].append(splitted_line)
        return result

def nltk_process(result):
    for sent in result:
        sent['ner'] = []
        tokens = []
        stems = []
        for word in sent['tokens']:
            tokens.append(word[1])
            stem = st.stem(word[1])
            stems.append(stem)
        pos = nltk.pos_tag(tokens)
        parsed = parser.tagged_parse(pos)
        sent['parse'] = treetodict(parsed.next())
        for i in range(0,len(sent['tokens'])):
            sent['tokens'][i].append(pos[i][1])
        entities = nltk.chunk.ne_chunk(pos)
        for i in range(0, len(entities)):
            if isinstance(entities[i], nltk.tree.Tree):
                sent['ner'].append(treetodict(entities[i]))
        for i in range(0, len(sent['tokens'])):
            sent['tokens'][i].append(stems[i])
    return result

def treetodict(tree):
    dict1 = {}
    dict1['label'] = tree.label()
    dict1['children'] = []
    for i in range(0, len(tree)):
        if isinstance(tree[i], nltk.tree.Tree):
            dict1['children'].append(treetodict(tree[i]))
        else:
            dict1['children'].append(tree[i])
    return dict1
    
            
            
def main():
        list_of_files = glob.glob("original/*")
        print list_of_files
        for one_file in list_of_files:
            filename = re.sub(r"original", "", one_file)
            with open("preprocessed"+filename+".dict", "w") as fout:
                result_list = tokens_ids_anno(one_file)
                nltk_result = nltk_process(result_list)
                fout.write(str(nltk_result))


if __name__ == '__main__':
    main()
