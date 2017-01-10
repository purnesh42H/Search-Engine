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
relevanceJudgements = {}

queryFile       = os.getcwd() + '\\cacm.query'
uniGram_DfTable = open (os.getcwd() + '\\MyIndex\\OneGram_DfTable.txt', 'r').read()
uniGram_TfTable = open(os.getcwd() + '\\MyIndex\\OneGram_TfTable.txt', 'r').read()
PlainTextFolder = os.getcwd() + '\\PlainText'
IndexMappingDoc = open(os.getcwd() + '\\DocumentIndexMapping_CACM.txt', 'r').read()
relJudgementFile = os.getcwd() + '\\cacm.rel'
N = 0

numericRegex            = r'(\d{1,3},\d{3}(,\d{3})*)(\.\d*)?|\d+\.?\d*'
alphanumericRegex       = '.*/d+.*'

def corpusSize():
    return (len(IndexMappingDoc.split('\n')) - 1)

def queries():
    queries = open(queryFile, 'r').read()
    pattern = re.compile(r'</DOCNO>(.*?)</DOC>')
    lst = re.findall(pattern, queries.replace('\n',' '))
    for query in lst:
        InputQueries.append(removePunctuation(query.strip().lower()))

def retrieveRelevanceJudgement():
    with open(relJudgementFile, 'r') as f:
        for relevanceJudgement in f:

            items = relevanceJudgement.split(' ')
            queryID = items[0]
            documentID = items[2]
            documentID = documentID.strip('CACM-')
          
            if queryID in relevanceJudgements:
                relevanceJudgements[queryID].append(documentID)
            else:
                relevanceJudgements[queryID] = [ documentID ]
    f.close()
        
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
    return decimal.Decimal(queryDict[term])/(getTextLength(query))

def getTermWeightInDoc(term, idf, tf, docLen):
    termComp = float(tf)
    numerator = decimal.Decimal((termComp)*idf)
    return numerator

def getTextLength(text):
    return len(text.split(' '))

def getIdf(n):
    if n == 0:
        return 0
    return math.log(N/n, 10)

def relDocTerm(term, termDocs, relDocs):
    r = 0.0
    for doc in termDocs:
        if doc in relDocs:
            r += 1.0
    return r

def getDocScore(query, docId, queryId):
    score = decimal.Decimal(0.0)
    queryDict = getTextTif(query)
    docDict   = getDocTif(getDoc(docId))
    part1 = 0.0
    part2 = 0.0
    part3 = 0.0
    k1    = 1.2
    k2    = 100
    if queryId in relevanceJudgements:
        R = len(relevanceJudgements[queryId])
    else:
        R = 0.0
    b     = 0.75

    docText = open(PlainTextFolder + '/' + (getDoc(docId))).read()
    dl = getTextLength(docText)
    avdl = dl/len(docDict)

    K    = k1*((1-b) + (b*dl/avdl))
    
    for term in queryDict:
        termDocs = getTermDocIds(term)
        n = len(termDocs)
        if queryId in relevanceJudgements:
            r = relDocTerm(term, termDocs, relevanceJudgements[queryId])
        else:
            r = 0.0
        f = getTf(term, docText)
        qf = queryDict[term]
        part1=math.log(((r+0.5)/(R-r+0.5))/((n-r+0.5)/(N-n-R+r+0.5)))
        part2=((k1+1)*f)/(K+f)
        part3=((k2+1)*qf)/(k2+qf)
        score += decimal.Decimal(part1*part2*part3)
        
    return score

def getQueryDocs(query):
    docs = []
    queryTif = getTextTif(query)
    for term in queryTif:
        tD = getTermDocIds(term)
        for docId in tD:
            if docId not in docs:
                docs.append(docId)

    return docs

def scoreDocuments(query, batch, queryId):
    global scoredDoc
    for docId in batch:
        scoredDoc[docId] = getDocScore(query, docId, queryId)
    
def multiThreadAssignment(query, queryDocs, queryId):
    threads = []
    threadCount = 16
    docBatch = len(queryDocs)/threadCount
    batchSet = 0
    i=1
    batches = 0
    while batchSet < len(queryDocs) and i < threadCount:
        batch = queryDocs[batchSet : batchSet + docBatch]
        t = Thread(target=scoreDocuments, args=(query, batch, queryId, ))
        t.start()
        threads.append(t)
        batches += len(batch)
        batchSet += docBatch
        i+=1
    batch = queryDocs[batches:]
    t = Thread(target=scoreDocuments, args=(query, batch, queryId, ))
    t.start()
    threads.append(t)
    for t in threads:
        t.join()
    
def assignScoresToDocs(query, queryId):
    global scoredDoc
    start = time.time()
    scoredDoc = {}
    queryDocs = getQueryDocs(query)
    multiThreadAssignment(query, sorted(queryDocs), queryId)
    end = time.time()
    print 'Elapsed Time: %lf' % (end - start)
    return (OrderedDict(sorted(scoredDoc.items(), key=lambda x: x[1], reverse = True)))
   
queries()
retrieveRelevanceJudgement()
N = corpusSize()
print 'Total Documents - %d' % N
with open('BM25_QueryResults.txt','a+') as queryResults:
    queryResults.write('query_id Q0 docid rank TfIdf_score system_name')
    i = 1
    j = 1
    for query in InputQueries:
        if j <= 33:
            j+=1
            i+=1
            continue
        print 'query - %d' % i
        print query
        docs = assignScoresToDocs(query, '%d' % i)
        rank = 1
        with open('BM25_Query_%d_Result.txt' % i,'a+') as queryResult:
            queryResult.write('query_id Q0 docid rank TfIdf_score system_name')
            for doc in docs:
                queryResults.write('\n%d Q0 %s %d %lf BM25' % (i, doc, rank, docs[doc]))
                queryResult.write('\n%d Q0 %s %d %lf BM25' % (i, doc, rank, docs[doc]))
                if rank == 100:
                    break
                rank += 1
        i+=1 
