import zipfile
import os
import sys
import shutil
import json
import glob
from pathlib import Path

if Path(sys.argv[1]).exists():
    print('file input')
    file_name = sys.argv[1]
else:
    print('file is not found')
    sys.exit()

with open('./config.json') as config_json:
    config = json.load(config_json)

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname=arcname)

    return

def str_to_bool(str):
    if str.lower()=="false":
        return False
    else:
        return True

unanonymize = {}

config['numberDiffs'] = int(config['numberDiffs'])
config['taiko'] = str_to_bool(config['taiko'])

HOME = os.getcwd()
maps = os.path.join(HOME, file_name)
unzipped_maps = os.path.join(HOME, 'unzipped_maps')
extracted_oszs = os.path.join(HOME, 'extracted_oszs')
to_osz = os.path.join(HOME, 'to_osz')
outdir = os.path.join(HOME, 'output')

if os.path.exists(outdir):
    shutil.rmtree(outdir)
if os.path.exists(unzipped_maps):
    shutil.rmtree(unzipped_maps)
if os.path.exists(extracted_oszs):
    shutil.rmtree(extracted_oszs)
if os.path.exists(to_osz):
    shutil.rmtree(to_osz)
if os.path.exists('./anonmaps.zip'):
    os.remove('./anonmaps.zip')

os.mkdir(unzipped_maps)
os.mkdir(extracted_oszs)
os.mkdir(to_osz)

with zipfile.ZipFile(maps, "r") as zip_ref:
    zip_ref.extractall(extracted_oszs)

osz_folders = os.listdir(extracted_oszs)
title_list = []
duplicated_title_list = []
print('Anonymizing .osz files')
if len(os.listdir(os.path.join(extracted_oszs))) == 0:
    pass

all_files = [x for x in os.listdir(os.path.join(extracted_oszs))]
osu_list = [x for x in os.listdir(os.path.join(extracted_oszs)) if x.endswith('.osu')]
title = ''
artist = ''
creator = ''
version = ''
for file in osu_list:
    to_write = []
    with open(os.path.join(extracted_oszs, file), encoding='utf8') as f:
        lines = [line.rstrip() for line in f]
    # set title and artist
    for line in lines:
        if line.startswith('Title:'):
            title = line[6:].strip()
        elif line.startswith('Artist:'):
            artist = line[7:].strip()
        elif line.startswith('Creator'):
            creator = line[8:].strip()
        elif line.startswith('Version'):
            version = line[8:].strip()
    # for upwrite
    for line in lines:
        repl = False
        if line.startswith('DistanceSpacing: '):
            repl = 'DistanceSpacing: 1.4'
        elif line.startswith('BeatDivisor: '):
            repl = 'BeatDivisor: 4'
        elif line.startswith('GridSize'):
            repl = 'GridSize: 64'
        elif len(line.split(',')) in [6, 7] and config['taiko'] == True:
            hit_objects = line.split(',')
            hit_sound = int(hit_objects[4])
            if hit_sound | 2 == hit_sound:
                hit_sound = (hit_sound ^ 2) | 8
            repl = '256,192,' + ','.join(hit_objects[2:4]) + ',' + str(hit_sound) + ',' + ','.join(hit_objects[5:])
        if repl:
            to_write.append(repl+'\n')
        else:
            to_write.append(line+'\n')

    osu_to_save = os.path.join(extracted_oszs, f'{artist} - {title} ({creator}) [{version}].osu')

    f = open(osu_to_save, "a", encoding='utf8')
    f.writelines(to_write)
    f.close()

to_osz_folder = os.path.join(extracted_oszs)
move_file_list = glob.glob(to_osz_folder + "/*")
for item in move_file_list:
    shutil.move(item, to_osz)

zip_folder(to_osz, os.path.join(HOME, 'anonmaps.zip'))

shutil.rmtree(unzipped_maps)
shutil.rmtree(to_osz)
shutil.rmtree(extracted_oszs)

os.mkdir(outdir)
os.rename('./anonmaps.zip', os.path.join(outdir, f'{file_name}'))

print('Your contest entries are now anonymized')