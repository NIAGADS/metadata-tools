#!/usr/bin/env python3
"""
NIAGADS meta-data validator
"""
import argparse
import pandas as pd
import json

from sys import stderr, stdout, exit
from os import path
from datetime import datetime

ASSAY_TYPES = ["generic", "sequencing","rna_seq", "chipseq"]
SHEETS = ["contact", "study", "cohort", "phenotype", "sample_assay", "processing"]


def get_config(sheet):
    ''' load and return config file for specified sheet'''
    config = None
    with open(path.join(args.configDir, sheet + ".json"), 'r') as fh:
        config = fh.read()        
    return json.loads(config)


def load_metadata_from_xlsx():
    ''' loads metadata from EXCEL file and returns as list structure '''
    1

def validate_sheet(metadata, targetSheet, targetSheetConfig):
    ''' run sheet validator '''
    1

def validate_args():
    ''' validate command line arguments '''
    
    print("INFO:", "Validating arguments", file=stderr)
    
    messageJson = []
    notValid = False
    if args.excelFile and args.inputDir:
        message = "Options --excelFile and --inputDir provided. Will attempt to load specified EXCEL file, assuming value is full path. --inputDir will be ignored"
        messageJson.append({"WARNING": message})
        
    if not args.excelFile and not args.inputDir:
        message = "Must provide either the full path to the EXCEL file (--excelFile) or to the directory containing indivdual sheets in tab-delimited .txt or .tab files (--inputDir)"
        messageJson.append({"ERROR": message})
        notValid = True
        
    if not args.outputDir:
        message = "Output directory (--ouputDir) missing.  Outputting validation messages to STDOUT"
        messageJson.append({"WARNING": message})
        
    if args.sheetMap:
        raise NotImplementedError("Handling of sheet name mappings (--sheetMap) is not yet implemented")
        
    if notValid:
        print("ERROR - ", "Invalid arguments/values provided.")
        [ print(next(iter(message.values()))) for message in messageJson if 'ERROR' in next(iter(message.items())) ]
        print("Exiting")
        exit(1)
        
        
    else:
        print("WARNING - ")
        [ print(next(iter(message.values()))) for message in messageJson ]
        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='NIAGADS meta-data validator ', allow_abbrev=False)
    parser.add_argument('-c', '--configDir', required=True,
                        help="config file directory")
    parser.add_argument('--failOnFirstError', action="store_true",
                        help="flag indicating whether to fail on first error; if not specified will generate a JSON report with all errors")
    parser.add_argument('-a', '--assayType', default="generic", choices=ASSAY_TYPES,
                        help="type of assay")
    parser.add_argument('--warnOnNonAscii', action="store_true",
                        help="warn when non-ascii characters are detected and try to resolve;"  
                            + "when not specified, validator will report an ERROR and FAIL")
    parser.add_argument('-o', '--outputDir', 
                        help="directory to which validation output should be written;" 
                        + "if not provided output printed to STDOUT")   
    parser.add_argument('-e', '--excelFile',
                        help="full path to EXCEL file; use --inputDir to read in individual sheets in tab-delimited text format")
    parser.add_argument('-i', '--inputDir',
                        help="full path to directory containing input tab-delimited text files;" 
                            + "to read in an EXCEL file use the --excelFile option")        
    parser.add_argument('-s', '--sheet', 
                        help="for validating a single sheet, supply sheet name" 
                            + "in the EXCEL file, or file name if loading sheet from --inputDir") 
    parser.add_argument('--sheetMap', help="""mapping of actual sheet names to expected in JSON format; e.g., 
                        '{"study": "my_study_sheet_name", "sample_assay":"dataset2_assay"}'
                        sheets that can be mapped are "contact", "study", "cohort", "phenotype", "sample_assay", "processing"
                        "" and "" from the metadata template will be mapped automatically to "sample_assay" and "processing", respectively
                        """)

    args = parser.parse_args()
    
    if args.sheet:
        raise NotImplementedError("Validating single sheets has not yet been implmented; use --excelFile to validate an XLSX file contain all sheets in the metadata template")
    
    if args.inputDir:
        raise NotImplementedError("Validation from .tab or .txt tab-delimited files has not yet been implemented; use --excelFile to validate an XLSX file")
    
    validate_args()
    
    # read in EXCEL file and check for unicode/unprintable characters
    # validate sheets in order
    