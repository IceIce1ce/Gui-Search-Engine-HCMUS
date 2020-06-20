from nltk.corpus import wordnet as wn


def query(process):  # Create a new search query that is relevant to the old query
    temp = []
    for lis in process:
        syn = wn.synsets(lis)
        res = [r.name().split('.')[0] for r in syn]
        if len(res) >= 2:
            res = res[:2]
        res.append(lis)
        for re in res:
            temp.append(re)
    return temp


synonyms = []
antonyms = []
for syn in wn.synsets("good"):  # search for synonyms and antonyms
    for lem in syn.lemmas():
        synonyms.append(lem.name())
        if lem.antonyms():
            antonyms.append(lem.antonyms()[0].name())
# print(set(synonyms))
# print(set(antonyms))