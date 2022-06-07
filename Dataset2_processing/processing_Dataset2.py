import re, math
import spacy
from scipy import   spatial

import analyze_date
import convert_int_to_string
from Dataset2_processing import get_query, get_doc
import normalize_doc
from Dataset2_processing import processing_Query,reading_RLE


nlp = spacy.load(r'C:\Users\Ammar\AppData\Local\Programs\Python\Python310\Lib\site-packages\en_core_web_sm\en_core_web_sm-3.3.0')
nlp2 = spacy.load(r'C:\Users\Ammar\AppData\Local\Programs\Python\Python310\Lib\site-packages\en_core_web_lg\en_core_web_lg-3.3.0')

import lemmatization
from Dataset2_processing.get_doc import get_current_doc
import stemming

import vectorMath


def find_revelance_documents(queryVector,diction):
    result={}
    for key_dic in diction:
        value_dic = diction[key_dic]
        vector = list(value_dic.values())
        vector2=list(value_dic.keys())
        #print("keays",vector2)
        #print("vector=",vector)
        result.update({key_dic: vectorMath.get_corner_between_tow_vector(queryVector, vector)})
    return result
def get_similarity(query_embadding,diction_embadding):
    result = {}
    count = 0.0
    similarity = 0.0
    cosine_similarity = lambda x, y: 1 - spatial.distance.cosine(query_embadding, diction_embadding)
    for key_dic in diction_embadding:
        value_dic = diction_embadding[key_dic]
        vector_key = list(value_dic.keys())
        #print("vector_key",vector_key)
    for word in vector_key:
        new_vector_key_embadding = nlp2.vocab[word].vector
        similarity_for_each_word = cosine_similarity(new_vector_key_embadding, nlp2.vocab[query_embadding].vector)
        count += similarity_for_each_word
    similarity = count/len(vector_key)
       # similarity = count/len(vector_key)
    print(f"similarity {key_dic}",similarity)
       # computed_similarity.append((query_embadding,similarity))
    result.update({key_dic:similarity})
    return result
def get_similarity2(query,diction):
    dic = {}
    text= '\n'.join(query)
    query_embadding = list(nlp(text).vector)
    print(query_embadding)
    #text = ' '.join(query_embadding)
    print("text",text)
    for key_dic in diction:
        value_dic = diction[key_dic]
        vector_key = list(value_dic.keys())
        #print("vector",vector_key)
        #print("query",query)
        #for vector in vector_key:
        text2 = '\n'.join(vector_key)
        diction_embadding = list(nlp(text2).vector)
        #query_embadding = nlp2.vocab[query].vector
        #diction_embadding = nlp2.vocab[vector_key].vector
        result = 1 - spatial.distance.cosine(query_embadding, diction_embadding)
        dic.update({key_dic: result})
    #print("diction",diction_embadding)
    return dic








