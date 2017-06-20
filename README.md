# Boosting the Unbiased Functional Enrichment Analysis (BUFET)
<h2>Table of contents</h2>
<p>
<ol>
<li><a href="#introduction">Introduction</a></li>
<li><a href="#system-requirements">System Requirements</a></li>
<li><a href="#compiling-the-code">Compiling the code</a></li>
<li><a href="#required-files">Required Files</a></li>
<li><a href="#script-execution">Script Execution</a></li>
<li><a href="#example-execution">Example Execution</a></li>
<li><a href="#reproduction-of-an-experiment-in-the-manuscript-for-comparison-with-empiricalgo">Reproduction of an experiment in the manuscript for comparison with EmpiricalGO</a></li>
</ol></p>

<h2>Introduction</h2>
<p>BUFET is a free software designed to speed up the unbiased miRNA enrichment analysis algorithm as described by Bleazard et al. in <a href="http://bioinformatics.oxfordjournals.org/content/31/10/1592" target="_blank">in their paper</a></p>
<p>The BUFET algorithm generates an empirical distribution of genes targeted by miRNA and calculates p-values for related biological processes. Benjamini-Hochberg FDR correction produces a '*' or '**' for significance at 0.05 FDR and 0.01 FDR respectively.</p>

<h2>System Requirements</h2>
<p>In order for the program to run, the system must comply with the following specifications:
<ul>
	<li>Linux or other unix-like environments (Mac OS).</li>
    	<li>Python interpreter (>= version 2.7) that can run from the command line</li>
    	<li>g++ 4.8 and above</li>
</ul>
Additionally, due to the heavy computational load of the program, a multicore environment is recommended but not a prerequisite.</p>

<h2>Compiling the code</h2>

<p>In order to be able to run the BUFET script, you first need to compile the C++ program file. A Makefile is provided for that reason. The process is as follows:<br />
    <ol>
        <li>From the command line, navigate inside the folder containing the .cpp, .py and Make files</li>
        <li>Run the following command:
            <pre><code>make</code></pre>
    </ol>
This will compile the code and create a .bin file. <b>The .bin file must be in the same folder as the .py at all times for the program to run</b>
</p>

<h2>Required Files</h2>

<p>This script requires files from several public datasets, which must
be downloaded by the user. Files required in order to run the script are described below:

<ol>
    <li>Input miRNA list, which is a text file containing only the names
of differentially expressed miRNAs, each on a separate line. For
example:<br />
        <pre><code>hsa-miR-132-5p
hsa-miR-132-3p</code></pre>
    </li>
    <li>Gene synonym data from NCBI, <a href='ftp://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/All_Mammalia.gene_info.gz' target="_blank">ftp://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/All_Mammalia.gene_info.gz</a>. Decompress the file with: <pre><code>gzip -d All_Mammalia.gene_info.gz</code></pre></li>
    <li>A list of pathway annotation data retrieved by GO, KEGG, PANTHER, DisGeNet, etc. The data must be in the following CSV format:
    <pre><code>gene_name|pathway_id|pathway_name</code></pre>
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
	Note that in this case you will need to use the <b>"--ensGO"</b> option in order for the script to execute correctly! 
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
	In this case you will need to use the <b>"--miRanda"</b> option in order for the script to execute correctly!
    </li>
   </ol>
Note that all files listed above can contain header lines starting with the <b>"#"</b> character.</p>

<h2>Script Execution</h2>

<p>Navigate inside the folder containing the .py and .bin files and run the following command:

<pre><code>python bufet.py [OPTIONS]</code></pre>
By default the python script verifies that all input files exist, that they are not empty and that they have the correct format. Since the file check leads to increased execution times, it can be disabled by using the "--disable-file-check". However, we recommend that the file check remains enabled, since non-existing or empty files can crash the C++ core.

The script options are listed below:
<ul>
    <li>"-miRNA [filename]": the input miRNA list</li>
    <li>"-interactions [filename]": path to miRNA-gene interactions file.</li>
    <li>"-synonyms [filename]": path to gene synonyms file.</li>
    <li>"-output [filename]": path to output filename. Default filename: "output.txt"</li>
    <li>"-ontology [filename]": path to ontology data.</li>
    <li>"-iterations [value]": number of random miRNA groups to test against. Default value: "10000"</li>
    <li>"-processors": integer value for the number of threads to be used in a parallel parallel. Default value: system cores-1.</li>
    <li>"-species [species_name]": specify either "human" or "mouse". Default species: "human"</li>
    <li>"--ensGO": must be added when using GO ontology data supplied by Ensembl</li>
    <li>"--miRanda": must be added when using prediction data from miRanda run.</li>
    <li>"-miScore [score]": miRanda score thresold if the miRanda mode is specified. Default score: "155"</li>
    <li>"-miFree [energy]": miRanda free energy threshold if the miRanda mode is specified. Default energy: "-20.0"</li>
    <li>"--disable-file-check": disables the input file validation (not recommended).
    <li>'-h" or "--help": print help message and exit</li>
