import sys
import os

def convert_3_lettr_1_lettr(sequence):
    seq_3_lettr = sequence.upper()
    seq_1_lettr = []
    for acide in seq_3_lettr.split():
        if acide == "ALA":
            seq_1_lettr += ["A"]
        elif acide == "ARG":
            seq_1_lettr += ["R"]
        elif acide == "ASN":
            seq_1_lettr += ["N"]
        elif acide == "ASP":
            seq_1_lettr += ["D"]
        elif acide == "CYS":
            seq_1_lettr += ["C"]
        elif acide == "GLU":
            seq_1_lettr += ["E"]
        elif acide == "GLN":
            seq_1_lettr += ["Q"]
        elif acide == "GLY":
            seq_1_lettr += ["G"]
        elif acide == "HIS":
            seq_1_lettr += ["H"]
        elif acide == "ILE":
            seq_1_lettr += ["I"]
        elif acide == "LEU":
            seq_1_lettr += ["L"]
        elif acide == "LYS":
            seq_1_lettr += ["K"]
        elif acide == "MET":
            seq_1_lettr += ["M"]
        elif acide == "PHE":
            seq_1_lettr += ["F"]
        elif acide == "PRO":
            seq_1_lettr += ["P"]
        elif acide == "SER":
            seq_1_lettr += ["S"]
        elif acide == "THR":
            seq_1_lettr += ["T"]
        elif acide == "TRP":
            seq_1_lettr += ["W"]
        elif acide == "TYR":
            seq_1_lettr += ["Y"]
        elif acide == "VAL":
            seq_1_lettr += ["V"]
    seq_1_lettr_str = " ".join(seq_1_lettr)
    return seq_1_lettr_str

if len(sys.argv) == 2:
    if os.path.exists("convert_protein_3_letters_to_1_letter.py"):
        nom_fichier = sys.argv[1]
        if os.path.exists(nom_fichier):
            with open(nom_fichier, "r") as protein_in:
                protein_seq = protein_in.readlines()
                sequence_to_convert_0 = []
                for line in protein_seq:
                    if ">" not in line:
                        sequence_to_convert_0 += [line]
                sequence_to_convert_1 = " ".join(sequence_to_convert_0)
            sequence_converted = convert_3_lettr_1_lettr(sequence_to_convert_1)
            print("Sequence to convert :\n", " ".join(protein_seq),"\n", "Converted sequence :\n", sequence_converted)
        else:
            sys.exit("The file you want to convert is not avalaible on the disk !")
else:
    sys.exit("Two arguments required ! Please, use the syntax 'python convert_protein_3_letters_to_1_letter.py file_to_convert_name.fasta'")