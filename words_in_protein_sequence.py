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

def search_words_in_sequence(word_file: str, 
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

def counts_words_in_sequence(word_file: str, 
                            protein_seq_file: str) -> dict[str, int]:
    """Counts words in sequence.

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
                dico[word] += len(regex.findall(sequence))
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
        dico_search: dict[str, int] = search_words_in_sequence(words_file,
                                                        sequence_file)
        dico_count: dict[str, int] = counts_words_in_sequence(words_file,
                                                        sequence_file)
        for key in dico_search:
            if dico_search[key] == max(dico_search.values()):
                # Le mot qui se retrouve dans le plus des sequences
                print(key, "found in", dico_search[key], "sequence")
                # Le mot le plus fréquent dans le protéome
                print(key, "found in", f"{100*dico_search[key]/sum(dico_search.values()):.2f}",
                    "pourcent of the sequence")
        for clef in dico_count:
            if dico_count[clef] == max(dico_count.values()):
                # Le mot qui se retrouve dans le plus des sequences
                print(clef, "found", dico_count[clef], "times")
    else:
        sys.exit("No such file in directory !")