# Boosting the Unbiased Functional Enrichment Analysis (BUFET)

<h2>Introduction</h2>
<p>BUFET is a free software designed to speed up the unbiased miRNA enrichment analysis algorithm for GO categories and KEGG pathways as described by Bleazard et al. in <a href="http://bioinformatics.oxfordjournals.org/content/31/10/1592" target="_blank">in their paper</a></p>
<p>The BUFET algorithm generates an empirical distribution of genes targeted by miRNA and calculates p-values for related GO categories. Benjamini-Hochberg FDR correction produces a '*' or '**' for significance at 0.05 FDR and 0.01 FDR, as in the original script.</p>

<h2>System Requirements</h2>
<p>In order for the program to run the system must comply with the following specifications:
<ul>
    <li>Python interpreter that can run from the command line</li>
    <li>g++ 4.8 and above</li>
</ul>
Additionally, due to the heavy computational load of the program, a multicore environment is recommended but not a prerequisite.</p>

<p>In order to be able to run the BUFET script you first need to compile the C++ program file. A Makefile is provided for that reason. The process is as follows:<br />
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
    <li>Ensembl formatted annotations of genes to GO terms. From <a href="http://www.ensembl.org/biomart" target="_blank">http://www.ensembl.org/biomart</a> select Ensembl Genes XX
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
        
        *Instead of the file downloaded form the Ensembl biomart, you can also specify GO term/KEGG pathway gene annotation in the following format:
        <pre><code>Gene_Name|term_Accession|term_Name</code></pre>
        In this case you will need to use the "--altOntology" option in order for the script to execute correctly.
        
    </li>

    <li>Output from miRanda target prediction run. This requires:
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
            <li>miRanda software from <a href='http://www.microrna.org/microrna/getDownloads.do' target="_blank">http://www.microrna.org/microrna/getDownloads.do</a></li>

                To generate correct format for script input, please run as: 

                <pre><code>miranda hsa-mature-miRNA.fa ensembl3utr.txt -quiet | grep '>>hsa' >  miRandaPredictions.txt </code></pre>
            </li>
        </ul>
        *Instead interactions provided by miRanda, you can also specify interaction data in a file which has the following format for each line:
        <pre><code>miRNA|Gene_Name</code></pre>
        In this case you will need to use the "--altInteractions" option in order for the script to execute correctly.
    </li>
    <li>Gene synonym data from NCBI, <a href='ftp://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/All_Mammalia.gene_info.gz' target="blank">ftp://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/All_Mammalia.gene_info.gz</a></li>
</ol>

</p>

<h2>Script Execution</h2>

<p>Run the following command:

<pre><code>python bufet.py [OPTIONS]</code></pre>

The script options are listed below:
<ul>
    <li>"-miRNA [filename]": the input miRNA list</li>
    <li>"-miRanda [filename]": miRanda predictions. Default filename: "humanfullpredictions.txt"</li>
    <li>"-miScore [score]": miRanda score thresold. Default score: "155"</li>
    <li>"-miFree [energy]": miRanda free energy threshold. Default energy: -20.0</li>
    <li>"-synonyms [filename]": gene synonyms. Default filename: "gene_info"</li>
    <li>"-output [filename]": output filename. Default filename: "output.txt"</li>
    <li>"-ontology [filename]": GO ontology data. Default filename: "hsa-ensembl-go.txt"</li>
    <li>"-processors": integer value for processors to be used in parallel. Default value: system cores-1.</li>
    <li>"-species [species_name]": specify "human" or "mouse". Default species: "human"</li>
    <li>"--altOntology": use the alternate file format for gene annotation data</li>
    <li>"--altInteractions": use the alternate file format for interaction data</li>
</ul>
</p>
