#!/usr/bin/env python

"""
extract each ISATab sheet and save to a text file
"""

import argparse
import csv
import datetime
from os import getcwd, path
from openpyxl import Workbook as wb, load_workbook

def warning(*objs, **kwargs):
    '''
    print messages to stderr
    '''
    fh = sys.stderr
    flush = False
    if kwargs:
        if 'file' in kwargs: fh = kwargs['file']
        if 'flush' in kwargs: flush = kwargs['flush']

    print('[' + str(datetime.datetime.now()) + ']\t', *objs, file=fh)
    if flush:
        fh.flush()


def get_worksheet_names(workbook, print2stderr=False):
    '''
    returns worksheets in a workbook as a list; 
    optional: prints to stderr
    '''
    wsNames = workbook.get_sheet_names()
    if print2stderr:
        warning(str(len(wsNames)), "worksheets found:")
        for name in wsNames:
            warning(name)
    return wsNames


def convert_worksheet_to_csv(worksheet, sep='\t', outputDirectory=None, debug=False):
    '''
    converts specified sheet to csv writes to file with
    same name
    '''
    suffix = '.csv' if sep == ',' else '.txt'
    fileName = worksheet.title.replace(' ', '_') + suffix
    if outputDirectory is None:
        outputDirectory = getcwd()
    fileName = path.join(outputDirectory, fileName)
    lineNum = 0
    with open(fileName, 'w') as f:
        writer = csv.writer(f, delimiter=sep)
        for row in worksheet.rows:
            if debug:
                lineNum = lineNum + 1
                warning(lineNum, ":", [cell.value for cell in row])
            writer.writerow([cell.value for cell in row])


def extract_sheets():
    if args.verbose: warning("Parsing", args.file)
    workbook = load_workbook(args.file, data_only=True)
    worksheets = get_worksheet_names(workbook, print2stderr=args.verbose)
    if args.verbose: warning(str(len(worksheets)), "worksheets found.")
    for w in worksheets:
        if args.verbose: warning("Parsing sheet:", w)
        ws = workbook.get_sheet_by_name(name=w)
        convert_worksheet_to_csv(ws, sep=args.delimiter,
                                    outputDirectory=args.outputDir,
                                    debug=args.debug)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help="full path to file", required=True)
    parser.add_argument('-o', '--outputDir', help="output directory; if missing assume current directory", default=os.getcwd(), required=False)
    parser.add_argument('-d', '--delimiter', help="delimiter", default="\t", required=False)
    parser.add_argument('-v', '--verbose', help="will print line numbers as parsing", required=False, action='store_true')
    parser.add_argument('--debug', help="will print the lines from the excel file as they are parsed to help determine why a failure may have occurred",
        required=False, action='store_true')

    args = parser.parse_args()

    extract_sheets()