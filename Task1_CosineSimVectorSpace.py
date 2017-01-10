#!/usr/bin/env python

import os
import glob
import re
import math
import operator
from collections import *
import decimal
import time
from threading import Thread
decimal.getcontext().prec = 10

InputQueries = []
scoredDoc = {}

queryFile       = os.getcwd() + '\\cacm.query'
uniGram_DfTable = open (os.getcwd() + '\\MyIndex\\OneGram_DfTable.txt', 'r').read()
uniGram_TfTable = open(os.getcwd() + '\\MyIndex\\OneGram_TfTable.txt', 'r').read()
PlainTextFolder = os.getcwd() + '\\PlainText'
IndexMappingDoc = open(os.getcwd() + '\\DocumentIndexMapping_CACM.txt', 'r').read()
N = 0

numericRegex            = r'(\d{1,3},\d{3}(,\d{3})*)(\.\d*)?|\d+\.?\d*'
alphanumericRegex       = '.*\\d+.*'

def corpusSize():
    return (len(IndexMappingDoc.split('\n')) - 1)

def queries():
    queries = open(queryFile, 'r').read()
    pattern = re.compile(r'</DOCNO>(.*?)</DOC>')
    lst = re.findall(pattern, queries.replace('\n',' '))
    for query in lst:
        InputQueries.append(removePunctuation(query.strip().lower()))
        
def splitQuery(query):
    query.strip().split(' ')

def removePunctuation(text):
    pattern = re.compile(numericRegex)
    if hasNumber(text):
       text = preservePunctuation(text)
    else:
        if ',' in text:
            text = text.replace(',',' ')
        if '.' in text:
            text = text.replace('.',' ')

    if '/' in text:
        text = text.replace('/',' ')
    if '?' in text:
        text = text.replace('?',' ')
    if '!' in text:
        text = text.replace('!',' ')
    if '"' in text:
        text = text.replace('"',' ')
    if '~' in text:
        text = text.replace('~',' ')
    if '@' in text:
        text = text.replace('@',' ')
    if '#' in text:
        text = text.replace('#',' ')
    if '(' in text:
        text = text.replace('(',' ')
    if ')' in text:
        text = text.replace(')',' ')
    if '^' in text:
        text = text.replace('^',' ')
    if '[' in text:
        text = text.replace('[',' ')
    if ']' in text:
        text = text.replace(']',' ')
    if ':' in text:
        text = text.replace(':',' ')
    if ';' in text:
        text = text.replace(';',' ')
    if '&amp' in text:
        text = text.replace('&amp',' ')
    if '&nbsp' in text:
        text = text.replace('&nbsp',' ')

    if text != '' and (text[-1] == '.' or text[-1] == ','):
        return text[:-1]
    
    return text

def hasNumber(text):
    pattern = re.compile(alphanumericRegex)
    if re.match(pattern, text):
        return True

    return False

def preservePunctuation(text):
    n = len(text)
    i = 0
    while i < n-1:
        if i>0 and (text[i] == ',' or text[i] == '.'):
            if not (re.match('[0-9]', text[i - 1]) and re.match('[0-9]', text[i + 1])):
                text = text[:i] + text[(i+1):]
                n-=1
        i+=1
        
    return text

def getTermDocIds(term):
    if '*' in term:
        term = term.replace('*','\*')
    if '+' in term:
        term = term.replace('+','\+')
    pattern = re.compile(r'\n' + term + ' (.+?) ')
    result  = re.findall(pattern, uniGram_DfTable)
    doc = []
    if len(result) > 0:
        doc = result[0].split(',')
        
    return doc

def getDoc(docId):
    pattern = re.compile(r'\n' + docId + ', (.+?), ')
    result  = re.findall(pattern, IndexMappingDoc)
    doc = ''
    if len(result) > 0:
        doc = result[0] + '.txt'
    return doc

def getTextTif(text):
    wordFreq = {}
    for unigram in text.split(' '):
        word = unigram.strip("'").strip()
        if word == '':
            continue
        if word in wordFreq:
            wordFreq[word] += 1
        else:
            wordFreq[word] = 1
    return wordFreq

