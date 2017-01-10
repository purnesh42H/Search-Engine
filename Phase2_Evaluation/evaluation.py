
import os
from collections import OrderedDict
import math

RELEVANCEJUDGEMENT_FILE_PATH = 'cacm.rel.txt'
RETRIEVAL_MODELS_PATH = 'Runs which need Evaluation/'
EVALUATION_RESULTS_FILE_PATH = 'Evaluation Results/'
SUMMARY_FILE_NAME = 'summary.txt'

relevanceJudgements = {}

def retrieveRelevanceJudgement():
    with open(RELEVANCEJUDGEMENT_FILE_PATH, 'r') as f:
        for relevanceJudgement in f:

            items = relevanceJudgement.split(' ')
            queryID = items[0]
            documentID = items[2]
            
            # add front 0s to revise document name to standard form
            if len(documentID) < 9:
                for i in range(9 - len(documentID)):
                    documentID = documentID[0:5] + '0' + documentID[5:len(documentID)]
            documentID = documentID.strip('CACM-')
            # add into relevance judgement dictionary
            if queryID in relevanceJudgements:
                relevanceJudgements[queryID].append(documentID)
            else:
                relevanceJudgements[queryID] = [ documentID ]
    f.close()

def retrieveQueryResults(fileName):
    queryResults = OrderedDict()
    with open(fileName, 'r') as fr:
        for queryResult in fr:
            items = queryResult.split(' ')
            queryID = items[0]
            documentID = items[2]
            if queryID in queryResults:
                queryResults[queryID].append(documentID)
            else:
                queryResults[queryID] = [ documentID ]
    fr.close()
    return queryResults

def calculateMeasure(fileName, queryResults, summary):
    AP = []
    RR = []
    P5 = []
    P20 = []
    fw = open(fileName, 'w')
    for queryID in queryResults:
        psum = 0
        rr = 0
        results = queryResults[queryID]
        rank = 0
        relevantNumber = 0
        relevantDocuments = []
        # exclude queries which don't have relevant documents
        if queryID in relevanceJudgements:
            relevantDocuments = relevanceJudgements[queryID]
        else:
            continue
        for document in results:
            rank += 1
            isRelevant = 0
            if document in relevantDocuments:
                if relevantNumber == 0:
                    rr = 1 / (rank * 1.0)
                relevantNumber += 1
                isRelevant = 1
            precision = relevantNumber / (rank * 1.0)
            # AP
            if isRelevant == 1:
                psum += precision
            # P@5
            if rank == 5:
                P5.append(precision)
            # P@20
            if rank == 20:
                P20.append(precision)
            recall = 0 if len(relevantDocuments) == 0 else relevantNumber / (len(relevantDocuments) * 1.0)
            fw.write(queryID + ' ' + document + ' ' + str(rank) + ' ' + str(isRelevant) + ' ' + str("{:.3f}".format(precision)) + ' ' + str("{:.3f}".format(recall)) + '\n')
        if relevantNumber != 0:
            AP.append(psum / (relevantNumber * 1.0))
        else:
            AP.append(0.0)
        RR.append(rr)
    summary.write('MAP = ' + str("{:.3f}".format(math.fsum(AP) / len(AP))) + '\n')
    summary.write('MRR = ' + str("{:.3f}".format(math.fsum(RR) / len(RR))) + '\n')
    summary.write('Mean P@5 = ' + str("{:.3f}".format(math.fsum(P5) / len(P5))) + '\n')
    summary.write('Mean P@20 = ' + str("{:.3f}".format(math.fsum(P20) / len(P20))) + '\n')
    fw.close()

def evaluation(path):
    with open(EVALUATION_RESULTS_FILE_PATH + SUMMARY_FILE_NAME, 'w') as summary:
        for fileName in os.listdir(path):
            if fileName == '.DS_Store':
                continue

            runName = fileName[0:fileName.find('.txt')]
            summary.write(runName + '\n')

            # read query results from previous file
            queryResults = retrieveQueryResults(path + fileName)
            # calculate measure
            calculateMeasure(EVALUATION_RESULTS_FILE_PATH + 'evaluation_' + fileName, queryResults, summary)

    summary.close()

def  main():
    retrieveRelevanceJudgement()
    evaluation(RETRIEVAL_MODELS_PATH)

main()
