import re
import spacy

from Dataset1_processing.reading_Dataset1 import read_documents1
from Dataset1_processing.reading_Query1 import read_queries1
from Dataset2_processing import calculate_evaluation_before_word, processing_Dataset2, reading_Query
from Dataset2_processing.reading_Query import read_queries2

nlp = spacy.load(r'C:\Users\Ammar\AppData\Local\Programs\Python\Python310\Lib\site-packages\en_core_web_sm\en_core_web_sm-3.3.0')
nlp2 = spacy.load(r'C:\Users\Ammar\AppData\Local\Programs\Python\Python310\Lib\site-packages\en_core_web_lg\en_core_web_lg-3.3.0')

from nltk import WordNetLemmatizer
from nltk.stem import PorterStemmer #for the first question
import ast,math
from tkinter import *
import filtering_verbs_nouns
import remove_stop_words
from Dataset2_processing.reading_Dataset2 import read_documents2
from Dataset2_processing import get_dictionary_for_documents
from Dataset1_processing import reading_Query1 ,calculate_evaluetion_for_Dataset1,processing_Dataset1,get_dictionary_for_Dataset1
from textblob import TextBlob

#import processing_Dataset2
#import processing_Dataset2

data1=read_documents1()
data2 = read_documents2()
query1= read_queries1()
query2=read_queries2()
print("reading is done//////////////////////////")
diction1 = get_dictionary_for_Dataset1.build_vec_mod()
diction= get_dictionary_for_documents.build_vec_mod()
word_embadding1 = processing_Dataset1.get_vector()
word_embadding2 =processing_Dataset2.get_vector()

print("word embadding is done///////////////////////////////////")
calculate_evaluetion_for_Dataset1.calculate()
calculate_evaluation_before_word.calculate()
print("calculate evaluation is done//////////////////////////////")



#print("sort_in main:::",diction)

f3 = open("terms.txt", "r")
saved_terms = f3.read()
f3.close()
saved_terms = list(ast.literal_eval(saved_terms))
#emd_for_save = nlp2(str(saved_terms)).vector
#print("save term for embadding",emd_for_save)


