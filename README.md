<h1>Boosting the Unbiased Functional Enrichment Analysis (BUFET)</h1>
<h2>Table of contents</h2>
<p>
<ol>
<li><a href="#1-introduction">Introduction</a></li>
<li><a href="#2-compiling-bufet">Compiling BUFET</a></li>
<li><a href="#3-executing-bufet">Executing BUFET</a>
<br />&nbsp;&nbsp;3.1. <a href="#31-files-required">Files Required</a>
<br />&nbsp;&nbsp;3.2. <a href="#32-script-execution">Script Execution</a>
<br />&nbsp;&nbsp;3.3. <a href="#33-example">Example</a></li>
<li><a href="#4-reproduction-of-the-bufet-papers-experiments">Reproduction of the BUFET paper's experiments</a></li>
<li><a href="#5-contact">Contact</a></li>
</ol></p>

<h2>1. Introduction</h2>
<p>BUFET is an open-source software under the <a href="https://www.gnu.org/licenses/gpl-3.0.en.html">GPL v.3 licence</a>, designed to speed up the unbiased miRNA enrichment analysis algorithm as described by Bleazard et al. in <a href="http://bioinformatics.oxfordjournals.org/content/31/10/1592" target="_blank">in their paper</a>.</p>
<p>The BUFET algorithm generates an empirical distribution of genes targeted by miRNA and calculates p-values for related biological processes. Benjamini-Hochberg FDR correction produces a '*' or '**' for significance at 0.05 FDR and 0.01 FDR respectively.</p>

<h2>2. Compiling BUFET</h2>
<p>In order for the program to run, the system must comply with the following specifications:
<h4>Hardware:</h4>
<ul>
	<li>A system with at least 4GB of RAM</li>
</ul>
<h4>Software:</h4>
<ul>
	<li>Linux and MacOS</li>
    	<li>Python interpreter (>= version 2.7) that can run from the command line.</li>
    	<li>g++ 4.8 and above.</li>
</ul></p>

<p>In order to be able to run the BUFET script, you first need to compile the C++ program file. A Makefile is provided for that reason. The process is as follows:<br />
    <ol>
    <li><a href="https://github.com/diwis/BUFET/archive/master.zip">Download</a> the code and unzip the files.</li>
        <li>From the command line, navigate inside the folder containing the .cpp, .py and Makefile files.</li>
        <li>Run the following command:
            <pre><code>make</code></pre>
    </ol>
This will compile the code and create a .bin file. <b>The .bin file must be in the same folder as the .py at all times for the program to run</b>
</p>

<h2>3. Executing BUFET</h2>

<h3>3.1. Files required</h3>

<p><ol>
<li><b>Input miRNA file</b>, which is a text file containing only the names
of differentially expressed miRNAs, each on a separate line. For
example:<br />
        <pre><code>hsa-miR-132-5p
hsa-miR-132-3p</code></pre>
    </li>
    <li><b>Gene synonym data file</b> from NCBI, <a href='http://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/All_Mammalia.gene_info.gz' target="_blank">http://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/All_Mammalia.gene_info.gz</a>. Decompress the file with: <pre><code>gzip -d All_Mammalia.gene_info.gz</code></pre></li>
    <li><b>Gene annotation data file</b> retrieved by GO, KEGG, PANTHER, DisGeNet, etc. The file must contain the following CSV format for each line:
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
    <li><b>miRNA-gene interactions file</b>, which has the following CSV format for each line:
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

<h3>3.2. Script Execution</h3>

<p>Navigate inside the folder containing the .py and .bin files and run the following command:

<pre><code>python bufet.py [OPTIONS]</code></pre>
<!--By default--> The python script verifies that all input files exist, that they are not empty and that they have the correct format.
<!--Since the file check leads to increased execution times, it can be disabled by using the "--disable-file-check". However, we recommend that the file check remains enabled, since non-existing or empty files can crash the C++ core.-->

The script options are listed below:
<ul>
	<li>"-miRNA [filename]": path to the <b>input miRNA file</b>.</li>
	<li>"-interactions [filename]": path to <b>miRNA-gene interactions file</b>.</li>
	<li>"-synonyms [filename]": path to the <b>gene synonym data file</b>.</li>
	<li>"-ontology [filename]": path to <b>gene annotation data file</b>.</li>
    <li>"-output [filename]": path to output file. Created if it doesn't exist. Default filename: "output.txt"</li>
    <li>"-iterations [value]": number of random miRNA groups to test against. Default value: 10000</li>
    <li>"-processors [value]": the number of cores to be used in parallel. Default value: system cores-1.</li>
    <li>"-species [species_name]": specify either "human" or "mouse". Default species: "human"</li>
    <li>"--ensGO": must be added when using GO ontology data supplied by Ensembl</li>
    <li>"--miRanda": must be added when using prediction data from a miRanda run.</li>
    <li>"-miScore [score]": miRanda score thresold if the miRanda mode is specified. Default score: "155"</li>
    <li>"-miFree [energy]": miRanda free energy threshold if the miRanda mode is specified. Default energy: "-20.0"</li>
    <!--<li>"--disable-interactions-check": disables the validation for the interactions file (not recommended).</li>
    <li>"--disable-ontology-check": disables the validation for the ontology file (not recommended).</li>
    <li>"--disable-synonyms-check": disables the validation for the synonyms file (not recommended).</li>
    <li>"--disable-file-check": disables the validation for all files (not recommended).</li>-->
    <li>'-h" or "--help": print help message and exit</li>