</ul><br />
</p>

<h2>Example Execution</h2>
<p><ol>
    <li>Download the code and compile it according to the instructions (See section "Compiling the code")</li>
    <li>Download synonym data from NCBI. (For a link, see section "Required files")</li>
    <li>Place all files in the same folder as the .py and .bin files.</li>
    <li>From inside the folder containing all files execute the following command to run the example:
	    <pre><code>python bufet.py -interactions interactions_example.csv -ontology ontology_example.csv -output output.txt 
	    -miRNA input_exampleXX.txt -synonyms All_Mammalia.gene_info</code></pre>
    where XX is the number of miRNAs in the sample input file (5,10,25,50).</li>
    <li> The file "output.txt" contains the results of the analysis</li>
</ol></p>

<h2>Reproduction of an experiment in the manuscript for comparison with EmpiricalGO</h2>
<p>In order to reproduce one of the experiments detailed in the paper manuscript please follow the instructions below:
<ol>
    <li>Download the code and compile it according to the instructions (See section "Compiling the code")</li>
    <li>Download the special file form (that can be run by both BUFET and EmpiricalGO) for the interaction and annotation datasets, as detailed in the "Availability of Data and Material" section of the manuscript (links also provided below). Then, download the input files from the link provided in the manuscript (also provided below).
    	<ul>
	<li>Annotation data: <a target="_blank" href="http://carolina.imis.athena-innovation.gr/bufet/annotation_special_dataset.csv.gz">http://carolina.imis.athena-innovation.gr/bufet/annotation_special_dataset.csv.gz</a></li>
	<li>microT special form dataset: <a target="_blank" href="http://carolina.imis.athena-innovation.gr/bufet/microT_special_dataset.csv.gz">http://carolina.imis.athena-innovation.gr/bufet/microT_special_dataset.csv.gz</a></li>
	<li>miRanda special form dataset: <a target="_blank" href="http://carolina.imis.athena-innovation.gr/bufet/miRanda_special_dataset.csv.gz">http://carolina.imis.athena-innovation.gr/bufet/miRanda_special_dataset.csv.gz</a></li>
	<li>miRNA input files: <a target="_blank" href="http://carolina.imis.athena-innovation.gr/bufet/experiment_input.tar.gz">http://carolina.imis.athena-innovation.gr/bufet/experiment_input.tar.gz</a></li>
	</ul>
    </li>
    <li>Uncompress the miRNA input files with
    <pre><code>tar xzf experiment_input.tar.gz</code></pre>
    <li>Uncompress the interactions file with:
    <pre><code>gzip -d XX_special_dataset.csv.gz</code></pre>
    where XX can either be "microT" or "miRanda"</li>
    <li>Uncompress the annotations file with:
    <pre><code>gzip -d annotation_special_dataset.csv.gz</code></pre></li>
    <li>Download synonym data from NCBI. (For a link, see section "Required files")</li>
    <li>Place all files in the same folder as the .py and .bin files. If not, modify file paths accordingly.</li>
    <li>From inside the folder containing all files execute the following command to run the experiment:
	    <pre><code>python bufet.py -interactions XX_special_dataset.csv -ontology annotation_special_dataset.csv -output output.txt 
	    -miRNA input/expYY/miRNA-ZZ.txt -synonyms All_Mammalia.gene_info -processors PP --ensGO --miRanda</code></pre>
    where:
    	<ul>
    		<li>X is either microT or miRanda</li>
		<li>Y is the number of the experiment (1-10)</li>
		<li>ZZ is the number of miRNAs in the experiment input file (5,10,50,100).</li>
		<li>PP is the number of processors</li>
	</ul>
    <li> The file "output.txt" contains the results of the analysis</li>
</ol></p>



<h2>Contact</h2>
<p>For any problems with the execution of this code please contact us at zagganas@imis.athena-innovation.gr</p>
