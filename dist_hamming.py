import sys
import os

"""When using a if-clause in a function and a variable to iterate upon 
    --> either all the block of script will fall under the if-clause including the initialization var = 0 and its final value (case 1 below)
    --> or the initialization and the final value will be outside the if-clause (case 2 below)
    --> but in no case will one of them be in the if-clause unless an error appears, namely this one : "UnboundLocalError: local variable 'variable' referenced before assignment)"
case 1:"""
def dist_hamming(A, B):
    if len(A) == len(B):        
        dist = 0         #My variable "dist" is inside the if-clause
        for i in range(len(A)):
            if A[i] != B[i]:
                dist += 1
        distance = dist   #Again my variable is inside the if-clause
        return distance 
    else:
        print("Please ensure the lenghts of the two sequence entered are identical !")

""" case 2:
def dist_hamming(A, B):
    dist = 0        #My variable "dist" is outside the if-clause
    if len(A) == len(B):        
        for i in range(len(A)):
            if A[i] != B[i]:
                dist += 1
    else:
        print("Please ensure the lenghts of the two sequence entered are identical !")
    distance = dist  #Again, my variable is outside the if-clause
    return distance"""

def lit_genbank(filename):
    with open(filename, "r") as gbk_in:
        lines = gbk_in.readlines()
        flag = True
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
if len(sys.argv) != 3:
	sys.exit('Error! Exactly three arguments required.')
else:
	file_1, file_2 = sys.argv[1], sys.argv[2]
if os.path.exists('read_genbankfiles.py'):
    seq_1 = lit_genbank(file_1)
    seq_2 = lit_genbank(file_2)
    hamm_1_2 = dist_hamming(seq_1, seq_2)
    print("La distance de hamming entre les séquences 1 et 2 est {}".format(hamm_1_2))
else:
    sys.exit("At least one of the files is not avalaible on the disk !")