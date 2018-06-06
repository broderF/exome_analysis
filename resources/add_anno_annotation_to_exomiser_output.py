import sys

def getExomiserVariant(line):
    line = line.split('\t')
    return '_'.join(line[0:2])

def getAnnovarVariant(line):
    line = line.split('\t')

    alt = line[4]
    idents = []
    for cur_alt in alt.split(','):
        chrompos = line[0:2]
        pos = line[1]
        ref = line[3]
        #chrompos.append(ref)
        #chrompos.append(cur_alt)
        ident = '_'.join(chrompos)
        idents.append(ident)
#    if pos == '100550766':
    return idents

exomiser_path = sys.argv[1]
annovar_path = sys.argv[2]
output_path = sys.argv[3]


output_file = open(output_path,'w')

header = ''
ex_variants = dict()
with open(exomiser_path,'r') as exomiser_file:
        for line in exomiser_file:
                if line.startswith('#'):
                        header += line.strip()
                else:
                        ident = getExomiserVariant(line)
                        ex_variants[ident] = line.strip()

print '{}{}'.format('exomiser variants found: ',len(ex_variants))
nr_found = 0
annovar_idents = []
with open(annovar_path, 'r') as annovar_file:
        first = True
        for line in annovar_file:
                if first:
                        header += '\t'+line.strip()
                        first = False
                        print header
                        output_file.write(header+'\n')
                else:
                        idents = getAnnovarVariant(line)
                        for ident in idents:
                            annovar_idents.append(ident)
                            if ident in ex_variants:
                                exome_line = ex_variants[ident]
                                output_file.write(exome_line+'\t'+line.strip()+'\n')
                                nr_found += 1
                                ex_variants.pop(ident)

print '{}{}'.format('exomiser variants in annovar file found: ',nr_found)

missing_variants = list(set(ex_variants.keys()) - set(annovar_idents))
for element in missing_variants:
    exome_line = ex_variants[element]
    output_file.write(exome_line+'\n')
print missing_variants