def getDocTif(doc):
    text = open(PlainTextFolder + '\\' + doc).read()
    return getTextTif(text)

def getTf(term, text):
    if '*' in term:
        term = term.replace('*','\*')
    if '+' in term:
        term = term.replace('+','\+')
    pattern = re.compile(r' \b' + term + r'\b ')
    return len(re.findall(pattern, text))

def getTermWeightInQuery(term, queryDict, query):
    if term not in queryDict:
        return 0
    return decimal.Decimal(queryDict[term])/(getTextLength(query))

def getTermWeightInDoc(term, idf, tf):
    termComp  = 1 + math.log(tf, 10)
    numerator = decimal.Decimal((termComp)*idf)
    return numerator

def getTextLength(text):
    return len(text.split(' '))

def getIdf(n):
    if n == 0:
        return 0
    return math.log(N/n, 10)

def getDocScore(query, docId):
    queryDict = getTextTif(query)
    docDict   = getDocTif(getDoc(docId))
    
    numerator = decimal.Decimal(0.0)
    wDocSqSum = decimal.Decimal(0.0)
    wQuerySqSum = decimal.Decimal(0.0)
    
    for term in docDict:
        tf = docDict[term]
        idf = getIdf(len(getTermDocIds(term)))
        wQuery = getTermWeightInQuery(term, queryDict, query)
        wDoc   = getTermWeightInDoc(term, idf, tf)
        numerator += wDoc*wQuery
        wDocSqSum += pow(wDoc,2)
        wQuerySqSum += pow(wQuery,2)
        
    denominator = wDocSqSum * wQuerySqSum
    return numerator/(decimal.Decimal(math.sqrt(denominator)) + 1)

def getQueryDocs(query):
    docs = []
    queryTif = getTextTif(query)
    for term in queryTif:
        tD = getTermDocIds(term)
        for docId in tD:
            if docId not in docs:
                docs.append(docId)

    return docs

def scoreDocuments(query, batch):
    global scoredDoc
    for docId in batch:
        scoredDoc[docId] = getDocScore(query, docId)
    

def multiThreadAssignment(query, queryDocs):
    threads = []
    threadCount = 16
    docBatch = len(queryDocs)/threadCount
    batchSet = 0
    i=1
    batches = 0
    while batchSet < len(queryDocs) and i < threadCount:
        batch = queryDocs[batchSet : batchSet + docBatch]
        t = Thread(target=scoreDocuments, args=(query, batch, ))
        t.start()
        threads.append(t)
        batches += len(batch)
        batchSet += docBatch
        i+=1
    batch = queryDocs[batches:]
    t = Thread(target=scoreDocuments, args=(query, batch, ))
    t.start()
    threads.append(t)
    for t in threads:
        t.join()
    
def assignScoresToDocs(query):
    global scoredDoc
    start = time.time()
    scoredDoc = {}
    queryDocs = getQueryDocs(query)
    multiThreadAssignment(query, sorted(queryDocs))
    end = time.time()
    print 'Elapsed Time: %lf' % (end - start)
    return (OrderedDict(sorted(scoredDoc.items(), key=lambda x: x[1], reverse = True)))
   
queries()
N = corpusSize()
print 'Total Documents - %d' % N
with open('CosineSim_QueryResults.txt','a+') as queryResults:
    queryResults.write('query_id Q0 docid rank CosineSim_score system_name')
    i = 1
    j= 1
    for query in InputQueries:
        print 'query - %d' % i
        print query
        docs = assignScoresToDocs(query)
        rank = 1
        with open('CosineSim_Query_%d_Result.txt' % i,'a+') as queryResult:
            queryResult.write('query_id Q0 docid rank CosineSim_score system_name')
            for doc in docs:
                queryResults.write('\n%d Q0 %s %d %lf CosineSim' % (i, doc, rank, docs[doc]))
                queryResult.write('\n%d Q0 %s %d %lf CosineSim' % (i, doc, rank, docs[doc]))
                if rank == 100:
                    break
                rank += 1
        i+=1 
