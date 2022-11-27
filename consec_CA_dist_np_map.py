""" New easy way to compute consecutive atoms euclidian distance.
Use: (in shell)
    > python consec_CA_dist_np_map.py pdf_filename.pdb

"""

__author__ = "Eliakim M. Kambale"
__contact__ = "emkthegeek@gmail.com"
__license__ = "CC-BY-SA-NC"
__version__ = "1.0.0"


import pandas as pd
import numpy as np
import math
import re
import os
import sys


def ca_getter(pdbfile):
    """This function extracts the CA coordinates from pdf file.

    Args:
        pdbfile (str): pdf_filename.pdb

    Returns:
        numpy array: an array of size (n, 3) with n the number of aminoacids
        in the protein.
    """
    with open(pdbfile, "r", encoding="utf-8") as filein:
        lines = filein.readlines()
        c_alpha_coords = [re.findall("\-?[0-9]+\.[0-9]{3}", line) \
            for line in lines if line.startswith("ATOM") and \
                line[12:16].strip() == "CA"]
        coords = np.array(c_alpha_coords, dtype=float)
    return coords

def eucl_dist(point_P, point_Q):
    """This function computes the euclidian distance between two atoms.

    Args:
        point_P (tuple): first atom's x y z coordinates
        point_Q (tuple): second atom's x y z coordinates

    Returns:
        float: euclidian distance
    """
    x_1, y_1, z_1 = point_P
    x_2, y_2, z_2 = point_Q
    x, y, z = (x_1-x_2)**2, (y_1-y_2)**2, (z_1-z_2)**2
    dist = math.sqrt(x+y+z)
    return dist

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Two args required !")
    if os.path.exists("consec_CA_dist_np_map.py"):
        in_put = sys.argv[1]
        if re.search("[0-9a-zA-Z]+\.pdb", in_put):
            file = str(re.search("[0-9a-zA-Z]+\.pdb", in_put).group())
        else:
            sys.exit("Wrong PDB file name")
        # Extracting data from pdb to an array of size (89,3)
        coords = ca_getter(file)
        # The map() function iterates on two arrays (line by line)
        # Each line contains the three coordinates of a CA atom
        # The two arrays are one deprived on the first CA and the other of the last CA
        # so that the distance concerns to consecutive CA
        dist_CA_consec = map(eucl_dist, coords[:-1], coords[1:])
        # Formating and casting the results 
        distances_CA_consec = [float(f"{i:.3f}") for i in list(dist_CA_consec)]
        # Making a series of results
        CA_nums = [(i+1, i+2) for i in range(int(coords.size/3-1))]
        distances_series = pd.Series(index= CA_nums, data=distances_CA_consec)
        # Printing the results
        print(distances_series)
    else:
        sys.exit("No such file or directory !")