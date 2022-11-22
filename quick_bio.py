""" This module contains funtions for bio informatics.

Use:
    import the module in your main program and use help()
    to find out more about the functions.
"""

__author__ = ("Eliakim M. Kambale")
__contact__ = ("eliakim.kambale@unikin.ac.cd")
__copyright__ = "CC-BY-SA-NC"
__date__ = "2022/11/18"
__version__ = "1.0.0"

import collections
from math import sqrt
import math
import re


def pdb_finds_calpha(filename):
    """ This function searches CA in a pdb file.

    Parameter
    ----------
    filename : string
        a pdb filename
    Returns
    -------
    list
        a list of dictionnaries of the following kind :
        {'resid': int, 'x': float, 'y': float, 'z': float} where
        resid is the residue number and x y z the cartesian coordinates
        of the corresponding alpha carbon.
    """

    with open(filename, "r") as pdbfile_in:
        c_alpha = [line for line in pdbfile_in.readlines() \
            if line.startswith("ATOM") and line[13:17].strip() == "CA"] # List comprehension for CA selecting
        coords = []
        for line in c_alpha:
            dico_coords = {"resid":int(line[23:28].strip()),"x":float(line[30:39].strip()), \
                "y":float(line[40:47].strip()), "z":float(line[48:56].strip())}
            coords.append(dico_coords)
    return coords


def pdb_compute_barycenter(coordinates):
    """ This function computes a protein barycenter's coordinates.

    Parameter
    ---------
    coordinates : list 
        list of coordinate dictionnaries (from 'finds_calpha' function)
    Returns
    -------
    list
        list containing the barycenter's coordinates [x,y,z]
    Nota Bene : The protein center of gravity is approximated
                as the barycenter of its alpha carbons.
    """
    g_x, g_y, g_z = 0, 0, 0
    for dico in coordinates:
        g_x += (dico["x"])/len(coordinates)
        g_y += (dico["y"])/len(coordinates)
        g_z += (dico["z"])/len(coordinates)
    barycentre = [g_x, g_y, g_z]
    return barycentre


def pdb_displays_bary_coords(pdbfilename):
    """ This function prints a protein's center of gravity coordinates.

    Paremeter
    --------
    pdbfilename : string
        a pdb filename
    Returns
    ------
    None
        prints the a protein's center of gravity coordinates.
    """
    centre_bastar = pdb_compute_barycenter(pdb_finds_calpha(pdbfilename))
    f =""
    for g in range(len(centre_bastar)):
        if g == 0:
            f = "x"
        elif g == 1:
            f = "y"
        else:
            f ="z"
        print(f"Barycenter's {f} coordinate : {centre_bastar[g]:.2f}\n")


def fasta_seq_compo(fastafile):
    """ This function determines a sequence's composition.

    Parameter
    ---------
    fastafile : string
        a fasta file name
    Returns
    -------
    dictionnary
        dictionnary of this kind : {'constituent1': count1, ...}
    """

    with open(fastafile, "r") as fastafilein:
        sequence_list = [line for line in fastafilein.readlines() if ">" not in line]
        sequence_char = "".join(sequence_list)
        sequence = "".join(sequence_char.split("\n"))
    object_counter = collections.Counter(sequence)
    dico_compo = dict(object_counter)
    return dico_compo