def get_vector():
    #after_process_query = processing_Query.query_process()
    tokines = []  # contain all terms for all docs
    termsInAfile = []  # this contains all terms in (current file) without stop words
    diction = {}  # dictionary for all tokens
    reslist = {}
    sortdoc = {}
    doc = {}
    doc_embadding = []
    query_embadding = []
    result_query = []
    reciprocal_rank = 0
    total_rr = 0
    avg = 0
    for q in range(1,4):
        current_query = get_query.get_current_query(q)
        print("current_query",current_query)
        after_process_query = processing_Query.query_process(current_query)
        print("agter peocess query::=",after_process_query)
        for x in range(1, 500):
            # f = open("corpus/dataset2/{}.text".format(x), "r")
            # contentAFile = f.read()
            # f.close()
            contentAFile = get_doc.get_current_doc(x)




            contentAFile = contentAFile.lower()

            contentAFile = normalize_doc.do_normalize(contentAFile)

            contentAFile = analyze_date.do_findDate(contentAFile)


            ################################################################################
            verbs=lemmatization.lemmatiz_for_verb(contentAFile)
            nouns=stemming.nouns_stemming(contentAFile)
            termsInAfile.extend(verbs)
            termsInAfile.extend(nouns)

            text_doc = ' '.join(termsInAfile)
            text_query = ' '.join(after_process_query)
            doc_embadding = list(nlp2(text_doc).vector)
            query_embadding = list(nlp2(text_query).vector)
            result = 1 - spatial.distance.cosine(doc_embadding, query_embadding)
            if result > 0.5:
                doc.update({x: result})
            # print("result_term with query::", result)
            # array_doc.append((x,result))

            for w in termsInAfile:
                 if w not in tokines:
                     tokines.append(w)

            temp_dic = {}  # dictionary for each term
            for y in termsInAfile:
             temp_dic.update({y: (1 + math.log(termsInAfile.count(y), 10)).__round__(5)})
            # print("temp_doc=",temp_dic)

            diction.update({x: temp_dic})
            # print("dictionary",diction)
            print("document number : {} Done".format(x))
            termsInAfile.clear()

        print("document::", doc)
        reslist = sorted(doc.items(), key=lambda item: -item[1])
        #print("reslost", reslist)
        sortdoc = dict(reslist)
        # print("sorted",sortdoc)
        array_for_precision = []
        c = 0
        for r in sortdoc:
            c += 1
            result_query.append(r)
            if c == 10:
                break
            print("num of query", q, "result_query", result_query)
        print("doc", doc)
        print("sort_doc", sortdoc)
        print("doc", doc)
        lenght_of_doc = len(doc)
        lenght_of_result_query = len(result_query)
        print("lenght_of_doc", lenght_of_doc)
        print("sort_doc", sortdoc)
        count_pre_recall = 0
        for i in sortdoc:
            array_for_precision.append(i)
        print("array_for_precision", array_for_precision)
        string = convert_int_to_string.convert(result_query)
        print("string::=", string)
        sortdoc.clear()
        result_query.clear()
        doc.clear()
        mapping = reading_RLE.read_mappings()
        print("mapping value::", mapping['1'])
        count_pr10 = 0
        map_index = mapping[str(q)]
        print("map_index", map_index)
        for i in string:
            if i in map_index:
                count_pr10 = count_pr10 + 1
        print("count", count_pr10)
        array_for_precision_to_string = convert_int_to_string.convert(array_for_precision)
        for i in array_for_precision_to_string:
            if i in map_index:
                count_pre_recall += 1
        print("count_pre_recall", count_pre_recall)
        precision = 0.0
        recall = 0.0
        precision10 = 0.0
        precision = float(count_pre_recall) / float(lenght_of_doc)
        print("precision", precision)
        avg += precision
        recall = float(count_pre_recall) / float(len(map_index))
        print("recall", recall)
        precision10 = float(count_pr10) / float(lenght_of_result_query)
        print("precision@10", precision10)
        for i, d in enumerate(string):
            if d in map_index:
                reciprocal_rank = 1 / (i + 1)
                print("reciprocal_rank", reciprocal_rank, "i=", i)
                total_rr += reciprocal_rank
                print("total_rr", total_rr)
                break
    MAP = avg / 4
    print("MAP", MAP)
    MAA = total_rr / 4
    print("MAA=", MAA)
    for a in range(1, 500):
         temp_dic2 = diction.get(a).copy()
         diction.get(a).clear()
            # print(temp_dic2)
            # for y in list(dict.fromkeys(tokines)):
         for y in tokines:
            if y not in temp_dic2.keys():
                 diction.get(a).update({y: 0.0})
            else:
                diction.get(a).update({y: temp_dic2[y]})

            # print("query_doc",query_doc)

    f1 = open("vector model.txt", "w")
    f1.write(str(diction))
    f1.close()

    f2 = open("terms.txt", "w")
    f2.write(str(tokines))
    f2.close()
    print(len(tokines))

    #print("sorted_doc",sortdoc)
    #print("query_doc_",query_doc)
    return diction





    #or a, d in reslist:
         #   print(f'num {a} , hsa_similarity {b}')
        #for a, b in query_doc:
         #   print(f'num {a} , with doc {b}')





