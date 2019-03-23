# all this code has been taken and modified from 
#https://github.com/samlopezf/google-drive-api-tutorial
#https://developers.google.com/drive/api/v3/manage-uploads


from __future__ import print_function
import httplib2
import os, io
import sys

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

import pandas as pd
import json

scriptpath = str(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0,scriptpath)
scriptpath = scriptpath 

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


import authentication



class Provider:
    
    def __init__(self,scopes,clientSecretFile,applicationName,authInst,credentials,http,driveService,scriptpath):


        self.scopes = scopes
        self.clientSecretFile = clientSecretFile
        self.applicationName = applicationName
        self.authInst = authInst
        self.credentials = credentials
        self.http = http
        self.driveService = driveService
        self.scriptpath = scriptpath


        print("init {name}".format(name=self.__class__.__name__))

    def put(self, filename):#this is working fine
        file_metadata = {'name': filename}
        self.driveService = driveService

        """
        with open("FileTypes.json") as w:
            ft = json.loads(w)       


        filepath = filename
        mimetype = "image/jpeg"# initilization
        filenamelist = filename.split(".")
        fileForm = filenamelist[-1]
        try:

            mimetype = ft[str(fileForm)]

        except:
            mimetype = "image/jpeg"
            print("File format is adjusted to jpg style")
            """
        mimetype = "image/jpeg"
        filepath = filename
        media = MediaFileUpload(filepath,
                            mimetype=mimetype)
        file = driveService.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        print('File ID: %s' % file.get('id'))
        print("put", filename)
        #print("Hi")
        df = pd.read_csv("GDriveStorage.csv")
        #print(df)
        rowLength = df.shape[0]
        #rowLength = rowLength +1
        df.loc[rowLength,:] = rowLength
        df.loc[rowLength,"FileName"] = filename
        df.loc[rowLength,"FileID"] = file.get('id')
        #print(df)
        df.to_csv("GDriveStorage.csv")



    def get(self, filename):#this is working fine
        #hardcoded
        #in the future for each file we have uploaded we need to store that 
        #info in a database and 
        #file_id = searchFileLocally(filename)

        file_id = ""
        df = pd.read_csv("GDriveStorage.csv")
        for i in range(df.shape[0]):
            if df.loc[i,"FileName"] == filename:
                file_id = df.loc[i,"FileID"]
                #break
        next = str(int(df.shape[0] + 100)) #giving file name dynamically
        filepath = "google_download" +next + ".jpg"#file name in our local folder

        request = driveService.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        with io.open(filepath,'wb') as f:
            fh.seek(0)
            f.write(fh.read())
        print("gdrive provider get", filename)

    def delete(self, filename):#this is working
        
        file_id = ""
        df = pd.read_csv("GDriveStorage.csv")
        for i in range(df.shape[0]):
            if df.loc[i,"FileName"] == filename:
                file_id = df.loc[i,"FileID"]
                #df.drop(df.index[i])
                #break
        self.driveService = driveService
        try:
            driveService.files().delete(fileId=file_id).execute()
        except:#errors.HttpError, error:
            print ('An error occurred:')# %s' % error
        print("delete", filename, file_id)


    """    
    def searchFile(self,query):#this is not working
        size = 10
        results = driveService.files().list(
        pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(item)
                print('{0} ({1})'.format(item['name'], item['id']))
        return items[0]['id']

    def searchFileLocally(self,filename):
        fileID = ""
        df = pd.read_csv("GDriveStorage.csv")
        for i in range(len(df.shape[0])):
            if df.loc[i,"FileName"] == filename:
                fileID = df.loc[i,"FileID"]
                break

        return fileID

    """
    def createFolder(self,name):
        file_metadata = {'name': name,'mimeType': 'application/vnd.google-apps.folder'}
        self.driveService = driveService
    
    
        file = driveService.files().create(body=file_metadata,
                                        fields='id').execute()

        #needs to store this in a mongoDB
        print ('Folder ID: %s' % file.get('id'))
    def listFiles(self,size=10):
        self.size = size
        results = driveService.files().list(pageSize=size,fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print('{0} ({1})'.format(item['name'], item['id']))

    

scopes = 'https://www.googleapis.com/auth/drive'
clientSecretFile = 'client_secret.json'
applicationName = 'Drive API Python Quickstart'
authInst = authentication.authentication(scopes,clientSecretFile,applicationName)
credentials = authInst.get_credentials()


http = credentials.authorize(httplib2.Http())
driveService = discovery.build('drive', 'v3', http=http)

new_q = Provider(scopes,clientSecretFile,applicationName,authInst,credentials,http,driveService,scriptpath)
#new_q.createFolder("testy")
#new_q.put("photo_test.jpg")
#new_q.get("photo_test.jpg")
#new_q.delete("photo_test.jpg")
#fileName = "photo_test.jpg"
#query = "name contains " + str(fileName)
#print(query)
#new_q.searchFile("name contains 'photo_test'")
#new_q.searchFile('photo')