def gbk_gene_count(gbkfile):
    """ This function ferrets out all genes in a genbank file.

    Parameter
    ---------
    gbkfile : string
        a genbank filename
    Returns
    -------
    tuple
        a two-element tuple :
            * tuple[0] : list of dictionaries of this kind 
                {'gene': number, 'location': direct or complement,
                'startbase': number, 'endbase': number, 'totalbases': number}
            * tuple[1] : dictionary of this kind 
                {'totalgenes': number, 'directgenes': number, 
                'complementgenes': number}
        Nota Bene :
            The function also produces a 'gene_in_gbkfile.txt' file.
            It is avalaible in the working directory for necessary use.
    """

    with open(gbkfile, "r") as gbkfile_in, \
        open("gene_in_gbkfile.txt", "w") as txtfile_out:
        gbk_lines = gbkfile_in.readlines()
        g, gc = 0, 0
        for gbk_line in gbk_lines:
            if gbk_line[5:13].strip().startswith("gene"): #Before the test, I needed to locate the position of the keyword "gene" in a gbkfile. Thus : gbk_line[5:13].strip()
                g += 1      #Counts the number of genes
                if "complement" in gbk_line:
                    gc += 1 #Counts the number of complement genes
                    borne_inf = "".join(
                        gbk_line[32:].split("..")[0]).strip().strip("<")    #I used the two points .. as a mark to split the starting and ending base of a gene. Thus : gbk_line[32:].split("..")
                    borne_sup = "".join(
                        gbk_line[32:].split("..")[1]).strip().strip(">").strip(")") #The starting base was then accessible thanks to list method gbk_line[32:].split("..")[0]
                    base_num = int(borne_sup)-int(borne_inf)+1                                           #The ending base accessible via gbk_line[32:].split("..")[1]
                    txtfile_out.write("Gene  {:>4} \t\
                         cmplmt\t{:>7s}\t{:>7s}\t{:>7d}\n".format(g,
                          borne_inf,borne_sup,base_num))
                elif "complement" not in gbk_line:
                    borne_inf = "".join(
                        gbk_line[21:].split("..")[0]).strip().strip("<")
                    borne_sup = "".join(
                        gbk_line[21:].split("..")[1]).strip().strip(">").strip(")")
                    base_num = int(borne_sup)-int(borne_inf)+1
                    txtfile_out.write("Gene  {:>4} \t\
                         direct\t{:>7s}\t{:>7s}\t{:>7d}\n".format(g,
                          borne_inf,borne_sup, base_num))
            # The location of starting and ending base numbers varies a lot.
            # But, starting column is well formated. So, i relied on it!
            # For direct gene :
            #   the location of the starting and ending base is from the 21 column.
            #   Thus : gbk_line[21:]
            # For complement gene :
            #   the location of the starting and ending base is from the 32 column
            #   (after the word 'complement'). Thus : gbk_line[32:]

    with open("gene_in_gbkfile.txt", "r") as txtfile_in:
        gene_lines = txtfile_in.readlines()
        gene_list_dict = []
        for gene_line in gene_lines:
            dico = {"gene":gene_line[7:12].strip(),
            "location":gene_line[13:21].strip(), \
               "startbase":gene_line[21:29].strip(), 
               "endbase":gene_line[29:37].strip(), 
               "totalbases": gene_line[38:44].strip() }
            gene_list_dict.append(dico)
    dico_totals = {"totalgenes": g, "directgenes": g-gc, 
    "complementgenes": gc}
    return gene_list_dict, dico_totals


def dist_eucl(A, B):
    """ This function computes the eucidian distance.

    Parameters
    ----------
    A, B : lists
        lists of cartesian coordinates of two points A and B in space
    Returns
    -------
    float
        The returned float is the calculated euclidian distance.
    """

    xAB = float(A[0]) - float(B[0])
    yAB = float(A[1]) - float(B[1])
    zAB = float(A[2]) - float(B[2])
    d = sqrt(xAB**2 + yAB**2 + zAB**2)
    return d


