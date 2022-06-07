import analyze_date
import lemmatize_for_query
import normalize_doc
import stem_for_query
import re


def query_process(contentAQuery):
    tokines = []  # contain all terms for all docs
    termsInAQuery = []  # this contains all terms in (current file) without stop words

    contentAFile = contentAQuery.lower()

    contentAFile = normalize_doc.do_normalize(contentAFile)

    contentAFile = analyze_date.do_findDate(contentAFile)

    verbs=lemmatize_for_query.lemmatiz_for_verb(contentAQuery)
    nouns=stem_for_query.nouns_stemming(contentAQuery)

    termsInAQuery.extend(verbs)
    termsInAQuery.extend(nouns)

    tempTerms = []
    for w in termsInAQuery:
        if w not in tempTerms:
               tempTerms.append(w)


    return tempTerms