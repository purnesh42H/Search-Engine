import re
import os
import glob

InputQueries = []
results = {}

rawHtmlFolder       = os.getcwd() + '/corpus/'
docId2DocNumFile    = 'DocumentIndexMapping_CACM.txt'
queryResultFile     = os.getcwd() + '/7thRun_BM25_Stopping/BM25_Stopping_QueryResults.txt'
queryFile           = os.getcwd() + '\\cacm.query'
pTagRegex           = '<pre>(.*?)</pre>'

minFreq = 3
maxFreq = 8

def queries():
    queries = open(queryFile, 'r').read()
    pattern = re.compile(r'</DOCNO>(.*?)</DOC>')
    lst = re.findall(pattern, queries.replace('\n',' '))
    for query in lst:
        InputQueries.append(query)

def prefixZero(suffix):
    i = 0
    prefix = ''
    while i < 4 - len(suffix):
        prefix += '%d' % i
        i+=1
    return prefix + suffix

def getParagraphs(body):
    pattern = re.compile(pTagRegex)
    return re.findall(pattern, body)

def rankingResult():
    with open(queryResultFile, 'r') as f:
        for res in f:
            items = res.split(' ')
            queryID = items[0]
            documentID = items[2]
            documentID = 'CACM-' + prefixZero(documentID) + '.html'
            if queryID in results:
                if len(results[queryID]) < 10:
                    results[queryID].append(documentID)
            else:
                results[queryID] = [documentID]

    f.close()
    
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

def getSnippet(docDict, text):
    words = text.split(' ')
    snippet = ''
    snippets = []
    for word in words:
        if word in docDict:
            if docDict[word] > minFreq and docDict[word] < maxFreq:
                snippet += word + ' '
                maxNSWordCount = 0
            else:
                if snippet != '':
                    if maxNSWordCount < 4:
                        maxNSWordCount += 1
                        snippet += word + ' '
                    else:
                        snippets.append(snippet.strip())
                        snippet = ''
    return snippets

def removePunctuation(text):
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
    
    return text.lower()

def highlight(snippets, query):
    newSnippet = ''
    query = removePunctuation(query)
    for snippet in snippets:
        words = snippet.split(' ')
        for word in words:
            if ' ' + word.lower() + ' ' in query:
                newSnippet += '<HL>'+ word + '</HL> '
            else:
                newSnippet += word + ' '
        newSnippet +='.... '

    return newSnippet
              
def printSnippet(queryId):
    query = InputQueries[i]
    qid = '%d' % (queryId + 1)
    snippet = ''
    for doc in results[qid]:
        with open (rawHtmlFolder + doc, 'r') as htmlFile:
            text = getParagraphs(htmlFile.read().replace('\n',' ').replace('\t',' ').replace('   ',' ').replace('  ', ' '))
            docDict = getTextTif(text[0])
            snippet += '"'+ doc + '":\n'
            snippet += highlight(getSnippet(docDict, text[0]), query) + '\n\n'

    return snippet
            
            
queries()
rankingResult()
with open (os.getcwd() + '/snippets.txt', 'a+') as sFile:
    i = 0
    for i in range(len(InputQueries)):
        sFile.write('query %d: %s\n' % (i+1, InputQueries[i]))
        sFile.write('%s' % printSnippet(i))
        sFile.write('----------------------------------------------------------------------------------\n\n')

    sFile.close()
