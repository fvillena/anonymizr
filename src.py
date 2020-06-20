import pandas as pd
import numpy as np
import hashlib
import functools
import pathlib
import warnings
import os

def hasher(x,salt,result):
    if pd.isnull(x):
        return np.nan
    else:
        x = str(x) + str(salt)
        encoded_string = x.encode()
        hashed_string = hashlib.md5(encoded_string)
        hashed_hex = hashed_string.hexdigest()
    if result == "int":
        hashed_int = int(hashed_hex[:3], 16)
        return hashed_int
    if result == "md5":
        return hashed_hex


def anonymize(df,identifier_column_name,hash_column_names,blank_column_names,date_column_names,salt):
    df = df.copy()
    df[hash_column_names] = df[hash_column_names].applymap(lambda x: hasher(x,salt,"md5"))
    df[blank_column_names] = np.nan
    for date_column_name in date_column_names:
        df[date_column_name] = pd.to_datetime(df[date_column_name],errors="coerce")
        df[date_column_name] = df.apply(lambda x: x[date_column_name] + pd.DateOffset(days=hasher(x[identifier_column_name],salt,"int")),axis=1)
    return df

def load_dataset(dataset_location):
    path = pathlib.Path(dataset_location)
    if path.suffix == ".xlsx":
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            df = pd.read_excel(path,dtype=object)
    elif path.suffix == ".csv":
        df = pd.read_csv(path,dtype=object)
    else:
        raise NotImplementedError
    return df

def save_dataset(dataset_location,df):
    path = pathlib.Path(dataset_location)
    new_name = "anonym_" + path.name
    new_path = os.path.join(path.parent,new_name)
    if path.suffix == ".xlsx":
        df.to_excel(new_path,index=False)
    elif path.suffix == ".csv":
        df.to_csv(new_path,index=False)
    else:
        raise NotImplementedError