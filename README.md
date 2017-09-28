# Overview
This project was intended to design and develop a sophisticated search engine for the CACM dataset that can produce relavant documents(top 100) for a given query. Project was carried out in following phases:
- [Index creation and text processing](#indexer-and-text-processor)
- [Implemention of base retrieval models - Tf-Idf, Cosine Vector Space, BM25](#base-retrieval-models)
- [Evaluate each model over the CACM dataset based on standard parameters MAP, MRR, P@K and Precision & Recall](#base-evaluation)
- [Choose any one models(Tf-Idf for this project) and enhance it by incorporating query expansion(psuedo-relavance) and query processing(stopping, stemming) techniques](#enhancements)
- [Choose the best base model(BM25) and enhance it by query processing techinque "stopping"](#bm25-stopping)
- [Evaluate the enhanced models over the CACM dataset based on standard parameters MAP, MRR, P@K and Precision & Recall and tabulate the results](#final-evaluation)
- [Choose the best model(BM25 with stopping) and display the query results with summary highlighting the query words from each relavant document](#snippet-generation)

## Indexer And Text Processor
Text Processor code files
- For raw CACM corpus(/corpus) - Task1_HtmlTextExtracter.py
- For stemmed CACM corpus(/StemCorpus) - Task3_TextExtracter_StemText.py

Text Process output files
- /PlainText: Processed files of raw CACM corpus
- /StemmedText: Processed files stemmed CACM corpus

Indexer code files
- For raw CACM corpus - Task1_InvertedIndexer.py
- For stemmed CACM corpus - Task3_InvertedIndexer_StemText

Indexer output files
- /MyIndex
  - OneGram_DfTable.txt - Unigram document frequency index for raw CACM dataset(term, docId, df)
  - OneGram_DfTable_Stem.txt - Unigram document frequency index for stemmed CACM dataset(term, docId, df)
  - OneGram_TfTable.txt - Unigram term frequency index for raw CACM dataset(term, tf)
  - OneGram_TfTable_Stem.txt - Unigram term frequency index for stemmed CACM dataset(term, tf)
  
- Stoplists
  - /MyIndex/Task3_Stoplist_OneGram.txt - Stopwords for raw CACM dataset
  - /MyIndex/Task3_Stoplist_OneGram_Stem.txt - Stopwords for stemmed CACM dataset


All outputs:
1stRun(TfIdf baseline): ~\1stRun_TfIdf_Baseline\TfIdf_QueryResults.txt
2ndRun(CosineSim baseline: ~\2ndRun_CosinSim_Baseline\CosineSim_QueryResults.txt
3rdRun(Lucene baseline): ~\3rdRun_Lucene_Baseline\result\Lucene_QueryResults.txt
4thRun(BM25 baseline): ~\4thRun_BM25_Baseline\BM25_QueryResults.txt
5thRun(TfIdf+pseudo-relevance): ~\5thRun_TfIdf_PsuedoRelevance\TfIdf_with_PseudoRel_QueryResults.txt
6thRun(TfIdf+Stopping): ~\6thRun_TfIdf_Stopping\TfIdf_with_Stopping_QueryResults.txt
7thRun(BM25+Stopping): ~\7thRun_BM25_Stopping\BM25_Stopping_QueryResults.txt
8thRun(TfIdf+Stemming): ~\Task3_RunWithStemming\TfIdf_Stem_QueryResults.txt

Evaluation Results:
- All evaluation results can be found at ~\Project\Phase2_Evaluation\Evaluation Results\ folder.
- summary file contains the summarized results for each of 7 system i.e. (MRR, MAP, P@5, P@20).
- Each query result file is Precision & Recall table for each run.

Snippet Generation:
- Snippet for BM25 with stopping for all 64 queries can be found at ~\Snippet_BM25Stopping_7thRun\snippets.txt

Source Codes(Python files):
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

Source Codes(Java files):
- ~\Project\3rdRun_Lucene_Baseline\src\com\lucene\HW4.java - Lucene baseline model

Setup and compile python files:

***********************The files are build on Python version 2.7x****************************

In windows:
Open the python editor IDLE from the menu, and open xxxx.py(eg: Task-1.py for Task-1), then press F5 to run it.

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

Input, Output and Path Information for python files:

- All the file paths are included at the top in source files under import statements
- MyIndex folder contains all the indexes used to score documents.
- PlainText folder contains the plain text generated from raw html files.
- StemText folder contains the stemmed text generated from stemmed raw html files.

- corpus folder contains the raw htnml files of cacm dataset.
- StemCorpus folder contains the raw html files of cacm stemmed dataset.
- Input queries are stored in list "InputQueries" in source code which are read from cacm.query and cacm.query_stem.txt files respectively.
  It can be modified or added with any number of queries. The ranker will run sequentially for each query in list.
- The output files will be generated in the same directory as source file.

- For evaluation, put the 64 query result file in ~\Project\Phase2_Evaluation\Runs which need Evaluation\ folder.
- Remove the first header line from each file.
- The result will be generated in ~\Project\Phase2_Evaluation\Evaluation Results\ folder.

Input, Output and Path Information for java files:
- The input file folder is ~\Project\3rdRun_Lucene_Baseline\document\
- The indexes will be created at ~\Project\3rdRun_Lucene_Baseline\index\ folder.
- The result will be produced at ~\Project\3rdRun_Lucene_Baseline\result\ folder.
