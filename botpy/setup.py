import dotenv
import os
from util import getjson, getPath


'''A script to check if all the necessary media files are available (e.g. DB, .env)'''

filesPath = getPath('../json/essentialFiles.json')
if not os.path.exists(filesPath):
    print('File \"json/essentialFiles.json\" does not exist')
    exit()

files = getjson(filesPath)
for file in files:
    path = getPath(file)
    if not os.path.exists(path):
        print(f'File \"{file}\" does not exist')
        exit()

dotenv.load_dotenv(getPath('../.env'))