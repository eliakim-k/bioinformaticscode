""" This script converts genbank format to fasta format.
Use: (in shell)
    >python gbk_to_fasta_converter.py genbank_filename.gbk
"""

from typing import Literal

__author__: Literal['Eliakim M. Kambale'] = "Eliakim M. Kambale"
__contact__: Literal['emkthegeek@gmail.com'] = "emkthegeek@gmail.com"
__license__: Literal['CC-BY-SA-NC'] = "CC-BY-SA-NC"
__date__: Literal["08-12-2022"] = "08-12-2022"
__version__: Literal['1.0.0'] = "1.0.0"

import sys
import os


BA: dict[str, str] = {'a': 't', 'g': 'c', 't': 'a', 'c': 'g'}

def reads_gbk(gbk_file_name: str) -> list[str]:
    """Reads a genbank file

    Args:
        file_name (str): a genbank file name

    Returns:
        list[str]: the list of all lines in the file
    """
    with open(gbk_file_name, "r") as filein:
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
        if line.strip().startswith('ORGANISM'):
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

    genes: list[list] = []
    sens: int = 0
    antisens: int = 0
    for line in gbk_lines:
        if line[5:11].strip().startswith("gene") and "complement" not in line:
            gene: str = line[20:].strip().replace("<", "").replace(">", "")
            gene: list[str] = gene.strip().split("..")
            gene.append("direct")
            genes.append(gene)
            sens += 1
        elif line[5:11].strip().startswith("gene") and "complement" in line:
            gene: str = line[31:].replace("(<", "").replace(">", "").replace(")", "").replace("(", "")
            gene: list[str] = gene.strip().split("..")
            gene.append("complement")
            genes.append(gene)
            antisens += 1
    return genes
            
def extract_sequence(gbk_lines: list) -> str:
    """Extracts the complete sequence from a genbank file.

    Args:
        file_name (str): the genbank file name

    Returns:
        str: the sequence
    """
    is_sequence = False
    sequence: str = ""
    for line in gbk_lines:
        if line.strip().startswith("ORIGIN"):
            is_sequence: bool = True
        if line.strip().startswith("//"):
            is_sequence: bool = False
        if is_sequence is True:
            sequence += "".join(line[9:].split())
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
        complement += [BA[base]]
    complement.reverse()
    reverse_comp: str = "".join(complement)
    return reverse_comp

def writes_fasta(fasta_file_name: str, comment: str,
                sequence: str) -> None:
    """Generates fasta files.

    Args:
        fasta_file_name (str): the name of the fasta file that will be generated.
        comment (str): the top line of the fasta file.
        sequence (str): the sequence in the fasta file.    
    """
    width: int = 80
    seq_split: list[str] = [sequence[i: i+width] for i in range(0, 
                                                    len(sequence), width)]
    with open(fasta_file_name, 'w') as fileout:
        fileout.write(f">{comment}\n")
        for slice in seq_split:
             fileout.write(f"{slice}\n")

def extract_genes(gbk_file_name: str) -> None:
    """This functions combines the above function to convert
    a genbank file into a fasta file.

    Args:
        gbk_file_name (str): a genbank file name.
    """
    gbk_lines: list[str] = reads_gbk(gbk_file_name)
    complete_sequence: str = extract_sequence(gbk_lines)
    genes: list[str] = searches_genes(gbk_lines)
    organism: str = extract_organism(gbk_lines)
    for gene_count, gene in enumerate(genes):
        start: int = int(gene[0])
        end: int = int(gene[1]) + 1
        location: str = gene[2]
        if location == "complement":
            gene_sequence_direct: str = complete_sequence[start:end]
            gene_sequence: str = reverse_complement(gene_sequence_direct)
            gene_filename: str = f"gene_{gene_count+1:03d}.fasta"
            gene_comment: str = f"{organism}|{gene_count+1:05d}|\
{start}|{end}|{location}"
            writes_fasta(gene_filename, gene_comment, gene_sequence)
        elif location == "direct":
            gene_sequence: str = complete_sequence[start:end]
            gene_filename: str = f"gene_{gene_count+1:03d}.fasta"
            gene_comment: str = f"{organism}|{gene_count+1:05d}|\
{start}|{end}|{location}"
            writes_fasta(gene_filename, gene_comment, gene_sequence)
        print(gene_count+1, gene_filename)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        convertible: str = sys.argv[1]
    else:
        sys.exit("Two args required !")
    if os.path.exists("gbk_to_fasta_converter.py") and \
        os.path.exists(convertible):
            extract_genes("sacc_cerevisiae.gbk")
    else:
        sys.exit("No such file or directory !")



