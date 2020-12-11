"""
@project : Poirot
@author  : harumonia
@mail   : zxjlm233@163.com
@ide    : PyCharm
@time   : 2020-12-08 16:19:08
@description: None
"""
import fontforge

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--file_path', type=str, dest='filepath',
                    help='file path')
parser.add_argument('--file_name', type=str, dest='filename',
                    help='file name')
args = parser.parse_args()

F = fontforge.open(args.filepath)
for name in F:
    if name == '.notdef':
        continue
    file_suffix = args.filepath.replace('./font_collection/', '')
    filename = "./fontforge_output/{}/".format(args.filename) + name + ".png"
    # print name
    F[name].export(filename)
    # F[name].export(filename, 600)     # set height to 600 pixels
