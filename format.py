import json
from osuapi import get_user
import csv
import os

def formatMask(path):
    print('Formatting output file')
    with open('./decode.json', 'r') as file:
        decoder = json.load(file)
    try:
        with open('./token.json', 'r') as file:
            token = json.load(file)
    except FileNotFoundError:
        print('token.json does not exist')
    except json.decoder.JSONDecodeError:
        print('token.json is not formatted properly, surround the values in double quotation marks')
    except KeyError:
        print('invalid api token provided')


    declist = list(decoder.items())
    aa = os.path.join(path, './masking.csv')
    with open(aa, 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(declist)):
            a = get_user(token['token'], declist[i][1])[0]['user_id']
            tow = [declist[i][1], a, declist[i][0]]
            writer.writerow(tow)
    return True