def search():
    q= input1.get("1.0","end-1c")
    print("q",q)
    query_embadding = nlp2.vocab[q].vector
    #print("word embadding for query::=",word_embad)

    corrected_query = ""
    for i in re.findall("\S+",q.lower()):
       # print("iiii",i)
        print("original text: " , str(i))
        b=TextBlob(i)
        print("corrected text: " , str(b.correct()))
        corrected_query += str(b.correct()) + " "
        #print("correct::",corrected_query)
    if q !=correctQuery:
        correctQuery.delete(0,END)
        correctQuery.insert(0,corrected_query)
    f = open("common_words", "r")
    content = f.read()
    f.close()
    stop_words = re.findall("\S+", content)

    termsInQuery = []  # this contain all terms in query without stop words
    terms = []  #
    ########################################################################
    # extract dates from query
    dates = re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                       "(0[1-9]|1[012])"
                       "[/.-](\d{4})", q)
    dates.extend(re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                            "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                            "[/.-](\d{4})", q))
    dates.extend(re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                            "(January|February|March|April|May|June|July|August|September|October|November|December)"
                            "[/.-](\d{4})", q))
    years = re.findall("\d{4}", q)

    # remove dates from string
    q = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
               "(0[1-9]|1[012])"
               "[/.-](\d{4})", "", q)
    q = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
               "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
               "[/.-](\d{4})", "", q)
    q = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
               "(January|February|March|April|May|June|July|August|September|October|November|December)"
               "[/.-](\d{4})", "", q)
    q = re.sub("\d{4}", "", q)
    # convert dates to regular form 01-Mar-2020
    dates = processing_Dataset2.convert_to_regular_date(dates)

    ## processing emails
    # extract emails from string in contentAFile
    emails = re.findall("\w+@\w+[.]\w+", q)
    # remove emails from string
    q = re.sub("\w+@\w+[.]\w+", "", q)

    ## processing phones
    # extract phones from string in contentAFile
    phones = re.findall("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4} | "
                        "\(\d{3}\)\s *\d{3}[-\.\s]??\d{4} |"
                        "\d{3}[-\.\s]??\d{4})", q)
    # remove phones from string
    q = re.sub("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4} | "
               "\(\d{3}\)\s *\d{3}[-\.\s]??\d{4} |"
               "\d{3}[-\.\s]??\d{4})", "", q)

    verbs_nounes = filtering_verbs_nouns.filter_verb_nouns(q)
    verbs = remove_stop_words.remove_stop_word(verbs_nounes[0], stop_words)
    nounes = remove_stop_words.remove_stop_word(verbs_nounes[1], stop_words)

    #######################################################################

    lmtzr = WordNetLemmatizer()
    lemmatizedVerbs = []
    for v in verbs:
        lemmatizedVerbs.append(WordNetLemmatizer().lemmatize(v, 'v'))

    verbs = lemmatizedVerbs

    porter = PorterStemmer()
    porteredNouns = []
    for n in nounes:
        porteredNouns.append(porter.stem(n))

    nounes = porteredNouns

    ################################################################
    termsInQuery.extend(verbs)
    termsInQuery.extend(nounes)
    termsInQuery.extend(years)
    termsInQuery.extend(phones)
    termsInQuery.extend(dates)
    termsInQuery.extend(emails)

    diction_query = {}  # dictionary for  terms and its frequencies
    for y in termsInQuery:
        diction_query.update({y: (1 + math.log(termsInQuery.count(y), 10)).__round__(5)})
        #print("diction_query::=",diction_query)

        #diction_embadding = nlp2(str(diction_query))
   # print("diction query embadding::",diction_embadding)


    # remove duplication from termsInQuery
    tempTerms = []
    for w in termsInQuery:
        if w not in tempTerms:
            tempTerms.append(w)
            #print("temp term",tempTerms)
            #print("term",tempTerms)
           # embadding_query = nlp2.vocab[tempTerms].vector
            #print("query_embadding::",embadding_query)
    #print("diction::=",diction)
    termsInQuery = tempTerms
    # print(termsInQuery)
    # print(diction_query)

    # # Extension of the previous diction in order to contain all terms
    # # and show their repetition within the query
    temp_dic2 = diction_query.copy()
    diction_query.clear()
    result = []

    for term in saved_terms:
        #term_embadding = nlp2(str(term))
        if term not in temp_dic2.keys():
            diction_query.update({term: 0.0})
        else:
            diction_query.update({term: temp_dic2[term]})
            # diction_query.update({y: 505})
            #print("term embadding for term",term_embadding)
        #for t in diction_embadding:
         #    result = t.similarity(term_embadding)

    #for t in diction_embadding:
        #for a in term_embadding:
        #    result = a.similarity(t)
          #  print(t.text,t.has_vector,t.vector_norm,t.is_oov)
          #   print( "result===",result)
           #  reslist = sorted(result, key=lambda item: -item[1])
            # print("reslist",reslist)
    # for x, y in diction_query.items():
    #     print(x," ====> ", y)

    # # check if vector of the query is zero or not , if was zero that mean the query
    # # will not return any results
    #word_embad_for_diction = nlp2(diction).vector
    #print("word_embadding for dictionary:::=",word_embad_for_diction)

    #for a in term_embadding:
       # for t in diction_embadding:
            #print("term_text::",a.text,"diction_text::",t.text,t.similarity(a))
    #cosine_similarity = lambda x, y: 1 - spatial.distance.cosine(x, y)
   # computed_similarity = []

    #for word in saved_terms:
      #  similarity = cosine_similarity(query_embadding,nlp2.vocab[word].vector)
      #  computed_similarity.append((word,similarity))


    #for word in tempTerms:
        #for word in tempTerms:
        #result = processing_Dataset2.get_similarity2(tempTerms,diction)
        result_query = ""
        #reslist = sorted(result.items(), key=lambda item: -item[1])
        #sortdict = dict(reslist)
        #print("reslist",reslist)
        #print("sortdic",sortdict)
    #c=0
    #for r in sortdict:
     #   c +=1
      #  result_query += "d({}) -".format(r)
       # if c == 10:
        #    break




    #len_vec_query = vectorMath.calculate_length_vector(list(diction_query.values()))
    #if len_vec_query != 0.0:
        #result = diction_embadding.similarity(term_embadding)
     #   result = processing_Dataset2.find_revelance_documents(list(diction_query.values()), diction)
      #  result_query = ""
        #print("result::", result)

   #     reslist = sorted(result.item, key=lambda x: x[1])
     #   sortdict = dict(reslist)

   # c = 0
     #for r in sortdict:
       # c += 1
      #  result_query += "d({}) -".format(r)
      #  if c == 10:
       #    break

        #######################################################################

        output1.delete(0, END)  # reset the output field
        output1.insert(0, result_query)  # write in output field
    else:
        output1.delete(0, END)  # reset the output field
        output1.insert(0, "Sorry No Results")  # write in output field






