# Overview
This project was intended to design and develop a sophisticated search engine for the CACM dataset that can produce relavant documents(top 100) for a given query. Project was carried out in following phases:
- [Index creation and text processing](#indexer-and-text-processor)
- [Implemention of base retrieval models - Tf-Idf, Cosine Vector Space, Lucene, BM25](#base-retrieval-models-implementation)
- [Evaluate each model over the CACM dataset based on standard parameters MAP, MRR, P@K and Precision & Recall](#base-models-evaluation)
- [Choose any one models(Tf-Idf for this project) and enhance it by incorporating query expansion(psuedo-relavance) and query processing(stopping, stemming) techniques](#tf-idf-enhancements)
- [Choose the best base model(BM25) and enhance it by query processing techinque "stopping"](#bm25-with-stopping)
- [Evaluate the enhanced models over the CACM dataset based on standard parameters MAP, MRR, P@K and Precision & Recall and tabulate the results](#final-evaluation)
- [Choose the best model(BM25 with stopping) and display the query results with summary highlighting the query words from each relavant document](#snippet-generation)

# Source Codes(Python files):
- Task1_HtmlTextExtracter.py - To convert the raw html to plain text
- Task1_HtmlTextExtracter.py - To index the CACM dataset
- Task1_TfIdf.py - TfIdf baseline model
- Task1_CosineSimVectorSpace.py - Vector Space Cosine Sim baseline model
- Task1_BM25.py - BM25 baseline model
- Task2_TfIdf_Pseudo_Relevance.py - TfIf with pseudo relevance
- Task3_TextExtracter_StemText.py - To extract documents from stemmed text 
collection
- Task3_InvertedIndexer_StemText.py - To index the CACM stemmed dataset
- Task3_TfIdf_StemText.py - TfIdf with stemming
- Task3_TfIdf_Stopping.py - TfIdf with Stopping
- SnippetGeneration_ExtraCredits.py - To generate snippet of top 10 documents for 64 queries
- ~\Project\Phase2_Evaluation.py - Evaluates all the search engine by calculating effectiveness parameters

# Source Codes(Java files):
- ~\Project\3rdRun_Lucene_Baseline\src\com\lucene\HW4.java - Lucene baseline model

# Setup and compile python files:

The files are build on Python version 2.7x

In windows:
  - Open the python editor IDLE from the menu, and open xxxx.py(eg: Task-1.py for Task-1), then press F5 to run it.

In Linux:
1. On terminal, type chmod u+rx xxxx.py(eg: Task-1.py for Task-1) to make file executable and press Enter
2. Type python xxxx.py(eg: Task-1.py for Task-1) and press Enter
3. Provide the corpus file in directory "Corpus\\..."

Setup and compile java files:
Step 1: Open command prompt
Step 2: Include lucene-core-4.7.2.jar, lucene-analyzers-common-4.7.2.jar, lucene-queryparser-4.7.2.jar
Step 3: Compile HW4.java by writing " javac HW4.java" on command prompt.
Step 4: Execute the HW4.java file by following command
javac -cp ".;lucene-core-4.7.2.jar;lucene-analyzers-common-4.7.2.jar;lucene-queryparser-4.7.2.jar" HW4.java
java -cp ".;lucene-core-4.7.2.jar;lucene-analyzers-common-4.7.2.jar;lucene-queryparser-4.7.2.jar" HW4

## Indexer And Text Processor
Text Processor code files
- For raw CACM corpus(/corpus) - Task1_HtmlTextExtracter.py
- For stemmed CACM corpus(/StemCorpus) - Task3_TextExtracter_StemText.py

Text Process output files
- /PlainText: Processed files of raw CACM corpus
- /StemmedText: Processed files stemmed CACM corpus

Indexer code files
- For raw CACM corpus - Task1_InvertedIndexer.py
- For stemmed CACM corpus - Task3_InvertedIndexer_StemText.py

Indexer output files
- /MyIndex
  - OneGram_DfTable.txt - Unigram document frequency index for raw CACM dataset(term, docId, df)
  - OneGram_DfTable_Stem.txt - Unigram document frequency index for stemmed CACM dataset(term, docId, df)
  - OneGram_TfTable.txt - Unigram term frequency index for raw CACM dataset(term, tf)
  - OneGram_TfTable_Stem.txt - Unigram term frequency index for stemmed CACM dataset(term, tf)
  
Stoplists
- /MyIndex/Task3_Stoplist_OneGram.txt - Stopwords for raw CACM dataset
- /MyIndex/Task3_Stoplist_OneGram_Stem.txt - Stopwords for stemmed CACM dataset

## Base Retrieval Models Implementation
- Tf-Idf
  - Code: Task1_TfIdf.py
  - Result(Top 100 Documents for each query): /1stRun_TfIdf_Baseline/TfIdf_QueryResults.txt
  
- Cosine Vector Space
  - Code: Task1_CosineSimVectorSpace.py
  - Result(Top 100 Documents for each query): /2ndRun_CosinSim_Baseline/CosineSim_QueryResults.txt
  
- Lucene(Used the code from one of my assignment)
  - Code: /3rdRun_Lucene_Baseline/src/com/lucene/HW4.java
  - Result(Top 100 Documents for each query): /3rdRun_Lucene_Baseline/Lucene_QueryResults.txt

- BM25
  - Code: Task1_BM25.py
  - Result(Top 100 Documents for each query): /4thRun_BM25_Baseline/BM25_QueryResults.txt

## Base Models Evaluation
  - Code: Phase2_Evaluation/evaluation.py
  - Relavance file: Phase2_Evaluation/cacm.rel.txt
  
Tf-Idf
- Result: /Phase2_Evaluation/Evaluation Results/evaluation_TfIdf_QueryResults.txt
- MAP = 0.289
- MRR = 0.537
- Mean P@5 = 0.227
- Mean P@20 = 0.139

Cosine Vector Space
- Result: /Phase2_Evaluation/Evaluation Results/evaluation_CosineSim_QueryResults.txt
- MAP = 0.387
- MRR = 0.643
- Mean P@5 = 0.323
- Mean P@20 = 0.203

Lucene
- Result: /Phase2_Evaluation/Evaluation Results/evaluation_Lucene_QueryResults.txt
- MAP = 0.412
- MRR = 0.680
- Mean P@5 = 0.365
- Mean P@20 = 0.200

BM25
- Result: /Phase2_Evaluation/Evaluation Results/evaluation_BM25_QueryResults.txt
- MAP = 0.313
- MRR = 0.561
- Mean P@5 = 0.304
- Mean P@20 = 0.161

## Tf Idf Enhancements
- Tf-Idf with psuedo relavance
  - Code: Task2_TfIdf_Pseudo_Relevance.py
  - Result: /5thRun_TfIdf_PsuedoRelevance/TfIdf_with_PseudoRel_QueryResults.txt
  - Evaluation: /Phase2_Evaluation/Evaluation Results/evaluation_TfIdf_with_PseudoRel_QueryResults.txt
    - MAP = 0.168
    - MRR = 0.272
    - Mean P@5 = 0.123
    - Mean P@20 = 0.106
  
- Tf-Idf with stopping
  - Code: Task3_TfIdf_Stopping.py
  - Result: /6thRun_TfIdf_Stopping/TfIdf_with_Stopping_QueryResults.txt
  - Evaluation: /Phase2_Evaluation/Evaluation Results/evaluation_TfIdf_with_Stopping_QueryResults.txt
    - MAP = 0.331
    - MRR = 0.572
    - Mean P@5 = 0.265
    - Mean P@20 = 0.174
  
- Tf-Idf with stemming
  - Code: Task3_TfIdf_StemText.py
  - Result: /Task3_RunWithStemming/TfIdf_Stem_QueryResults.txt
  
## BM25 With Stopping
  - Code: Implementation2_BM25_Stopping.py
  - Result: /5thRun_TfIdf_PsuedoRelevance/TfIdf_with_PseudoRel_QueryResults.txt
  - Evaluation: /Phase2_Evaluation/Evaluation Results/BM25_Stopping_QueryResults.txt
    - MAP = 0.395
    - MRR = 0.654
    - Mean P@5 = 0.373
    - Mean P@20 = 0.220
    
# Final Evaluation
- TfIdf_with_PseudoRel_QueryResults
  - MAP = 0.168
  - MRR = 0.272
  - Mean P@5 = 0.123
  - Mean P@20 = 0.106
  
- TfIdf_QueryResults
  - MAP = 0.289
  - MRR = 0.537
  - Mean P@5 = 0.227
  - Mean P@20 = 0.139
  
- CosineSim_QueryResults
  - MAP = 0.387
  - MRR = 0.643
  - Mean P@5 = 0.323
  - Mean P@20 = 0.203
  
- BM25_QueryResults
  - MAP = 0.313
  - MRR = 0.561
  - Mean P@5 = 0.304
  - Mean P@20 = 0.161
  
- TfIdf_with_Stopping_QueryResults
  - MAP = 0.331
  - MRR = 0.572
  - Mean P@5 = 0.265
  - Mean P@20 = 0.174

- BM25_Stopping_QueryResults
  - MAP = 0.395
  - MRR = 0.654
  - Mean P@5 = 0.373
  - Mean P@20 = 0.220

- Lucene_QueryResults
  - MAP = 0.412
  - MRR = 0.680
  - Mean P@5 = 0.365
  - Mean P@20 = 0.200
  
## Snippet Generation
As per Luhn’s algorithm, The significant sentence is calculated based on the occurrence of significant words which are words of medium frequency the document, where “medium” means that the frequency is between predefined high-frequency(8 in our case) and low-frequency(3 in our case) cutoff values. Given the significant words, portions of the sentence that are “bracketed” by these words are considered, with a limit set for the number of non-significant words that can be between two significant words (typically four).

After extracting the snippets for each query we highlighted the query terms in each snippet between <HL>..</HL> tags. The output file for BM25+stopping can be found at “Snippet_BM25Stopping_7thRun/snippets.txt”.

For some documents, no snippet could be generated as no contiguous significant words were found.

- Code: SnippetGeneration_ExtraCredits.py
- Results with snippets: /Snippet_BM25Stopping_7thRun/snippets.txt
