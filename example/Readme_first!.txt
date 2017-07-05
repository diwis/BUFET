1. Download the code and compile it according to the instructions (See section "Compiling BUFET").
2. Download synonym data from NCBI.
3. Place all files in the same folder as the .py and .bin files.
4. Assuming that your current folder contains the .py and .bin files and all input files are located in the example folder, run an experiment as follows (or add the right paths for each file, accordingly):
	
	python bufet.py -interactions example/interactions_example.csv -ontology example/ontology_example.csv -output output.txt -miRNA XX -synonyms example/All_Mammalia.gene_info
	where XX is the one of the sample input miRNA files (example/input_example5.txt, example/input_example10.txt, example/input_example25.txt, input_example50.txt).

5. The file "output.txt" contains the results of the analysis
