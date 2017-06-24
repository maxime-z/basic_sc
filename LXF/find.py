#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def find(pwd,filename):
    res = []
    pwd_abs = os.path.abspath(pwd)
    for x in os.listdir(pwd):
        full_path_x = os.path.join(pwd,x)
        if os.path.isdir(full_path_x):
            res.append(removeCommonPath(os.path.abspath(x)+'/',pwd_abs))
            res += find(full_path_x,filename)
        else:
            if filename in x:
                res.append(removeCommonPath(os.path.abspath(x),pwd_abs))
    return res

def removeCommonPath(a,b):
    common = os.path.commonpath([a,b])
    if a.startswith(common):
        return a[len(common):]

res = find('./LXF','test')

for x in res:
    print(x)