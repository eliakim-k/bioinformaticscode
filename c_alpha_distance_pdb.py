"""
Calculation of distances between consecutive alpha carbons of a protein structure
"""
import sys
import os

# Selection of alpha carbons in a PDB file

def finds_pdb_calpha(pdbfile):
    with open(pdbfile, "r") as file_in, open("calpha_file.dat", "w") as file_out:
        pdb_lines = file_in.readlines()
        for pdb_line in pdb_lines:
            if pdb_line.startswith("ATOM"):
                if pdb_line[13:17].strip() == "CA":
                    file_out.write("{}".format(pdb_line))
    with open("calpha_file.dat", "r") as calpha_file:
        ca_lines = calpha_file.readlines()
        ca_list = []
        for ca_line in ca_lines:
            ca_list.append(ca_line)
    return ca_list

#Computation of the Euclidean distance between consecutive alpha carbons

def eucl_dist_capha(pdbfile):
    import math
    calpha_list = finds_pdb_calpha(pdbfile) #use of the previous selection function
    list_coords = []
    for i in range(len(calpha_list)):
        record = calpha_list[i].split()
        num_ca = int(record[1])
        x = float(record[6])
        y = float(record[7])
        z = float(record[8])
        list_coords += [(num_ca, x, y, z)]
    list_dist_eucl = []
    for j in range(len(list_coords)-1):
        num_1 = list_coords[j][0]
        num_2 = list_coords[j+1][0]
        a = list_coords[j][1] - list_coords[j+1][1]
        b = list_coords[j][2] - list_coords[j+1][2]
        c = list_coords[j][3] - list_coords[j+1][3]
        dist_eucl = math.sqrt(a**2+b**2+c**2)
        list_dist_eucl += [[num_1, num_2, dist_eucl]]
    mean = 0
    for i in range(len(list_dist_eucl)):
        mean += list_dist_eucl[i][2] / len(list_dist_eucl)
    with open("distance_calpha.dat","w") as distancefile_written:
        distancefile_written.write("CA_prev CA_flwing Distance\n")
        for m in range(len(list_dist_eucl)):
            distancefile_written.write("{:<6d}{:<6d}{:>6.2f}\n".format(list_dist_eucl[m][0],list_dist_eucl[m][1],list_dist_eucl[m][2]))
        distancefile_written.write("    Mean {:>6.2f}\n".format(mean))
    with open("distance_calpha.dat","r") as distancefile_read:
        dist_lines = distancefile_read.readlines()
        for dist_line in dist_lines:
            print(dist_line)
    return list_dist_eucl   #Optional (Useful if you want to perform other actions on the generated data)

if len(sys.argv) != 2:
    sys.exit("Two arguments required !")
else:
    pdbfilename = sys.argv[1]
if os.path.exists("c_alpha_distance_pdb.py") and os.path.exists(pdbfilename):
    eucl_dist_capha(pdbfilename)
else:
    print("'{}' or '{}' not avalaible on the disk".format("c_alpha_distance_pdb.py",pdbfilename))


