#-*- coding: utf-8 -*-
"""
lsdir: list files and folders in specified dirs and generate text in fixed markdown format
"""
import sys, os

item_templ = "- [{name}]({path})"

def get_name(name):
    return os.path.splitext(name)[0]

def main(root):
    items = []
    for path, dir_list, file_list in os.walk(root):
        # list subdirs
        for name in dir_list:
            items.append((name, os.path.join(path, name)))
        # list files
        for name in file_list:
            items.append((get_name(name), os.path.join(path, name)))
    
    # sort by name
    items.sort(key=lambda item: item[0])

    # print
    for item in items:
        print(item_templ.format(name=item[0], path=item[1]))

def usage():
    print("""
    Usage: python {} <dir>
    """.format(sys.argv[0]))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        exit()

    main(sys.argv[1])