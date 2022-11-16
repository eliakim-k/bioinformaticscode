"""
This function counts the number of genes in a gbk file and prints the results
in four column : Gene number Location Starting Base Ending Base and Number of bases in the gene
"""
import sys
import os

def gene_count_gbk(gbkfile):
    with open(gbkfile, "r") as gbkfile_in, open("gene_in_gbkfile.txt", "w") as txtfile_out:
        gbk_lines = gbkfile_in.readlines()
        g, gc = 0, 0
        txtfile_out.write("Gene  Location  Start   End   Bases\n")
        for gbk_line in gbk_lines:
            if gbk_line[5:13].strip().startswith("gene"): #Before the test, I needed to locate the position of the keyword "gene" in a gbkfile. Thus : gbk_line[5:13].strip()
                g += 1      #Counts the number of genes
                if "complement" in gbk_line:
                    gc += 1 #Counts the number of complement genes
                    borne_inf = "".join(gbk_line[32:].split("..")[0]).strip().strip("<")    #I used the two points .. as a mark to split the starting and ending base of a gene. Thus : gbk_line[32:].split("..")
                    borne_sup = "".join(gbk_line[32:].split("..")[1]).strip().strip(">").strip(")") #The starting base was then accessible thanks to list method gbk_line[32:].split("..")[0]
                    base_num = int(borne_sup)-int(borne_inf)+1                                           #The ending base accessible via gbk_line[32:].split("..")[1]
                    txtfile_out.write("Gene {} cmplmt\t{}\t{}\t{}\n".format(g, borne_inf,borne_sup,base_num))
                elif "complement" not in gbk_line:
                    borne_inf = "".join(gbk_line[21:].split("..")[0]).strip().strip("<")
                    borne_sup = "".join(gbk_line[21:].split("..")[1]).strip().strip(">").strip(")")
                    base_num = int(borne_sup)-int(borne_inf)+1
                    txtfile_out.write("Gene {} direct\t{}\t{}\t{}\n".format(g, borne_inf,borne_sup, base_num))
            """ The location of starting and ending base numbers varies a lot. But, starting column is well formated. So, i relied on it!
            for direct gene :
                    the location of the starting and ending base is from the 21 column. Thus : gbk_line[21:]
            for complement gene :
                    the location of the starting and ending base is from the 32 column(after the word 'complement'). Thus : gbk_line[32:]
            """
        txtfile_out.write("Total number of genes : {}\n".format(g))
        txtfile_out.write("Direct genes          : {}\n".format(g-gc))
        txtfile_out.write("Complement genes      : {}\n".format(gc))
    with open("gene_in_gbkfile.txt", "r") as txtfile_in:
        gene_lines = txtfile_in.readlines()
        for gene_line in gene_lines:
            print(gene_line.strip())

if len(sys.argv) != 2:
    sys.exit("Two arguments required !")
else:
    gbk_file_name = sys.argv[1]
    if os.path.exists("gbk_gene_counter.py") and os.path.exists(gbk_file_name):
        gene_count_gbk(gbk_file_name)
    else:
        print("At least one file not avalaible on the disk !")