</ul><br />
</p>

<h3>3.3. Example</h3>
<p><ol>
<li><a href="https://github.com/diwis/BUFET/archive/master.zip">Download</a> the code and compile it according to the instructions (See section "Compiling BUFET").</li>
    <li><a target="_blank" href="http://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/All_Mammalia.gene_info.gz">Download</a> synonym data from NCBI.</li>
    <li>Place all files in the same folder as the .py and .bin files.</li>
    <li>Assuming that your current folder contains the .py and .bin files and all input files are located in the example folder, run an experiment as follows (or add the right paths for each file, accordingly):
	    <pre><code>python bufet.py -interactions example/interactions_example.csv -ontology example/ontology_example.csv -output output.txt -miRNA XX -synonyms example/All_Mammalia.gene_info</code></pre>
    where XX is the one of the sample input miRNA files (example/input_example5.txt, example/input_example10.txt, example/input_example25.txt, input_example50.txt).</li>
    <li> The file "output.txt" contains the results of the analysis.</li>
</ol></p>

<h2>4. Reproduction of the BUFET paper's experiments</h2>
<p>
<ol>
<li><a href="https://github.com/diwis/BUFET/archive/master.zip">Download</a> the code and compile it according to the instructions (See section "Compiling the code").</li>
    <li>Files required for the reproduction of the experiments:
    	<ul>
	<li>GO gene annotations for Ensembl v.69</li>
	<li>microT miRNA-gene interactions for miRBase v.21 and Ensembl v.69</li>
	<li>miRanda miRNA-gene interactions for miRBase v.21 and Ensembl v.69</li>
	<li>miRNA input files</li>
	<li>Synonym data from NCBI</li>
	</ul>
	All files listed above can be found in a compressed file <a href="http://carolina.imis.athena-innovation.gr/bufet/reproduction_files.zip">here</a>.
    </li>
    <li>Decompress the file:
    <pre><code>unzip reproduction_files.zip</code></pre>
    <li>Assuming that your current folder contains the .py, .bin, and all input files, run an experiment as follows (or add the right paths for each file, accordingly):
	    <pre><code>python bufet.py -interactions microT_dataset.csv -ontology annotation_dataset.csv -output output.txt -miRNA input/exp1/miRNA-5.txt -synonyms All_Mammalia.gene_info -processors 1 -iterations 10000</code></pre>
This will run a BUFET analysis for an input of 5 miRNAs using microT interactions (random miRNA groups used: 10000, cores used: 1).  The file "output.txt" contains the results of the analysis.</li>

<li>Reproduce the rest of the experiments. Repeat the analysis for:
	<ul>
		<li>every input miRNA file in folders exp1, exp2, ..., exp10 (miRNA-5.txt, miRNA-10.txt, miRNA-50.txt, miRNA-100.txt). Examples: "input/exp7/miRNA-50.txt", "input/exp4/miRNA-100.txt"</li>
		<li>both types of miRNA-gene interactions data files: microT_dataset.csv and miRanda_dataset.csv.
		<li>10000, 100000 and 1000000 random miRNA groups.</li>
		<li>1 and 7 cores.</li>
</ul>

<b>Examples</b>: 
<ul>
	<li>(miRanda interactions, 10 miRNAs, 100000 random groups, 7 cores):
<pre><code>python bufet.py -interactions miRanda_dataset.csv -ontology annotation_dataset.csv -output output.txt -miRNA input/exp8/miRNA-10.txt -synonyms All_Mammalia.gene_info -processors 7 -iterations 100000</code></pre></li>
	<li>(microT interactions, 50 miRNAs, 1000000 random groups, 7 cores):
<pre><code>python bufet.py -interactions microT_dataset.csv -ontology annotation_dataset.csv -output output.txt -miRNA input/exp3/miRNA-50.txt -synonyms All_Mammalia.gene_info -processors 7 -iterations 1000000</code></pre></li>
	<li>(miRanda interactions, 100 miRNAs, 10000 random groups, 1 core):
<pre><code>python bufet.py -interactions miRanda_dataset.csv -ontology annotation_dataset.csv -output output.txt -miRNA input/exp2/miRNA-100.txt -synonyms All_Mammalia.gene_info -processors 1 -iterations 10000</code></pre></li>
</ul>
</ol></p>

<h2>5. Contact</h2>
<p>For any problems with the execution of this code please contact us at zagganas@imis.athena-innovation.gr</p>
