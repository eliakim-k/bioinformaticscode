import quick_bio

for i in quick_bio.gbk_gene_count_regex("sacc_cerevisiae.gbk"):
    print(i[0],"\t",i[1],"\t",i[2],"\t",i[3],"\t",i[4])