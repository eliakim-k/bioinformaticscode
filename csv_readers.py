""" This script reads csv files and returns a dataframe printing it on screen. 
Use: (in shell)
    > python csv_readers.py csv_file_name.csv
    The user is asked to choose from three functions. Once done, the results are
    printed on screen.
"""

__author__ = ("Eliakim M. Kambale")
__contact__ = ("emkthegeek@gmail.com")
__copyright__ = "CC-BY-SA-NC"
__version__ = "1.0.0"
__date__ = "11-22-2022"


import copy
import csv
import numpy as np
import pandas as pd
import sys
import os


def csv_to_d_frame_through_csv_module(csv_filename):
    """This function reads a csv file and returns a pandas dataframe.
        It uses the python csv bult-in module and pandas series.

    Args:
        csv_filename (str): the name of the csv file

    Returns:
        pandas dataframe: a table like object containing data.
    
    Nota:
        The functions prints the results on screen as well.
        All what this function does can be done by 'pandas.read_csv()'
    """
    
    with open(csv_filename, "r", encoding="UTF-8") as file_in:
        f_reader = csv.DictReader(file_in)
        f_list = []
        i = -1
        for row in f_reader:
            i += 1
            series = pd.Series(row)
            # Converting a Series to a Dataframe
            frame = series.to_frame()
            # Adding a index to columns (because the method
            # .to_frame() defaults them to 0)
            frame.columns = [i]
            # Making a list of dataframes
            f_list.append(frame)
        # Concatenating the frames and avoiding repetition
        # of etiquettes (thus argument axis=1)
        d_frame = pd.concat(f_list, axis=1)
        # Printing the transpose of the dataframe
        print(d_frame.T)
    return d_frame.T


def csv_to_d_frame_through_pd_series(csv_filename):
    """ This function reads a csv file and returns a pandas dataframe.
        It uses pandas series.
    
    Parameter
    --------
    csv_filename : str
        The CSV filename
    Returns
    -------
    list
        a list of dictionnaries whose keys are the headings and values the data.
    Nota Bene:
              The functions also prints the dataframe corresponding to the csv file.
              All what this function does can be done by 'pandas.read_csv()'
    """
    
    with open(csv_filename, "r", encoding="UTF-8") as file_in:
        lines = file_in.readlines()
        # Selecting the headings
        heading_list = lines[0].strip().split(",")
        # Making a dictionary of headings
        head = []
        for i in range(len(heading_list)):
            head += [(i, heading_list[i])]
        head = dict(head)
        # Loading data in a list of dictionnaries
        data_list = []
        for line in lines[1:]:
            list_line = line.strip().split(",")
            dict_data = []
            for i in range(len(list_line)):
                dict_data.append((head[i], list_line[i]))
            dict_data = dict(dict_data)
            data_list.append(dict_data)
        f_list = []
        i = -1
        for dico in data_list:
            i += 1
            series = pd.Series(dico)
            # Converting a Series to a Dataframe
            frame = series.to_frame()
            # Adding a index to columns (because the method
            # .to_frame() defaults them to 0)
            frame.columns = [i]
            # Making a list of dataframes
            f_list.append(frame)
        # Concatenating the frames and avoiding repetition
        # of etiquettes (thus argument axis=1)
        d_frame = pd.concat(f_list, axis=1)
        # Printing the transpose of the dataframe
        print(d_frame.T)
    return d_frame.T


def csv_to_d_frame_through_np_arrays(csv_filename):
    """ This function reads a CSV file and returns a pandas dataframe.
        It uses numpy arrays.
    
    Parameter
    --------
    csv_filename : str
        The CSV filename
    Returns
    -------
    pandas dataframe.
    
    Nota Bene:
              The functions also prints the results. All what this function
              does can be done by pandas function 'pandas.read_csv()'
    """
    
    with open(csv_filename, "r", encoding="UTF-8") as file_in, \
        open("data_for_np.dat", "w", encoding="UTF-8") as file_out:
        lines = file_in.readlines()
        # Selecting the headings
        heading_list = lines[0].strip().split(",")
        # Making a dictionary of headings
        heads = []
        for i in range(len(heading_list)):
            heads.append((i, heading_list[i]))
        heads_copy = copy.deepcopy(heads)
        head_dict = dict(heads)
        file_out.write(f'{head_dict}')
        # Writing data in .dat file (making CSV a TSV)
        for line in lines[1:]:
            list_line = line.strip().split(",")
            line_str = "\t".join(list_line)
            file_out.write(f"{line_str}\n")
    # Loading the data from .dat file with numpy
    # I had to precise the dtype=str (defaults is float) 
    # and delimiter="\t" to get expected results
    data_array = np.loadtxt("data_for_np.dat", dtype=str, delimiter="\t")
    # Making a list of tuples (heading, vertical vector)
    # The transpose attribute of numpy array helps a lot
    data_list_tupl = []
    for i in range(len(heads_copy)):
        data_list_tupl.append((head_dict[i], data_array.T[i]))
    # Turning the list of tuples into a dictionary
    data_dict = dict(data_list_tupl)
    # Using pandas function to make a dataframe out of a dictionary
    d_frame = pd.DataFrame.from_dict(data_dict)
    # Printing the results
    print(d_frame)
    return d_frame


if __name__ == "__main__":
    choice = input("Choose the function :\n\
        1. csv_to_d_frame_through_csv_module()\n\
        2. csv_to_d_frame_through_pd_series()\n\
        3. csv_to_d_frame_through_np_arrays()\n\
        > ")
    if int(choice) == 1:
        if len(sys.argv) != 2:
            sys.exit("Two str args required !")
        if os.path.exists("csv_readers.py"):
            file = str(sys.argv[1])
            csv_to_d_frame_through_csv_module(file)
        else:
            sys.exit("Source file 'csv_readers.py' missing.")
    elif int(choice) == 2:
        if len(sys.argv) != 2:
            sys.exit("Two str args required !")
        if os.path.exists("csv_readers.py"):
            file = str(sys.argv[1])
            csv_to_d_frame_through_pd_series(file)
        else:
            sys.exit("Source file 'csv_readers.py' missing.")
    elif int(choice) == 3:
        if len(sys.argv) != 2:
            sys.exit("Two str args required !")
        if os.path.exists("csv_readers.py"):
            file = str(sys.argv[1])
            csv_to_d_frame_through_np_arrays(file)
        else:
            sys.exit("Source file 'csv_readers.py' missing.")


