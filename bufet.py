import multiprocessing
import sys
import subprocess
import re

patt=re.compile('--.*')

commandLine=sys.argv
options = {}

options['-processors'] = str(max(1,multiprocessing.cpu_count() - 1))
options['-iterations'] = '10000'
options['-miRNA'] = ''
options['-ontology'] = 'ontology.csv'
options['-interactions'] = 'interactions.csv'
options['-output'] = 'output.txt'
options['-species'] = 'human'
options['-synonyms'] = 'gene_info'
options['-miRanda']='no'
options['-ensGO']='no'
options['-miScore'] = '155.0'
options['-miFree'] = '-20.0'

#read arguments
for i in range(len(commandLine)):
	if patt.match(commandLine[i]):
		options[commandLine[i][1:]]='yes'
		continue
	if commandLine[i] in options:
		options[commandLine[i]] = commandLine[i+1]
		if i+1>=len(commandLine):
			break

if options['-miRanda']=='no':
	altInt='1'
else:
	altInt='0'

if options['-ensGO']=='no':
	altOnt='1'
else:
	altOnt='0'

if options['-miRNA']=='':
	print('Error: No input specified!')
	exit(1)

try:
	f=open(options['-interactions'],'r')
	f.close()
except:
	print('Error: Interactions file not specified or file could not be opened!')
	exit(2)

try:
	f=open(options['-ontology'],'r')
	f.close()
except:
	print('Error: Ontology file not specified or file could not be opened!')
	exit(3)

try:
	f=open(options['-synonyms'],'r')
	f.close()
except:
	print('Error: Synonyms file not specified or file could not be opened!')
	exit(4)

return_code=subprocess.call(['./bufet',options['-interactions'],options['-output'],options['-miRNA'],options['-ontology'], options['-iterations'], options['-processors'],options['-synonyms'],options['-miFree'],options['-miScore'],options['-species'],altInt,altOnt])