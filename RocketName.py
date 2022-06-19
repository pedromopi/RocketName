import sqlite3
import pandas as pd
import os
from os.path import exists

def connect2sqlite(db_file):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("select ZRADOWNLOADMEDIA.ZUNIQUEID, ZRADOWNLOADUSER.ZUSERNAME from ZRADOWNLOADMEDIA left join ZRADOWNLOADUSER on ZRADOWNLOADMEDIA.ZUSER = ZRADOWNLOADUSER.Z_PK")
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=['Filename', 'Username'])
    return df
        
variablePath = os.getcwd()
databasePath = "\\RocketDatabases\\RocketDownloads.sqlite"
mediaPath = "\\RocketDownloads\\"

df = connect2sqlite(variablePath+databasePath)

size = df["Filename"].size

for i in range(size):
    try:  
        idFilePath = variablePath+mediaPath+df["Filename"][i]
        usernameFilePath = variablePath+mediaPath+df["Username"][i]
        idFilePathExt = idFilePath + ".png"
        usernameFilePathExt = usernameFilePath + ".png"

        if exists(idFilePathExt) == True:
            idFilename = idFilePathExt
            userFilename = usernameFilePathExt

        else:
            idFilePathExt = idFilePath + ".mp4"
            usernameFilePathExt = usernameFilePath + ".mp4"

            if exists(idFilePathExt) == True:
                idFilename = idFilePathExt
                userFilename = usernameFilePathExt

            else:
                pass

        def append_number(filename):
            name, ext = os.path.splitext(filename)
            return "{name}_{expand}{ext}".format(name=name,expand=expand, ext=ext)

        if os.path.isfile(userFilename):
            expand = 0
            while True:
                expand += 1
                new_file_name = append_number(userFilename)
                if os.path.isfile(new_file_name):
                    continue
                else:
                    userFilename = new_file_name
                    break
        os.rename(idFilename, userFilename)
    except:
        pass

mediaDir = variablePath+mediaPath
listOfFiles = os.listdir(mediaDir)
df2del = pd.DataFrame(listOfFiles, columns=['Filename'])
df2del = df2del[df2del['Filename'].str.contains("thumb")]
df2del = df2del.reset_index()
df2del = df2del[['Filename']]
sizeOfDel = df2del['Filename'].size

for i in range(sizeOfDel):
    try:
        os.remove(os.path.join(mediaDir, df2del['Filename'][i]))
    except OSError:
        pass

#pedromopi