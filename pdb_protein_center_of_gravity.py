""" Protein center of graivity """
import os
import sys

""" This function finds the C_alpha and collects the residue number and the related CA coordinates
in a list of dictionnaries """

def finds_calpha(filename):
    with open(filename, "r") as pdbfile_in:
        c_alpha = [line for line in pdbfile_in.readlines() \
            if line.startswith("ATOM") and line[13:17].strip() == "CA"] #Liste de compréhension pour sélectionner les CA
        coords = []
        for line in c_alpha:
            dico_coords = {"resid":int(line[24:28].strip()),"x":float(line[30:38].strip()), \
                "y":float(line[40:47].strip()), "z":float(line[49:55].strip())}
            coords.append(dico_coords)
    return coords

""" 
The 'computer_barycenter' function computes the x,y,z coordinates of the center of gravity of a protein
approximated as the barycenter of its C_alpha.
This function returns a list of the barycenter's [x,y,z] coordinates.

"""

def compute_barycenter(coordinates):
    g_x, g_y, g_z = 0, 0, 0
    for dico in coordinates:
        g_x += (dico["x"])/len(coordinates)
        g_y += (dico["y"])/len(coordinates)
        g_z += (dico["z"])/len(coordinates)
    barycentre = [g_x, g_y, g_z]
    return barycentre

"""The 'displays_coord_bary' function helps display the results of calculation """
def displays_coord_bary(pdbfilename):
    centre_bastar = compute_barycenter(finds_calpha(pdbfilename))
    print()
    f =""
    for g in range(len(centre_bastar)):
        if g == 0:
            f = "x"
        elif g == 1:
            f = "y"
        else:
            f ="z"
        print(f"Barycenter's {f} coordinate : {centre_bastar[g]:>7.3f}")
    print()

if len(sys.argv) != 2:
    sys.exit("Two arguments required !")
else:
    file = sys.argv[1]
if os.path.exists("pdb_protein_center_of_gravity.py") and os.path.exists(file):
    displays_coord_bary(file)
else:
    sys.exit("At least one of the files is not avalaible on the disk !")