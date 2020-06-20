import math
import porter2stemmer
import sys
import importlib
from nltk.corpus import RegexpTokenizer  # split a string into substrings using a regular expression
importlib.reload(sys)


def get_list(text):  # Tokenize each string and change to normalize
    list1 = RegexpTokenizer(r'\w+|\$[\d\.]+|\S+')
    list1_text = list1.tokenize(str(text))
    temp = []
    for lis in list1_text:
        lis = lis.lower()
        temp.append(lis)
    return temp


def snowball(list2):  # Change the string to the base form
    temp = []
    ps = porter2stemmer.Porter2Stemmer()
    list2 = remove_metadata(list2)
    for lis in list2:
        flag = ps.stem(lis)
        flag = str(flag)
        temp.append(flag)
    return temp


def create_index(process, temp, dictionary):  # Calculate each term-frequency in a single document
    for lis in process:
        if lis not in dictionary:
            dictionary[lis] = {}
            dictionary[lis][temp] = 1.0
        if temp not in dictionary[lis]:
            dictionary[lis][temp] = 1.0
        dictionary[lis][temp] += 1.0
    return dictionary


def tfidf(query):  # Calculate the tf-idf scores for each query
    dict = {}
    for lis in query:
        if lis not in dict:
            dict[lis] = 1.0
        dict[lis] += 1.0
    return dict


def vector_tfidf(dictionary, number_of_document):  # find the idf score for words in the document and update the existing tf-idf values
    idf = {}
    for word in dictionary:
        idf[word] = len(dictionary[word].keys())
    for word in dictionary:
        for document in dictionary[word]:
            dictionary[word][document] = (1.0 + math.log(dictionary[word][document])) * math.log(number_of_document / idf[word])
    return dictionary, idf


def caculate_tfidf(dict, idf, number_of_document):  # find the tf-idf value for the word in the search query to update the existing tf-idf values
    for word in dict:
        dict[word] = (1.0 + math.log(dict[word])) * math.log(number_of_document / idf[word])
    return dict


def remove_metadata(line):  # remove spammy meta keywords from search engine
    global start
    start = 0
    for i in range(len(line)):
        if line[i] == '\n':
            start = i + 1
            break
    new_line = line[start:]
    return new_line