import os
import sys

"""
This function reads a genbank file and renders its sequence.
This is how it works:
-> when Python encounters a line that starts with (in line) "ORIGIN", it sets the boolean variable 'flag' to 'True'
-> even if the next line does not contain the word 'ORIGIN', 'flag' remains 'True' because 
we did not instruct Python to change this value otherwise (via the else-clause that's willingly absent)
-> In fact, 'flag' can only turn 'False' if a line starts with '//'. An this is where our sequence stops !

:) It's a f*cking hack to the logical variables
"""

def lit_genbank(filename):
    with open(filename, "r") as gbk_in:
        lines = gbk_in.readlines()
        flag = False
        sequence = ""
        for line in lines:
            if "ORIGIN" in line:    #Technique pour demander à Python de lire tout ce qui vient après ligne contenant "ORIGIN"
                flag = True
            if flag == True:
                sequence += line[11:76]
            if "//" in line:
                flag = False
    return sequence

#Récuperer le nom du fichier à partir du terminal
if len(sys.argv) != 2:
	sys.exit('Error! Exactly two arguments required.')
else:
	nom_fichier_glo = sys.argv[1]
if os.path.exists('read_genbankfiles.py'):
    seq = lit_genbank(nom_fichier_glo)
    print(seq)
