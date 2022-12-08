""" This script converts genbank format to fasta format
    utilizing regular expressions.

Use: (in shell)
    >python gbk_to_fasta_converter_regex.py gbk_filename.gbk
"""

from typing import Literal

__author__: Literal['Eliakim M. Kambale'] = "Eliakim M. Kambale"
__contact__: Literal['emkthegeek@gmail.com'] = "emkthegeek@gmail.com"
__license__: Literal['CC-BY-SA-NC'] = "CC-BY-SA-NC"
__date__: Literal["08-12-2022"] = "08-12-2022"
__version__: Literal['1.0.0'] = "1.0.0"

import sys
import os
import re

# Nitrogen bases dictionary (handy for complement sequence generation)
NITROBASES: dict[str, str] = {'a': 't', 'g': 'c', 't': 'a', 'c': 'g'}


def reads_gbk(file_name: str) -> list[str]:
    """Reads a genbank file

    Args:
        file_name (str): a genbank file name

    Returns:
        list[str]: the list of all lines in the file
    """
    with open(file_name, "r") as filein:
        lines: list[str] = filein.readlines()
        gbk_lines: list[str]= [line for line in lines]
    return gbk_lines

def extract_organism(gbk_lines: list) -> str:
    """Extract the organism which the sequence belong to.

    Args:
        file_name (str): a genbank file name

    Returns:
        str: the name of the organism
    """
    organism ="Not found"
    for line in gbk_lines:
        if re.search('ORGANISM', line[2:12]):
            organism: str = line[11:37].strip()
    return organism

def searches_genes(gbk_lines: list) -> list[str]:
    """Identifies genes in a genbank file.

    Args:
        file_name (str): a genbank file name

    Returns:
        list[str]: a list containing the start and end codons as well as
        the location (either direct or complement)
    """
    # Initializing the genes list
    genes: list[list] = []
    # Optional gene counting typewise
    direct: int = 0
    complement: int = 0
    for line in gbk_lines:
        # first condition to treat complement genes seperately
        if "gene" in line[5:11].strip() and "complement" not in line[21:33]:
            # utilizing regex to spot the start and end codons
            match: re.Match = re.search("\(?\<?([0-9]+)\.\.\>?([0-9]+)\)?",
                                        line)
            try:
                start: int = int(match.group(1))
                end: int = int(match.group(2))
            except (TypeError, ValueError):
                sys.exit("failed to convert the match to integer")
            # each sublist contains the start and end codon for each gene
            gene: list = [start, end, "direct"]
            genes.append(gene)
            direct += 1
        # second condition to treat direct genes seperately
        elif "gene" in line[5:11].strip() and "complement" in line[21:33]:
            # utilizing regex to spot the start and end codons
            match: re.Match = re.search("\(?\<?([0-9]+)\.\.\>?([0-9]+)\)?",
                                        line)
            try:
                start = int(match.group(1))
                end = int(match.group(2))
            except (TypeError, ValueError):
                sys.exit("failed to convert the match to integer")
            # each sublist contains the start and end codon for each gene
            gene = [start, end, "complement"]
            genes.append(gene)
            complement += 1
    return genes
            
def extract_sequence_regex(gbk_lines: list) -> str:
    """Extracts the complete sequence from a genbank file.

    Args:
        file_name (str): the genbank file name

    Returns:
        str: the sequence
    """
    # building the pattern
    regex: re.Pattern[str] = re.compile("([0-9]{1,6})\s([a-z\s?]{1,66})")
    sequence: str = ""
    for line in gbk_lines:
        # testing if the pattern is in line
        if regex.search(line):
            match: re.Match[str] = regex.search(line)
            # picking only the seconf group (letters : the sequence)
            line_seq: str = match.group(2)
            # using .split() method to get rid of whitespace in sequence
            sequence += "".join(line_seq.split())
    return sequence

def reverse_complement(sequence: str) -> str:
    """Generates the reverse compement of the sequence provided in argument.

    Args:
        sequence (str): the sequence to find the reverse for.

    Returns:
        str: teh reverse compement sequence.
    """
    complement: list[str] = []
    for base in sequence.lower():
        complement += [NITROBASES[base]]
    complement.reverse()
    reverse_comp: str = "".join(complement)
    return reverse_comp

def writes_fasta(fasta_file_name: str, comment: str,
                sequence: str) -> None:
    """Generates fasta files.

    Args:
        fasta_file_name (str): the name of the fasta file
        that is going to be generated.
        comment (str): the top line of the fasta file.
        sequence (str): the sequence in the fasta file.    
    """
    # Splitting the sequence in small sequences of 80 bases :)
    width: int = 80
    seq_split: list[str] = [sequence[i: i+width] for i in range(0, 
                            len(sequence), width)]
    with open(fasta_file_name, 'w') as fileout:
        fileout.write(f">{comment}\n")
        for slice in seq_split:
             fileout.write(f"{slice}\n")

def extract_genes_regex(gbk_file_name: str) -> None:
    """This function combines the above function to convert
    a genbank file into a fasta file.

    Args:
        gbk_file_name (str): a genbank file.
    """
    # preparing the complete sequence and the genes list
    gbk_lines: list[str] = reads_gbk(gbk_file_name)
    complete_sequence: str = extract_sequence_regex(gbk_lines)
    genes: list[str] = searches_genes(gbk_lines)
    organism: str = extract_organism(gbk_lines)
    # making the fasta file one by one
    for gene_count, gene in enumerate(genes):
        start: int = gene[0]
        end: int = gene[1] + 1 # the (end+1)th base is excluded (rule for slices !!!)
        location: str = gene[2]
        if location == "complement":
            # generating the reverse sequence
            gene_sequence_direct: str = complete_sequence[start:end]
            gene_sequence: str = reverse_complement(gene_sequence_direct)
            # making the fasta file name and top line comment
            gene_filename: str = f"gene_{gene_count+1:03d}.fasta"
            gene_comment: str = f"{organism}|{gene_count+1:05d}|\
{start}|{end}|{location}"
            # writing the fasta file
            writes_fasta(gene_filename, gene_comment, gene_sequence)
        elif location == "direct":
            # slicing the direct sequence from the complete sequence
            gene_sequence: str = complete_sequence[start:end]
            # making the fasta file name and top line comment
            gene_filename: str = f"gene_{gene_count+1:03d}.fasta"
            gene_comment: str = f"{organism}|{gene_count+1:05d}|\
{start}|{end}|{location}"
            # Writing the fasta file
            writes_fasta(gene_filename, gene_comment, gene_sequence)
        # printing the process' progress
        print(gene_count+1, gene_filename)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        convertible: str = sys.argv[1]
    else:
        sys.exit("Two args required !")
    if os.path.exists("gbk_to_fasta_converter.py") and \
        os.path.exists(convertible):
           extract_genes_regex(convertible)
    else:
        sys.exit("No such file or directory !")



