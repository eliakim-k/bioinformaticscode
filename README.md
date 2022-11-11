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

#3 read_genbankfiles.py

This file reads genbank files and renders the sequence of nucleotides.
-> The syntax is the same as above :
    > python read_genbankfiles.py name_genbank_file.gbk