def pdb_eucl_dist(atnum1, atnum2, pdbfilename):
    """ This function computes an euclidian distance between two atoms.

    Parameters
    ----------
    atnum1, atnum2 : int
        the atom numbers for which we want to calculate the euclidian distance
    pdbfilename : string
        the pdbfilename containing the two atoms
    Returns
    -------
    float
        The euclidian distance and prints the result on screen.
    """

    # Reading the pdb file to find the coordinates
    # related to the atom numbers specified
    j = 0
    with open(pdbfilename, "r") as pdbfilein:
        lines = pdbfilein.readlines()
        for line in lines:
            if line.startswith("ATOM"):
                j += 1
                if atnum1 <= j and int(line[7:12]) == atnum1:
                    x = float(line[31:39])
                    y = float(line[40:47])
                    z = float(line[48:56])
                    P = (x, y, z) #P est un 3-tuple mais il peut aussi être une liste
                    atomtp1 = line[13:17].strip()
                    res1 = line[17:23].strip()
                if atnum2 <= j and int(line[7:12]) == atnum2:
                    a = float(line[31:39])
                    b = float(line[40:47])
                    c = float(line[48:56])
                    Q = (a, b, c) #Q est un 3-tuple mais il peut aussi être une liste
                    atomtp2 = line[13:17].strip()
                    res2 = line[17:23].strip()
    try:
        #Calcul de la distance entre ces atomes
        distancePQ = dist_eucl(P, Q)
        #Affichage du résultat de calcul
        print("The distance between atom {} ({}/{}) and atom {} ({}/{}) is : \
             {:5.3f} Angstroms. \n".format(atnum1, atomtp1, res1, 
             atnum2, atomtp2, res2, distancePQ))
    except:
        print("At least one number provided is not"
         "a atom number in the molecule.")
    return distancePQ


def reads_fasta(filename):
    """ This function reads a fasta file.

    Parameter
    ---------
    filename : string
        a fasta filename
    Returns
    -------
    string
        a sequence without whitespaces
    """
    
    with open(filename, "r") as fasta_file_in:
        sequence =""
        flag = False
        for line in fasta_file_in.readlines():
            if line.startswith(">"):
                flag = False
            else:
                flag = True
            if flag is True:
                sequence += line
    sequence_list = sequence.split('\n')
    sequence_char = "".join(sequence_list)
    return sequence_char


def pdb_eucl_dist_consec_capha(pdbfile):
    """ This function computes the euclidian distance
        between consecutive alpha carbons from a pdb file.
    
    Parameter
    ---------
    pdbfile : string
        pdb filename
    Returns
    -------
    list
        a list of three-element tuples of this kind :
        (atom number j, atom number j+1, euclidian distance)
    Nota Bene:
              The function automatically prints the results as well.
    """

    # Extraction of C alpha coordinates from pdf file
    calpha_list = pdb_finds_calpha(pdbfile)
    list_coords = []
    for i in range(len(calpha_list)):
        record = calpha_list[i]
        num_ca = int(record["resid"])
        x = float(record["x"])
        y = float(record["y"])
        z = float(record["z"])
        list_coords += [(num_ca, x, y, z)]
    # Consecutive alpha carbons are identified by j and j+1 index
    # Calculation of the euclidian distance between consecutive alpha carbons
    list_dist_eucl = []
    for j in range(len(list_coords)-1):
        num_1 = list_coords[j][0]
        num_2 = list_coords[j+1][0]
        a = list_coords[j][1] - list_coords[j+1][1]
        b = list_coords[j][2] - list_coords[j+1][2]
        c = list_coords[j][3] - list_coords[j+1][3]
        dist_eucl = math.sqrt(a**2+b**2+c**2)
        list_dist_eucl += [(num_1, num_2, dist_eucl)]
    # Computing the mean alpha carbons distance
    mean = 0
    for i in range(len(list_dist_eucl)):
        mean += list_dist_eucl[i][2] / len(list_dist_eucl)
    # Writing the results in a .dat file
    with open("distance_calpha.dat","w") as distancefile_written:
        distancefile_written.write("CA_prev CA_flwing Distance\n")
        for m in range(len(list_dist_eucl)):
            distancefile_written.write("{:<6d}\t  {:<6d} {:>6.2f}\n".format(
                list_dist_eucl[m][0],list_dist_eucl[m][1],
                list_dist_eucl[m][2]))
        distancefile_written.write("\tMean\t\t {:>6.2f}\n".format(mean))
    # Reading the data for display and return
    with open("distance_calpha.dat","r") as distancefile_read:
        dist_lines = distancefile_read.readlines()
        for dist_line in dist_lines:
            print(dist_line.strip())
    return list_dist_eucl


