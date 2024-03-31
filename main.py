import zipfile
import os
import shutil
import json
import glob

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
maps = os.path.join(HOME, 'maps.zip')
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
    zip_ref.extractall(unzipped_maps)

extr = os.listdir(unzipped_maps)
for dir in extr:
    os.mkdir(os.path.join(extracted_oszs, dir))
    try:
        with zipfile.ZipFile(os.path.join(unzipped_maps, dir), 'r') as t_zip:
            t_zip.extractall(os.path.join(extracted_oszs, dir))
    except zipfile.BadZipFile:
        print('\nentry invalid %s' % os.path.join(unzipped_maps,dir))
        pass

osz_folders = os.listdir(extracted_oszs)
title_list = []
duplicated_title_list = []
print('Anonymizing .osz files')
for folder in osz_folders:
    if len(os.listdir(os.path.join(extracted_oszs, folder))) == 0:
        pass

    all_files = [x for x in os.listdir(os.path.join(extracted_oszs, folder))]
    for file in all_files:
        if file.endswith('.osb'):
            os.remove(os.path.join(extracted_oszs, folder, file))
        if os.path.isdir(os.path.join(extracted_oszs, folder, file)):
            shutil.rmtree(os.path.join(extracted_oszs, folder, file))
    osu_list = [x for x in os.listdir(os.path.join(extracted_oszs, folder)) if x.endswith('.osu')]
    img_list = [x for x in os.listdir(os.path.join(extracted_oszs, folder)) if x.endswith(('.jpg', '.png'))]
    audio_list = [x for x in os.listdir(os.path.join(extracted_oszs, folder)) if x.endswith(('.ogg', '.mp3'))]
    if len(osu_list) != config['numberDiffs']:
        if config['numberDiffs'] != 0:
            print('\nError: %s includes wrong number of .osu files' % folder)
            continue
    ctr = 0
    title = ''
    artist = ''
    audio_file_name = ''
    for file in osu_list:
        to_write = []
        with open(os.path.join(extracted_oszs, folder, file), encoding='utf8') as f:
            lines = [line.rstrip() for line in f]
        # set title and artist
        for line in lines:
            if line.startswith('Title:'):
                index = 1
                while True:
                    title = f'{line[6:].strip()}({index})'
                    if title not in title_list:
                        break
                    index += 1
                title_list.append(title)
            elif line.startswith('Artist:'):
                artist = line[7:].strip()
        # for upwrite
        for line in lines:
            repl = False
            if line.startswith('AudioFilename'):
                audio_file_name = line[14:].strip()
                for audio in audio_list:
                    # 使用する audio ファイルはリネームし、使用しないものは削除
                    if audio == audio_file_name:
                        os.rename(os.path.join(extracted_oszs, folder, audio), os.path.join(extracted_oszs, folder, f'{title}.mp3'))
                    else:
                        os.remove(os.path.join(extracted_oszs, folder, audio))
                repl = f'AudioFilename: {title}.mp3'
            elif line.startswith('DistanceSpacing: '):
                repl = 'DistanceSpacing: 1.4'
            elif line.startswith('BeatDivisor: '):
                repl = 'BeatDivisor: 4'
            elif line.startswith('TimelineZoom'):
                repl = 'TimelineZoom: 2.6'
            elif line.startswith('GridSize'):
                repl = 'GridSize: 64'
            elif line.startswith('Title:'):
                repl = f'Title:{config["tournamentName"]}'
            elif line.startswith('TitleUnicode:'):
                repl = f'TitleUnicode:{config["tournamentName"]}'
            elif line.startswith('Artist:'):
                repl = f'Artist:Various Artists'
            elif line.startswith('ArtistUnicode:'):
                repl = 'ArtistUnicode:Various Artists'
            elif line.startswith('Creator'):
                repl = f'Creator:{config["fileName"]}'
            elif line.startswith('Tags:'):
                repl = 'Tags:'
            elif line.startswith('CircleSize') and config['taiko'] ==True:
                repl = 'CircleSize:5'
            elif line.startswith('ApproachRate') and config['taiko'] ==True:
                repl = 'ApproachRate:5'
            elif line.startswith('Version:'):
                repl = f'Version:{artist} - {title}'
                if len(osu_list) > 1:
                    repl += ' ' + str(ctr+1)
                    ctr+=1
            elif line.startswith('Source'):
                repl = 'Source:'
            elif line.startswith('0,0,"'):
                bg = line.split(',')[2]
                bg = bg.replace('"', '')
                ext = bg[-4:]
                splt = line.split(',')
                repl = splt[0]+','+splt[1]+','+'"bg'+ext+'",'+splt[3]+','+splt[4]
                nname = 'bg'+ext
                bgp = os.path.join(extracted_oszs, folder, bg)
                try:
                    os.rename(bgp, os.path.join(extracted_oszs, folder, nname))
                except FileNotFoundError:
                    pass
            elif line.startswith("BeatmapID"):
                repl = 'BeatmapID:0'
            elif line.startswith('BeatmapSetID'):
                repl = 'BeatmapSetID:-1'
            elif line.startswith('Bookmarks'):
                repl = 'Bookmarks:'
            elif len(line.split(',')) == 6 and config['taiko'] ==True:
                repl = '256,192,'+','.join(line.split(',')[2:])
            elif len(line.split(',')) == 7 and config['taiko'] ==True:
                repl = '256,192,' + ','.join(line.split(',')[2:])
            if repl:
                to_write.append(repl+'\n')
            else:
                to_write.append(line+'\n')

        if len(osu_list) > 1:
            osu_to_save = os.path.join(extracted_oszs, folder, f'{config["fileName"]} ({config["fileName"]}{str(ctr)}) [{title}].osu')
        else:
            osu_to_save = os.path.join(extracted_oszs, folder, f'{config["fileName"]} ({config["fileName"]}) [{title}].osu')

        f = open(osu_to_save, "a", encoding='utf8')
        f.writelines(to_write)
        f.close()

        os.remove(os.path.join(extracted_oszs, folder, file))

    # all BGs removed (tentative)
    for img in img_list:
        os.remove(os.path.join(extracted_oszs, folder, img))
        # if img == bg:
        #     continue
        # else:
        #     os.remove(os.path.join(extracted_oszs, folder, img))

    to_osz_folder = os.path.join(extracted_oszs, folder)
    move_file_list = glob.glob(to_osz_folder + "/*")
    for item in move_file_list:
        shutil.move(item, to_osz)

zip_folder(to_osz, os.path.join(HOME, 'anonmaps.zip'))

shutil.rmtree(unzipped_maps)
shutil.rmtree(to_osz)
shutil.rmtree(extracted_oszs)

os.mkdir(outdir)
os.rename('./anonmaps.zip', os.path.join(outdir, f'{config["fileName"]}.osz'))

print('Your contest entries are now anonymized')