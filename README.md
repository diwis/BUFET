# Boosting the Unbiased Functional Enrichment Analysis (BUFET)

<h2>Introduction</h2>
<p>BUFET is a free software designed to speed up the unbiased miRNA enrichment analysis algorithm as described by Bleazard et al. in <a href="http://bioinformatics.oxfordjournals.org/content/31/10/1592" target="_blank">in their paper</a></p>
<p>The BUFET algorithm generates an empirical distribution of genes targeted by miRNA and calculates p-values for related biological processes. Benjamini-Hochberg FDR correction produces a '*' or '**' for significance at 0.05 FDR and 0.01 FDR</p>

<h2>System Requirements</h2>
<p>In order for the program to run, the system must comply with the following specifications:
<ul>
	<li>Linux or other unix-like environments (OSX).</li>
    	<li>Python interpreter (>= version 2.7) that can run from the command line</li>
    	<li>g++ 4.8 and above</li>
</ul>
Additionally, due to the heavy computational load of the program, a multicore environment is recommended but not a prerequisite.</p>

<p>In order to be able to run the BUFET script, you first need to compile the C++ program file. A Makefile is provided for that reason. The process is as follows:<br />
    <ol>
        <li>Navigate inside the folder containing the .cpp, .py and Make files</li>
        <li>Run the following command:
            <pre><code>make</code></pre>
    </ol><br />

<h2>Required Files:</h2>

<p>This script requires reference to several public datasets, which must
be downloaded by the user. Files needed to run the script are described below:

<ol>
    <li>Input miRNA list, which is a text file containing only the names
of differentially expressed miRNAs, each on a separate line. For
example:<br />
        <pre><code>hsa-miR-132-5p
hsa-miR-132-3p</code></pre>
    </li>
    <li>A list of pathway annotation data retrieved by GO, KEGG, PANTHER, DisGeNet, etc. The data must be in the following CSV format:
    <pre><code>gene_name|pathway/category_id|pathway/category_name</code></pre>
    *Alternatively, a list of Ensembl formatted annotations of genes to GO terms can be supplied. From <a href="http://www.ensembl.org/biomart" target="_blank">http://www.ensembl.org/biomart</a> select Ensembl Genes XX
    and species of interest. 
        In attributes select in the following order:
        <ul>
            <li>Ensembl Gene ID</li>
            <li>Ensembl Transcript ID</li>
            <li>Associated Gene Name</li>
            <li>GO Term Accession</li>
            <li>GO Term Name</li>
            <li>GO Term Definition</li>
            <li>GO domain</li>
        </ul>
        <b>Note that in this case you will need to use the "--ensGO" option in order for the script to execute correctly!</b>  
    </li>
    <li>miRNA-gene interaction data in a file which has the following format for each line:
        <pre><code>miRNA_name|gene_name</code></pre>
        *The user can also use the output from miRanda target prediction run. This requires:
        <ul>
            <li>FASTA sequences for known mature miRNA from <a href='http://www.mirbase.org/ftp.shtml' target='_blank'>http://www.mirbase.org/ftp.shtml</a> filtered for species of interest</li>
            <li>FASTA sequences for 3' UTR of genes from <a href='http://www.biomart.org/' target='_blank'>http://www.biomart.org/</a>
                Select the the following order:
                <ul>
                    <li>Sequence Retrieval</li>
                    <li>3' UTR</li>
                    <li>headers</li>
                    <li>Ensembl Gene ID</li>
                    <li>Ensembl Transcript ID</li>
                    <li>Associated Gene Name</li>
                </ul>
                After the file has been downloaded, remove entries with "Sequence Unavailable".
            </li>
            <li>miRanda software from <a href='http://www.microrna.org/microrna/getDownloads.do' target="_blank">http://www.microrna.org/microrna/getDownloads.do</a>.
                To generate correct format for script input, please run as: 
                <pre><code>miranda hsa-mature-miRNA.fa ensembl3utr.txt -quiet | grep '>>hsa' >  miRandaPredictions.txt </code></pre>
            </li>
        </ul>
        <b>In this case you will need to use the "--miRanda" option in order for the script to execute correctly!</b>
    </li>
    <li>Gene synonym data from NCBI, <a href='ftp://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/All_Mammalia.gene_info.gz' target="_blank">ftp://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/All_Mammalia.gene_info.gz</a></li>
</ol>

Note that all files listed above <b>must not contain any header lines</b>!
</p>

<h2>Script Execution</h2>

<p>Navigate inside the folder containing the .py and .bin files and run the following command:

<pre><code>python bufet.py [OPTIONS]</code></pre>

The script options are listed below:
<ul>
    <li>"-miRNA [filename]": the input miRNA list</li>
    <li>"-interactions [filename]": miRNA-gene interactions. Default filename: "interactions.csv"</li>
    <li>"-synonyms [filename]": gene synonyms. Default filename: "gene_info"</li>
    <li>"-output [filename]": output filename. Default filename: "output.txt"</li>
    <li>"-ontology [filename]": ontology data. Default filename: "ontology.csv"</li>
    <li>"-iterations [value]": number of random miRNA groups to test against. Default value: "10000"</li>
    <li>"-processors": integer value for processors to be used in parallel. Default value: system cores-1.</li>
    <li>"-species [species_name]": specify "human" or "mouse". Default species: "human"</li>
    <li>"--ensGO": use GO ontology data supplied by Ensembl</li>
    <li>"--miRanda": use prediction data from miRanda run.</li>
    <li>"-miScore [score]": miRanda score thresold if the miRanda mode is specified. Default score: "155"</li>
    <li>"-miFree [energy]": miRanda free energy threshold if the miRanda mode is specified. Default energy: "-20.0"</li>
</ul><br />

<h2>Example Execution</h2>
<ol>
    <li>Download the code and compile it according to the instructions</li>
    <li>Download synonym data from NCBI.</li>
    <li>Place all files in the same folder.</li>
    <li>From inside the folder containing all files execute the following command to run the example:
	    <pre><code>python bufet.py -interactions interactions_example.csv -ontology ontology_example.csv -output output.txt -miRNA input_exampleXX.txt -synonyms gene_info</code></pre>
    where XX is the number of miRNAs in the sample input file (5,10,25,50).</li>
    <li> The file "output.txt" contains the results of the analysis</li>
</ol>
<h2>Contact</h2>
For any problems with the execution of this code please contact us at zagganas@imis.athena-innovation.gr
</p>
