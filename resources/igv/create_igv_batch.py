import locale

def print_to_batch(batch_file,track,chrom,pos_raw):
    batch_file.write('new\n')
    batch_file.write('genome hg19\n')
    batch_file.write('snapshotDirectory '+screen_folder+'\n')
    batch_file.write('load  '+bam_folder+track+'.bam\n')
    pos = locale.format("%d", int(pos_raw), grouping=True)
    batch_file.write('goto chr'+chrom+':'+pos+'\n')
    filename = chrom+"_"+pos_raw+"_"+track+".png"
    batch_file.write('snapshot '+filename+'\n')
    batch_file.write('\n')

def load_individuals(batch_file, path_to_individuals):
    batch_file.write('new\n')
    batch_file.write('genome hg19\n')
    batch_file.write('snapshotDirectory '+screen_folder+'\n')
    for element in path_to_individuals:
        batch_file.write('load  '+element+'\n')
        
def load_locations(batch_file,vcf_file_path):
    with open(vcf_file_path,'r') as vcf_file:
        for line in vcf_file:
            if line.startswith('#'):
                continue
            else:
                line = line.split('\t')
                pos = locale.format("%d", int(line[1]), grouping=True)
                chrom = line[0]
                batch_file.write('goto chr'+chrom+':'+pos+'\n')
                filename = chrom+"_"+str(pos)+".png"
                batch_file.write('snapshot '+filename+'\n')
                batch_file.write('\n')

locale.setlocale(locale.LC_ALL, 'en_US')
bam_files = []
screen_folder = ''
vcf_file = ''

batch_file = open('igv_batch_file.TXT','w')
load_individuals(batch_file,bam_files)
load_locations(batch_file,vcf_file)

batch_file.write('exit')
batch_file.close()


   
