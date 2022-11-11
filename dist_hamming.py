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

"""case 2:"""
def dist_hamming(A, B):
    dist = 0        #My variable "dist" is outside the if-clause
    if len(A) == len(B):        
        for i in range(len(A)):
            if A[i] != B[i]:
                dist += 1
    else:
        print("Please ensure the lenghts of the two sequence entered are identical !")
    distance = dist  #Again, my variable is outside the if-clause
    return distance

seq_1 = "AGWPSGGASAGLAIL"
seq_2 = "IGWPSAGASAGLWIL"
seq_3 = "ATTCATACGTTACGATT"
seq_4 = "ATACTTACGTAACCATT."

hamm_1_2 = dist_hamming(seq_1, seq_2)
hamm_3_4 = dist_hamming(seq_3, seq_4)
print(
"La distance de hamming entre les séquences 1 et 2 est {}\n \
    La distance de hamming entre les séquences 3 et 4 est {}".format(hamm_1_2, hamm_3_4)
)