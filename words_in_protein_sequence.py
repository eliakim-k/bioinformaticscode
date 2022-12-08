""" This script checks whether a word is in the protein sequence.

Use: (in shell)
    >python words_in_protein_sequence words_filename.txt sequence_filename.fasta
"""

from typing import Literal

__author__: Literal['Eliakim M. Kambale'] = "Eliakim M. Kambale"
__contact__: Literal['emkthegeek@gmail.com'] = "emkthegeek@gmail.com"
__license__: Literal['CC-BY-SA-NC'] = "CC-BY-SA-NC"
__version__: Literal['1.0.0'] = "1.0.0"


import re
import sys
import os


def reads_word(file_name: str) -> list[str]:
    """Generates a list from a file containing English words.

    Args:
        file_name (str): the file name of an extension .txt.

    Returns:
        list[str]: list of words.
    """
    
    with open(file_name, 'r') as filein:
        lines: list[str] = filein.readlines()
        upper_case_words: list[str] = [
            line.strip().upper() for line in lines[:]
            if len(line.strip()) >= 3]
    return upper_case_words

def reads_sequence(file_name: str) -> dict[str, str]:
    """Reads a fasta file with mutiple sequences

    Args:
        file_name (str): the name of the file in .fasta extension

    Returns:
        dict[str, str]: a dictionary whose keys are the accessions of the
        sequences and the values are the sequence themselves.
    """
    
    with open(file_name, 'r') as filein:
        lines: list[str] = filein.readlines()
        dico: dict[str, str] = {}
        for line in lines[:]:
            if line.startswith('>'):
                key: str = re.search("(\>[sp]?\|?)([0-9A-Za-z\w\W?]+)(\|)", line).group(2)
                dico[key] = ""
            else:
                dico[key] += line.strip()
    return dico

def search_words_in_proteome(word_file: str, 
                            protein_seq_file: str) -> dict[str, int]:
    """Searches words in sequence.

    Args:
        word_file (str): the file containg the words to search
        proteome_file (str): the file containing the sequence to search from.

    Returns:
        dict[str, int]: a dictionary whose keys are the words and the values
        are the number of sequence in which that word occured.
    """
    
    word_list: list[str] = reads_word(word_file)
    protein_seq_dict: dict[str, str] = reads_sequence(protein_seq_file)
    dico: dict[str, int] = {}
    for word in word_list:
        regex: re.Pattern[str] = re.compile(word)
        dico[word] = 0
        for sequence in protein_seq_dict.values():
            if regex.search(sequence):
                dico[word] += 1
    return dico


if __name__ == "__main__":
    if len(sys.argv) == 3 and os.path.exists("words_in_protein_sequence.py"):
        arg: str = " ".join(sys.argv[1:])
        try:
            words_file: str = re.search("[a-zA-Z0-9\_?]+\.txt", arg).group(0)
            sequence_file: str = re.search("[a-zA-Z0-9\_?]+\.fasta", arg).group(0)
        except:
            sys.exit('Wrong file extensions !')
    if os.path.exists(words_file) and os.path.exists(sequence_file):
        dico: dict[str, int] = search_words_in_proteome(words_file, sequence_file)
        for key in dico:
            if dico[key] ==1:
                print(key, "found in", dico[key], "sequence")
            else:
                print(key, "found in", dico[key], "sequences")
    else:
        sys.exit("No such file in directory !")