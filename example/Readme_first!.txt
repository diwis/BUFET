1. Download the code and compile it according to the instructions
2. Download synonym data from NCBI.
3. Place all files in the same folder.
4. From inside the folder containing all files execute the following command to run the example:

	python bufet.py -interactions interactions_example.csv -ontology ontology_example.csv -output output.txt -miRNA input_exampleXX.txt -synonyms gene_info
	
	where XX is the number of miRNAs in the sample input file (5,10,25,50).

5. The file "output.txt" contains the results of the analysis
