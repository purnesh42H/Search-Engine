import re
import os
import glob
from collections import *

PlainTextFileFolder = os.getcwd() + '/PlainText/'

oneGram_tfTable = 'MyIndex\\OneGram_TfTable.txt'
oneGram_dfTable = 'MyIndex\\OneGram_DfTable.txt'

twoGram_tfTable = 'MyIndex\\TwoGram_TfTable.txt'
twoGram_dfTable = 'MyIndex\\TwoGram_DfTable.txt'

threeGram_tfTable = 'MyIndex\\ThreeGram_TfTable.txt'
threeGram_dfTable = 'MyIndex\\ThreeGram_DfTable.txt'

oneGram_Stoplist     = 'MyIndex\\Task3_Stoplist_OneGram.txt'

invertedIndex = {}

class TermFrequency:

    def __init__(self, docNumber, docId, freq):
        self.docNumber = docNumber
        self.docId = docId
        self.frequency = freq

    def setDocId(self, docNum):
        self.docNumber = docNum
        
    def setDocId(self, docId):
        self.docId = docId

    def increaseFrequence(self, freq):
        self.frequency = freq

class Document:
    
    def __init__(self, tf):
        self.tf = tf

    def appendTf(self, tf):
        self.tf.append(tf)


def getGramFrequency(text):
    wordFreq = {}
    for unword in text.split(' '):
        word = unword.strip("'")
        if word in wordFreq:
            wordFreq[word] += 1
        else:
            wordFreq[word] = 1
    return wordFreq

def prepareInvertedIndex(gramSequence):
    docCounter = 1
    for root, dirs, files in os.walk(PlainTextFileFolder):
        for document in files:
            #print docCounter
            with open (PlainTextFileFolder + document, 'r') as textFile:
                nGramFrequencies = getGramFrequency(textByGram(textFile.read().
                                               replace('\n',' ').replace('    ',' ').replace('   ',' ').replace('  ', ' ')
                                                                 , gramSequence))
            for word in nGramFrequencies:
                if (word.count('2_2') == gramSequence - 1 and word.split('2_2')[0] != '' and word.split('2_2')[gramSequence - 1] != ''):
                    if word not in invertedIndex and word != ' ' and word != '':
                        invertedIndex[word] = Document([TermFrequency(docCounter,
                                                        document,
                                                        nGramFrequencies[word])])
                    else:
                        invertedIndex[word].appendTf(TermFrequency(docCounter,
                                                        document,
                                                        nGramFrequencies[word]))
            docCounter += 1

def textByGram(text, n):
    if n == 1:
        return text

    nGramText = ''
    newText = ''
    wordCount = 0
    textBySpace = text.split(' ')
    textLength  = len(textBySpace)
    inWordCount = 1
    while wordCount < len(textBySpace) - n:
        newText += textBySpace[wordCount]
        inWordCount = 1
        while (inWordCount % n) != 0:
            if textBySpace[wordCount + inWordCount] == ' ':
                wordCount += 1
                continue
            newText += '2_2' + textBySpace[wordCount + inWordCount]
            inWordCount += 1
        newText += ' '
        wordCount += 1

    newText += textBySpace[textLength - n]
    inWordCount = 1
    while (inWordCount % n) != 0:
        newText += '2_2' + textBySpace[textLength - (n - inWordCount)]
        inWordCount += 1
         
    return newText
            
def getGramInvertedList():
    tfTable = {}
    for word in invertedIndex:
        freq = 0
        for doc in invertedIndex[word].tf:
            freq += doc.frequency
            
        tfTable[word.replace('2_2',' ')] = freq

    return tfTable

def createTfTable(tfTable, gramFile):
    totWords = 0
    with open (os.getcwd() + '/' + gramFile, 'a+') as tfFile:
        tfFile.write('term, tf')
        for key, value in (OrderedDict(sorted(tfTable.items(), key=lambda x: x[1], reverse = True))).items():
            tfFile.write('\n%s, %d' % (key, value))
            totWords += float(value)
    print 'Total number of tokens = %f' % totWords
        
def createGramDocumentFrequency(gramFile):
    with open (os.getcwd() + '/' + gramFile, 'a+') as dfFile:
        dfFile.write('term docID df')
        for word, value in (OrderedDict(sorted(invertedIndex.items(), key=lambda x: x[0]))).items():
            line = '\n' + word.replace('2_2',' ') + ' '
            for doc in invertedIndex[word].tf:
                line += '%d,' % doc.docNumber
            line = line[:-1] + ' %d' % len(invertedIndex[word].tf)
            dfFile.write(line)

def generateStoplist(stoplist_file):
    with open (os.getcwd() + '/' + stoplist_file, 'a+') as stopFile:
        for word in invertedIndex:
            if len(invertedIndex[word].tf) >= 500:
                stopFile.write(word + '\n')
                
print ('Processing 1 grams....')
prepareInvertedIndex(1)
generateStoplist(oneGram_Stoplist)
createTfTable(getGramInvertedList(), oneGram_tfTable)
createGramDocumentFrequency(oneGram_dfTable)

#invertedIndex = {}

##print ('Processing 2 grams....')
##prepareInvertedIndex(2)
##createTfTable(getGramInvertedList(), twoGram_tfTable)
##createGramDocumentFrequency(twoGram_dfTable)
##
##invertedIndex = {}
##
##print ('Processing 3 grams....')
##prepareInvertedIndex(3)
##createTfTable(getGramInvertedList(), threeGram_tfTable)
##createGramDocumentFrequency(threeGram_dfTable)
                                
