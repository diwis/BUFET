import sys

def matchSysnonyms(synonyms, ontology, ontologyGenes, interactions):
    
    newInt={}
    
    for mirna in interactions:
        if mirna not in newInt:
            newInt[mirna]=set()
        for gene in interactions[mirna]:
            newGene=gene
            if gene not in ontologyGenes:
                if gene in synonyms:
                    geneSynonyms=synonyms[gene]
                    for synonym in geneSynonyms:
                        if synonym in ontologyGenes:
                            newGene=synonym
                            break
                
            newInt[mirna].add(gene)
    
    return newInt

def readOntology(filename):
    ontology={}
    ontologyNames={}
    ontologyGenes=set()

    f=open(filename,'r')
    for line in f:
        line=line.strip().split('|')
        gene=line[0]
        cat=line[1]
        name=line[2]

        if cat not in ontologyNames:
            ontologyNames[cat]=name
        if cat not in ontology:
            ontology[cat]=set()
        ontology[cat].add(gene)
        ontologyGenes.add(gene)
    f.close()

    return ontology,ontologyNames,ontologyGenes

def readInteractions(filename):
    interactions={}

    f=open(filename,'r')
    for line in f:
        line=line.strip().split('|')
        mirna=line[0]
        gene=line[1]

        if mirna not in interactions:
            interactions[mirna]=set()
        interactions[mirna].add(gene)
    f.close()

    return interactions

def readSynonyms(filename, taxid):
    synonyms = {}
    f= open(filename, 'r')
    f.readline()
    for line in f:
        line = line.rstrip().split('\t')
        tid=line[0]
        name=line[2]
        otherNames=line[4]
        names=[line[2]]

        if tid!=taxid:
            continue
        
        if otherNames!= '-':
            otherNames=otherNames.split('|')

            names=[name]+otherNames

            for synonym in names:
                if synonym not in synonyms:
                    synonyms[synonym] = names
    f.close()
    return synonyms


def readMirnas(filename):
    mirnas=set()
    f=open(filename,'r')
    for line in f:
        mirna=line.strip()
        mirnas.add(mirna)
    f.close()

    return mirnas


ontologyFile=sys.argv[1]
interactionsFile=sys.argv[2]
mirnaFile=sys.argv[3]
synonymsFile=sys.argv[4]
outFile=sys.argv[5]
taxid=''
if len(sys.argv)>=6:
    taxid=sys.argv[6]

ontology,ontologyNames,ontologyGenes=readOntology(ontologyFile)
interactions=readInteractions(interactionsFile)
mirnas=readMirnas(mirnaFile)
if taxid!='':
    synonyms=readSynonyms(synonymsFile,taxid)
interactions=matchSysnonyms(synonyms,ontology,ontologyGenes,interactions)

g=open(outFile,'w')
for category in ontology:
    g.write('>' + category + '\n')
    for mirna in mirnas:
        genes=interactions[mirna] & ontology[category]
        g.write(mirna + '\t' + ','.join(genes) + '\n')

g.close()

