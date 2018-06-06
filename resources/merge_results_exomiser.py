import os
import itertools
import fileinput
import sys

#get all absolute paths in a given folder
def getAllSubFiles(input_folder):
    exomiser_config_paths = []
    for name in os.listdir(input_folder):
            exomiser_config_paths.append('/'.join([input_folder,name]))
    return exomiser_config_paths

def getAllExomiserResultVariantPaths(paths):
    result_paths = []
    for path in paths:
        name = os.path.basename(path)
        if name.startswith('result') and name.endswith('variants.tsv'):
            result_paths.append(path)
    return result_paths

def sortExomiserFiles(files):
    for result in results:
        os.system('sort '+result+' -o'+result)
        
def mergeInheritance(results):
    files = [open(f,'r') for f in results]
    first = True
    for lines in itertools.izip(*files):
        inheritances = []
        contributed = []
        contributed_var = []
        combined_score = []
        gene_var_score = []
        pheno_score = []
        variant_score = []
        counter = 0
        basic_line = ""
        for line in lines:
            if first:
                print line.strip()
                break
            else:
                basic_line = line.strip()
                cur_inheritance = line.split('\t')[5]
                file_name = os.path.basename(files[counter].name)
                moi = file_name[-15:][0:2]
                if cur_inheritance == 'PASS':
                    inheritances.append(moi+'_'+ cur_inheritance)
                    contributed_var.append(basic_line.split('\t')[32])
                    combined_score.append(basic_line.split('\t')[31])
                    gene_var_score.append(basic_line.split('\t')[30])
                    pheno_score.append(basic_line.split('\t')[29])
                    variant_score.append(basic_line.split('\t')[28])
            counter += 1
        if first:
            first = False
        else:
            basic_line = basic_line.split('\t')
            if len(inheritances) == 0: inheritances.append('inheritance')
            basic_line[5] = ';'.join(inheritances)
            basic_line[32] = 'CONTRIBUTING_VARIANT' if 'CONTRIBUTING_VARIANT' in contributed_var else  '.'
            basic_line[31] = max(combined_score)
            basic_line[30] = max(gene_var_score) 
            basic_line[29] = max(pheno_score)
            basic_line[28] = max(variant_score)
                        
            print '\t'.join(basic_line)

    for f in files:
        f.close()

analysis_folder = sys.argv[1]
paths = getAllSubFiles(analysis_folder)
results = getAllExomiserResultVariantPaths(paths)

#sort files
sortExomiserFiles(results)

#merge inheritance
mergeInheritance(results)


