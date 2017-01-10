import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.ArrayList;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;


public class HW4 {
    //private static Analyzer sAnalyzer = new StandardAnalyzer(Version.LUCENE_47);
    private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);

    private IndexWriter writer;
    private ArrayList<File> queue = new ArrayList<File>();
    
    public static String[] readline() throws IOException {
    	int i =0;
		BufferedReader reader = new BufferedReader(new FileReader("cacm_processed_query_token.txt"));
	    String[] res = new String[64];
	    while(true){
	        String line = reader.readLine();
	        if(line == null){
	            break;
	        }
	        res[i] = line;
	        i++;
	    }
	    return res;
    }

    public static void main(String[] args) throws IOException {
    String[] query = readline();
    for (String q : query) {
    	System.out.println(q);
    }
	
    String indexLocation = null;
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    String s = "index";
    
    
    File dir = new File("index");
    for (File file: dir.listFiles()) 
    	file.delete();
    
    HW4 indexer = null;

	try {
	    indexLocation = s;
	    indexer = new HW4(s);
	} catch (Exception ex) {
	    System.out.println("Cannot create index..." + ex.getMessage());
	    System.exit(-1);
	}

	
	try {
		s = "document";
		indexer.indexFileOrDirectory(s);
    } 
	catch (Exception e) {
    	System.out.println("Error indexing " + s + " : "
    			+ e.getMessage());
    }
	// ===================================================
	// after adding, we always have to call the
	// closeIndex, otherwise the index is not created
	// ===================================================
	indexer.closeIndex();

	// =========================================================
	// Now search
	// =========================================================
	
	IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
			indexLocation)));
	IndexSearcher searcher = new IndexSearcher(reader);
	PrintWriter writer = new PrintWriter("result/Lucene_QueryResults.txt", "UTF-8");
	for (int i = 0; i < query.length; i++) {
			TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);
			
		try {
			s = query[i];
			Query q = new QueryParser(Version.LUCENE_47, "contents",
					sAnalyzer).parse(s);
			searcher.search(q, collector);
			ScoreDoc[] hits = collector.topDocs().scoreDocs;
			
			// 4. display results
		    int queryId = i + 1;
		    int count = 1;
			for (int j = 0; j < hits.length; ++j) {
			    int docId = hits[j].doc;
			    Document d = searcher.doc(docId);
			    String name = d.get("filename");
			    String documentId = name.substring(0, name.length() - 5);
                            String x = documentId.substring(5,9);
                           
			    writer.println(queryId + " Q0 " + x + " " + count + " " +hits[j].score + " Lucene");
			    count++;
			}
			
		} catch (Exception e) {
			System.out.println("Error searching " + s + " : "
					+ e.getMessage());
			break;
		}
		
	}
	writer.close();
	
}

    
    HW4(String indexDir) throws IOException {

	FSDirectory dir = FSDirectory.open(new File(indexDir));

	IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47,
		sAnalyzer);

	writer = new IndexWriter(dir, config);
    }

    
    public void indexFileOrDirectory(String fileName) throws IOException {
	// ===================================================
	// gets the list of files in a folder (if user has submitted
	// the name of a folder) or gets a single file name (is user
	// has submitted only the file name)
	// ===================================================
	addFiles(new File(fileName));

	int originalNumDocs = writer.numDocs();
	for (File f : queue) {
	    FileReader fr = null;
	    try {
		Document doc = new Document();

		// ===================================================
		// add contents of file
		// ===================================================
		fr = new FileReader(f);
		doc.add(new TextField("contents", fr));
		doc.add(new StringField("path", f.getPath(), Field.Store.YES));
		doc.add(new StringField("filename", f.getName(),
			Field.Store.YES));

		writer.addDocument(doc);
		//System.out.println("Added: " + f);
	    } catch (Exception e) {
		System.out.println("Could not add: " + f);
	    } finally {
		fr.close();
	    }
	}

	int newNumDocs = writer.numDocs();
	System.out.println("");
	System.out.println("************************");
	System.out
		.println((newNumDocs - originalNumDocs) + " documents added.");
	System.out.println("************************");

	queue.clear();
    }

    private void addFiles(File file) {

	if (!file.exists()) {
	    System.out.println(file + " does not exist.");
	}
	if (file.isDirectory()) {
	    for (File f : file.listFiles()) {
		addFiles(f);
	    }
	} else {
	    String filename = file.getName().toLowerCase();
	    // ===================================================
	    // Only index text files
	    // ===================================================
	    if (filename.endsWith(".htm") || filename.endsWith(".html")
		    || filename.endsWith(".xml") || filename.endsWith(".txt")) {
		queue.add(file);
	    } else {
		System.out.println("Skipped " + filename);
	    }
	}
    }

    public void closeIndex() throws IOException {
	writer.close();
    }
}