#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
from collections import deque


def findFile1(path, file):
    '''To implent the simple functions like linux command -- find.'''
    # Depth First Search
    with os.scandir(path) as entryDir:
        for entry in entryDir:
            if entry.name == file:
                return entry.path
            if entry.is_dir(follow_symlinks=True):
                res = findFile1(path=entry.path, file=file)
                if res:
                    return res


def findFile2(path, file):
    '''To implent the simple functions like linux command -- find.'''
    # Breadth  First Search
    dirs = deque()
    with os.scandir(path) as entryDir:
        for entry in entryDir:
            if entry.is_file(follow_symlinks=True) and entry.name == file:
                return entry.path
            if entry.is_dir(follow_symlinks=True):
                if entry.name == file:
                    return entry.path
                dirs.append(entry.path)
    while True:
        try:
            dir_ = dirs.popleft()
            res = findFile2(dir_, file)
            if res:
                return res
        except IndexError:
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser('To implent the simple functions like linux command -- find.')
    parser.add_argument('-p', '--path', type=str, help='the root directory to find file.')
    parser.add_argument('-f', '--file', type=str, help='the file or dir to find.')
    args = vars(parser.parse_args())
    # path = args['path']
    # file = args['file']

    path = 'D:\sublime_coding'
    file = 'notes.py'
    res = findFile2(path, file)
    print(res)
