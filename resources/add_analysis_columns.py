import fileinput
import sys

counter = 1
for line in fileinput.input(sys.argv[1]):
    basic_line = line.strip().split('\t')
    if basic_line[0].startswith('#'):
        basic_line.insert(0,"keep")
        basic_line.insert(1,"note")
        basic_line.insert(2,"mark")
        basic_line.insert(8,"Clinvar")
    else:
        basic_line.insert(0,"")
        basic_line.insert(1,"")
        basic_line.insert(2,"")
        basic_line.insert(8,".")
        basic_line[15] = "=FN"+str(counter)
    counter += 1
    print '\t'.join(basic_line)
