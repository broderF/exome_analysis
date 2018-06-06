import os

exomiser_path = '/Users/broder/projects/IBD-DACH_FT_3/exomiser/analysis'
annovar_path = '/Users/broder/projects/IBD-DACH_FT_3/variants.merged.normalized.vcf.gz.annovar.hg19_multianno.txt'
output_path = '/Users/broder/projects/IBD-DACH_FT_3/result.tsv'

os.system("python resources/merge_results_exomiser.py "+exomiser_path +" > /tmp/result1")
os.system("python resources/add_gene_filter.py /tmp/result1 > /tmp/result2")
os.system("python resources/add_anno_annotation_to_exomiser_output.py /tmp/result2 "+annovar_path +" /tmp/result3")
os.system("python resources/add_analysis_columns.py /tmp/result3 > "+output_path)