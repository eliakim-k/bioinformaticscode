# bioinformaticscode
scripts for bioinformatics

#1 lecturefichierfasta.py
- You need to have this file in the same directory as your fasta file
- Open the shell and pass in the following arguments
    > python lecturefichierfasta.py fasta_file_name.fasta
- You will get the following information about the fasta file
    * name of the fasta file
    * length of the sequence
    * a message telling you whether or not this number is a multiple of 3 (as for 3 nitrogen bases)
    * the number of codons
    * the ten first bases
    * the ten last bases
Nota: You can find two fasta file in the repository to check this out

#2 convert_protein_3_letters_to_1_letter.py
- This file helps convert a 3-letter encoded protein sequence into a 1-letter encoded one
- You need position yourself in the folder containing the file convert_protein_3_letters_to_1_letter.py and the fasta file of the protein sequence you cant to convert
- Then you pass in a shell the following arguments to the python interpreter :
    > python convert_protein_3_letters_to_1_letter.py fasta_file_name.fasta
- You will be presented the sequence in 3-letter code and the converted one just below it
Nota: Your fasta file needs to be in 3-letter code, otherwise your converted sequence will appear empty.

#3 dist_hamming.py
This script calculates the hamming distance between two sequences. The Hamming distance measures the difference between two sequences of the same size by counting the number of positions which, for each sequence, do not correspond to the same amino acid.
-> Only genbank files are supported so far
-> Syntax :
    > python dist_hamming.py file_name_seq_1.gbk file_name_seq_2.gbk

#4 read_genbankfiles.py

This file reads genbank files and renders the sequence of nucleotides.
-> The syntax is the same as above :
    > python read_genbankfiles.py name_genbank_file.gbk

#5 c_alpha_distance_pdb.py

This file computes the distance between consecutive c_alpha carbons in a PDB file.
The calculation results are printed on screen with a head containg the column titles and a bottom line (containg the mean of distances).
-> The syntax is the same as above :
    > python c_alpha_distance_pdb.py pdb_file_name.pdb

#6 gbk_gene_counter.py

This script helps count the number of genes in a genbank file.
Syntax:
     > python gbk_gene_counter.py genbank_file_name.gbk
Note : The two files must be in the folder from with you are lauching python. Otherwise, an error will appear.

#7 pdb_protein_center_of_gravity.py

This script computes and displays a protein's center of graivity as an approximation of the barycenter of its C_alpha carbones.

Syntax:
    >python pdb_protein_center_of_gravity.py pdb_file_name.pdb
Note : The two files must be in the folder from with you are lauching python. Otherwise, an error will appear.

#8 quick_bio.py

This file is a collection of the above functions. Imported as a module, it gives access to the above functions.
In a main program:
    import quick_bio
    quick_bio.function_name(argument)
