import argparse
import os
import shutil
from typing import List

"""
1. 普通导入: import_once('numpy') 
2. 别名导入: import_once('numpy', 'np')
3. 多级导入: import_once('numpy.random.randint')
4. from ... import ...:import_once('numpy', names=['sin', 'cos'])
"""



def create_directory(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return path

def clear_directory(path):
    files = os.listdir(path)
    for file in files:
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)

def str2bool(v):

    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def tail_directory_func(path: str, func: callable, *args):
    """
    Recursively traverse all subdirectories of path and execute func
    when a file is encountered.

    Args:
        path (str): The path of the directory to traverse
        func (callable): The function to execute when a file is found
        *args: Optional arguments passed to func when called
    """
    if not os.path.exists(path) or not os.path.isdir(path):
        return False

    dir_contents = os.listdir(path)
    is_tail = True
    for name in dir_contents:
        subDir = os.path.join(path, name)
        if os.path.isdir(subDir):
            tail_directory_func(subDir, func, *args)
            is_tail = False
    if is_tail:
        func(subDir,*args)