#root=Tk()

#frm =ttk.Frame(root,padding=10)
#frm.grid()
#ttk.Label(frm,text="Ammar Shannar").grid(column=0,row=0)
#ttk.Button(frm,text="Quite",command=root.destroy).grid(column=1,row=0)
#root.mainloop()

def CISI_window():
      to_cisi = Toplevel(root1)
    #  to_cisi.minsize(600,300)
    #  lable1 = Label(to_cisi, text="Enter Your Query ...!?", font=("Arial Bold", 20))
    #  lable1.pack()
      #input1 = Text(to_cisi, width=50, height=4)
     # input1.pack()
     # B = Button(to_cisi, text="search", font=("Arial Bold", 10), command=search)
     # B.pack()

def CACM_Window():
    to_cacm=Toplevel(root1)
    to_cacm.minsize(600, 300)
    lable1 = Label(to_cacm, text="Enter Your Query ...!?", font=("Arial Bold", 20))
    lable1.pack()

    # input1 = Entry(root, width=90)
    input1 = Text(to_cacm, width=50, height=4)
    input1.pack()

    B = Button(to_cacm, text="search", font=("Arial Bold", 10), command=search)
    B.pack()

    lable1 = Label(to_cacm, text="correct query", font=("Arial Bold", 10))
    lable1.pack()

    correctQuery = Entry(to_cacm, width=80)
    correctQuery.pack()

    lable1 = Label(to_cacm, text="result", font=("Arial Bold", 10))
    lable1.pack()

    output1 = Entry(to_cacm, width=80)
    output1.pack()






root1 = Tk()
root1.geometry('200x100')
btn = Button(root1, text="Create a new window", command =CISI_window())
btn.pack(pady = 10)
#btn = Button(root1, text="Create a new window", command =CACM_Window())
#btn.pack(pady = 10)
root1.title("IR")
root1.minsize(600, 300)
lable1 = Label(root1, text="Enter Your Query ...!?", font=("Arial Bold", 20))
lable1.pack()

    # input1 = Entry(root, width=90)
input1 = Text(root1, width=50, height=4)
input1.pack()
B = Button(root1, text="search", font=("Arial Bold", 10), command=search)
B.pack()

lable1 = Label(root1, text="correct query", font=("Arial Bold", 10))
lable1.pack()
correctQuery = Entry(root1, width=80)
correctQuery.pack()

lable1 = Label(root1, text="result", font=("Arial Bold", 10))
lable1.pack()

output1 = Entry(root1, width=80)
output1.pack()



root1.mainloop()

















