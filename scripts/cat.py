#!/usr/bin/env python

import os
import sys
from lib import *

index = 0

def cat_pair(fullpath, name, pid):
    global index
    files = filter(lambda i: not i.endswith(".txt"), os.listdir(fullpath))
    if not files:
        c = {}
        c["id"] = index
        index += 1
        c["pid"] = pid
        c["name"] = name
        c["is_leaf_node"] = True
        return [c]
    data = []
    c = {}
    c["id"] = index
    index += 1
    c["pid"] = pid
    c["name"] = name
    c["is_leaf_node"] = False
    data.append(c)

    for i in files:
        data += cat_pair(os.path.join(fullpath, i), i, c["id"])
    return data

    
def main(dirpath):
    global index
    files = os.listdir(dirpath)
    data = []
    for i in files:
        fullpath = os.path.join(dirpath, i)
        data += cat_pair(fullpath, i, index)
    return data


if __name__ == "__main__":
    session = create_session()
    for i in main(sys.argv[1]):
        c = Category()
        c.id = i['id']
        c.pid = i['pid']
        c.name = i['name']
        c.is_leaf_node = i['is_leaf_node']
        session.add(c)
    session.commit()
    session.close()
    
        