def pdb_finds_c_alpha_regex(pdbfilename):
    """ This function uses regular expressions to find CA coordinates.
    
    Parameter
    ---------
    pdbfilename : string
        a pdb filename
    returns
    -------
    list
        a list of four-element dictionaries of this kind
        {"resid": int, "x": float, "y": float, "z": float} in which
        'resid' represents the residue number and 'x' 'y' 'z' the cartesian
        coordinates of the corresponding alpha carbon.
    Nota Bene:
              The function generates a 'ca_coordinates_pdb_file.dat'
              file for any necessary use.

        """
    # Defining the regular expression
    regex = re.compile(".[0-9]+\.[0-9]+")
    # Reading and selecting the CA in a pdb file
    with open(pdbfilename, "r") as file_in:
        # Building the list of CA lines from the pdb file
        c_alpha_list = [
            line for line in file_in.readlines() 
            if line[13:17].strip() == "CA"]
        # Identifying and extracting the regex (here the x y z coordinates)
        coords_list = []
        for line in c_alpha_list:
            coords = regex.findall(line)    # Finding the regex in a CA line
            dico_coords = {"resid": int(line[23:28].strip()),
             "x": float(coords[0]), "y": float(coords[1]), 
             "z": float(coords[2])}         # Extracting it from the list : coords[index]
            coords_list.append(dico_coords) # Adding dicos to a list
    # Writing the coordinates in a '.dat' file
    with open("ca_coordinates_pdb_file.dat", "w") as file_out:
        for record in coords_list:
            (resid, x, y, z) = (record["resid"], record["x"], 
            record["y"], record["z"])
            file_out.write(f"{resid}\t\t{x:>7.3f}\t\t{y:>7.3f}\t\t{z:>7.3f}\n")
    return coords_list


def gbk_gene_count_regex(genbank_file):
    """ This function uses regular expressions to count genes
        in a genbank file.

    Parameter
    ---------
    genbank_file : string
        a genbank filename
    Returns
    -------
    list
        a list of five-element tuples of this kind
        (gene count -> int, startbase count -> int,
            endbase count -> int, gene location -> str, base count -> int)
    Nota Bene:
              The function generates a 'gene_count_file.txt' file containg
              these four columns for any necessary disposition.
    """
    # Creating regex
    regex_gene = re.compile("gene")
    # The group 'complement\(' is putative (thus the use of '?')
    # Notice '\' before '(' character to escape creating another group
    regex_base = re.compile("(complement\()?<?([0-9]+)\.\.>?([0-9]+)")
    # Reading a .gbk file and writing a .txt file
    with open(genbank_file,"r") as gbk_file_in, \
        open("gene_count_file.txt", "w") as file_out:
        gene_list = []
        i = 0
        for line in gbk_file_in.readlines():
            # The target line is the one containg both of these patterns
            if regex_gene.search(line) and regex_base.search(line):
                i += 1
                result = regex_base.search(line)
                groupe_1 = result.group(1)
                startbase = int(result.group(2))
                endbase = int(result.group(3))
                if groupe_1 == "complement(":
                    location = "complement"
                    gene_list.append((i, startbase, endbase, location, endbase-startbase+1))
                    file_out.write(
                        f"{i:<4d}\t{startbase:>7d} \t {endbase:>7d} \t {location:<7s}\t{endbase-startbase+1:>7d}\n")
                else:
                    location = "direct"
                    gene_list.append((i, startbase, endbase, location, endbase-startbase+1))
                    file_out.write(
                        f"{i:<4d}\t{startbase:>7d} \t {endbase:>7d} \t {location:<7s}\t{endbase-startbase+1:>7d}\n")  
    return gene_list


