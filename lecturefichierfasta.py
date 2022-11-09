import sys
import os

#Fonction qui récupère le nom du fichier et le contenu
def lit_fasta(nom_fichier):
    with open(nom_fichier, "r") as lecture:
        lines_list = lecture.readlines()
    return lines_list, nom_fichier
""" La fonction lit_fasta renvoie un tuple contenant le nom du fichier
    et une liste de toutes les lignes du fichier fasta
    * Pour récupérer les éléments du tuple, j'utilise ma méthode tuple[i] avec i l'indice
    """
#Récuperer le nom du fichier à partir du terminal
if len(sys.argv) != 2:
	sys.exit('Error! Exactly two arguments required.')
else:
	nom_fichier_glo = sys.argv[1]
if os.path.exists('lecturefichierfasta.py'):
    tuple_rendu = lit_fasta(nom_fichier_glo)
    sequence = tuple_rendu[0]

    """" La méthode .split() me permet de couper la première chaîne de caractère (sequence[0])
         La liste qui en découle me permet de récupérer la tranche d'éléments en indices [1:3]
         La méthode "".join() permet de transformer la sous-liste obtenu par la méthode .split()
         en une chaine de caractère simple
    """
    nom_seq_list = sequence[0].split()[1:3]
    nom_seq_str = " ".join(nom_seq_list)

    longueur_seq = 0
    for line in sequence:
        if ">" not in line:             #Dans un fichier fasta, toute ligne qui commence par ">" est dediée
            longueur_seq += len(line)   #à la description de la séquence et ne peut pas être compté et lu comme faisant partie de ladite séquence    
    nombre_codon = round(longueur_seq / 3)

    print()
    print(nom_fichier_glo)
    print("Le nom de la séquence est : ", nom_seq_str)
    print("La séquence contient : {} bases".format(longueur_seq))
    if longueur_seq%3 == 0:
        print("Le nombre des bases est un mutiple de 3")
    else:
        print("Le nombre des bases n'est pas un mutiple de 3")
        print("La séquence possède environ {} codons".format(nombre_codon))
        print("Les dix premières bases sont : {}".format(sequence[1][0:10]))
        print("Les dix dernières bases sont : {}".format(sequence[-1][-11:-1])) #N'est pas parvenu à lire la dernière base
        print()
