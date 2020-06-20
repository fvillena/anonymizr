#!/usr/bin/env python3

import os
import sys
script_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, script_directory)
import src
import argparse
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

directory = os.getcwd()

logger.debug(script_directory)
logger.debug(directory)

parser = argparse.ArgumentParser(description='Dataset anonymizer', usage='%(prog)s [options]')
parser.add_argument("dataset", help="Location of the dataset.", type=str)
args = parser.parse_args()

dataset_location = os.path.join(directory, args.dataset)

logger.debug(dataset_location)

df = src.load_dataset(dataset_location)

columns = list(df.columns)

for i,column in enumerate(df.columns):
    print(f"{i}: {column}")

identifier_column_index = int(input("identifier column number: "))
identifier_column_name = columns[identifier_column_index]

logger.debug(identifier_column_name)

hash_column_indices = input("hash column number: ").replace(" ","").split(",")
hash_column_names = [columns[int(i)] for i in hash_column_indices]

logger.debug(hash_column_names)

blank_column_indices = input("blank column number: ").replace(" ","").split(",")
blank_column_names = [columns[int(i)] for i in blank_column_indices]

logger.debug(blank_column_names)

date_column_indices = input("date column number: ").replace(" ","").split(",")
date_column_names = [columns[int(i)] for i in date_column_indices]

logger.debug(date_column_names)

salt = input("salt: ")

new_df = src.anonymize(df, identifier_column_name, hash_column_names, blank_column_names, date_column_names, salt)

src.save_dataset(dataset_location,new_df)