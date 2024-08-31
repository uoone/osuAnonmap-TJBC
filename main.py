import zipfile
import os
import re
import sys
import shutil
import glob
from pathlib import Path

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname=arcname)

    return

def anonymization(file_path):
    file_name = file_path.split('/')[-1]
    HOME = os.getcwd()
    extracted_oszs = os.path.join(HOME, 'extracted_oszs')
    to_osz = os.path.join(HOME, 'to_osz')
    outdir = os.path.join(HOME, 'output')

    if os.path.exists(extracted_oszs):
        shutil.rmtree(extracted_oszs)
    if os.path.exists(to_osz):
        shutil.rmtree(to_osz)

    os.mkdir(outdir)
    os.mkdir(extracted_oszs)
    os.mkdir(to_osz)

    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(extracted_oszs)

    if len(os.listdir(os.path.join(extracted_oszs))) == 0:
        pass

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
            elif len(line.split(',')) in [6, 7]:
                hit_objects = line.split(',')
                hit_sound = int(hit_objects[4])
                if hit_sound | 2 == hit_sound:
                    hit_sound = (hit_sound ^ 2) | 8
                repl = '256,192,' + ','.join(hit_objects[2:4]) + ',' + str(hit_sound) + ',' + ','.join(hit_objects[5:])
            if repl:
                to_write.append(repl+'\n')
            else:
                to_write.append(line+'\n')

        artist = re.sub(r'[\\/:*?"<>|]+','', artist)
        title = re.sub(r'[\\/:*?"<>|]+','', title)
        creator = re.sub(r'[\\/:*?"<>|]+','', creator)
        version = re.sub(r'[\\/:*?"<>|]+','', version)
        osu_to_save = os.path.join(to_osz, f'{artist} - {title} ({creator}) [{version}].osu')

        f = open(osu_to_save, "a", encoding='utf8')
        f.writelines(to_write)
        f.close()

    copy_file_list = glob.glob(os.path.join(extracted_oszs) + "/*")
    for item in copy_file_list:
        if not item.endswith('.osu'):
            shutil.copy(item, to_osz)

    zip_folder(to_osz, os.path.join(outdir, f'{file_name}'))
    shutil.rmtree(to_osz)
    shutil.rmtree(extracted_oszs)

    return os.path.abspath(outdir)

if __name__ == "__main__":
    if Path(sys.argv[1]).exists():
        file_name = sys.argv[1]
        anonymization(os.path.join(os.getcwd(), file_name))
    else:
        sys.exit()