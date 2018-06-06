import fileinput
import sys
import os
import re

def getGeneFiles(gene_folder):
        gene_paths = dict()
        for name in os.listdir(gene_folder):
            result = re.match("genes_.*_.*.txt", name) 
            if result != None:
                listname = name.split("_")[1]
                gene_paths[listname] = gene_folder + name
        return gene_paths

gene_folder = "resources/genes/"

gene_paths = getGeneFiles(gene_folder)

gene_dict = dict()
for key,value in gene_paths.iteritems():
    cur_genes = []
    with open(value,'r') as gene_file:
        for line in gene_file:
            cur_genes.append(line.strip())
    gene_dict[key] = cur_genes

for line in fileinput.input(sys.argv[1]):
    if line.startswith('#'):
        print line.strip()+'\tGeneFilter'
    else:
        cur_gene = line.split('\t')[10]
        gene_filter = []
        for key,value in gene_dict.iteritems():
            if cur_gene in value:
                gene_filter.append(key)
        if len(gene_filter) == 0:
            gene_filter.append('.')
        print line.strip()+'\t'+';'.join(gene_filter)

