"""
A module for editing trdens.in files.

We want to be able to edit the nki, nkf values.

To run this file with command line arguments::

    python edit_dot_in.py -o original/path/trdens.in -n new/path/trdens.in -i 1 -f 2
"""

import argparse

# no need to edit these if you're running the file from the command line
original_filename = "../_trdens_input_files/trdens.in_1"
new_filename = "../_trdens_input_files/trdens.in_1_2"
nki = 1
nkf = 2

# which line of the file are your nki and nkf values on?
# these should be constant but edit if needed
nki_line_index = 1
nkf_line_index = 3


def read_file(filename):
    """
    Get the lines (as a list of strings) of the file
    at the path given by filename (string).
    """
    with open(filename, "r+") as open_file:
        lines = open_file.readlines()
    return lines


def get_nki_nkf(lines):
    """
    Given the lines (list of strings) of a trdens.in file,
    get nki and nkf (integers).

    The first 4 lines should look like this::

        F
        1   2               ! ki,nki
        1  5  6  10
        1   1               ! kf,nkf

    So just get the second word of the 2nd and 4th lines.
    """
    nki_line_words = lines[nki_line_index].split()
    nki = int(nki_line_words[1])
    nkf_line_words = lines[nkf_line_index].split()
    nkf = int(nkf_line_words[1])
    return nki, nkf


def set_nki_nkf(lines, new_nki, new_nkf):
    """
    Given the lines (list of strings) of a trdens.in file, set nki and nkf
    to the values of new_nki and new_nkf (integers).
    """
    nki_line_words = lines[nki_line_index].split()
    nki_line_words[1] = str(new_nki)
    lines[nki_line_index] = "  ".join(nki_line_words) + "\n"
    nkf_line_words = lines[nkf_line_index].split()
    nkf_line_words[1] = str(new_nkf)
    lines[nkf_line_index] = "  ".join(nkf_line_words) + "\n"
    return lines


def write_file(lines, output_filename):
    """
    Write the file given by lines (list of strings)
    to the path output_filename (string).
    """
    with open(output_filename, "w+") as open_file:
        open_file.writelines(lines)


def edit_trdens_in_file(filename, new_filename, new_nki, new_nkf):
    lines = read_file(filename)
    new_lines = set_nki_nkf(lines, new_nki, new_nkf)
    write_file(new_lines, new_filename)


if __name__ == "__main__":
    # add argument parser so we can call this with
    # python output_plotter.py -f "filename"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-o', '--original_file', help='Original Filename',
        required=False, default=[])
    parser.add_argument(
        '-n', '--new_file', help='New Filename',
        required=False, default=[])
    parser.add_argument(
        '-i', '--nki', help='Value of nki',
        required=False, default=[])
    parser.add_argument(
        '-f', '--nkf', help='Value of nkf',
        required=False, default=[])

    args = parser.parse_args()
    if args.original_file != []:
        # I assume that means all args were provided
        edit_trdens_in_file(
            args.original_file, args.new_file, args.nki, args.nkf)
    else:
        edit_trdens_in_file(original_filename, new_filename, nki, nkf)
