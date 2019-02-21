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

scriptpath = str(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0,scriptpath)
scriptpath = scriptpath 

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


import auth



class Provider:
    
    def __init__(self,SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME,authInst,credentials,http,drive_service,scriptpath):


        self.SCOPES = SCOPES
        self.CLIENT_SECRET_FILE = CLIENT_SECRET_FILE
        self.APPLICATION_NAME = APPLICATION_NAME
        self.authInst = authInst
        self.credentials = credentials
        self.http = http
        self.drive_service = drive_service
        self.scriptpath = scriptpath


        print("init {name}".format(name=self.__class__.__name__))

    def put(self, filename):#this is working fine
        file_metadata = {'name': filename}
        self.drive_service = drive_service
        
        #Hard coding
        
        filepath = filename
        mimetype = "image/jpeg"

        media = MediaFileUpload(filepath,
                            mimetype=mimetype)
        file = drive_service.files().create(body=file_metadata,
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
        file_id = "1vmC8PNQf48r2TAivi5NDNHY7MWBWL0jf"#fileId instead of file name
        #in the future for each file we have uploaded we need to store that 
        #info in a database and 
        filepath = "google_download.jpg"#file name in our local folder
        request = drive_service.files().get_media(fileId=file_id)
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

    def delete(self, file_id):#this is partially working
        try:
            #query = "name contains " + str(fileName)
            #size = 100
            #file_id = searchFile(query)
            file_id = "1vmC8PNQf48r2TAivi5NDNHY7MWBWL0jf"
            self.drive_service = drive_service
            try:
                drive_service.files().delete(fileId=file_id).execute()
            except:#errors.HttpError, error:
                print ('An error occurred:')# %s' % error
            print("put", fileName, file_id)
        except:
            print("No file named " + str(fileName) + " in the Google Drive")


        
    def searchFile(query):#this is not working
        size = 10
        results = drive_service.files().list(
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



SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()


http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

new_q = Provider(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME,authInst,credentials,http,drive_service,scriptpath)
new_q.put("photo_test.jpg")
#new_q.get("photo_test.jpg")
#new_q.delete("photo_test.jpg")
fileName = "photo_test.jpg"
#query = "name contains " + str(fileName)
#print(query)
#new_q.searchFile("name contains 'photo_test'")
#new_q.searchFile('photo')