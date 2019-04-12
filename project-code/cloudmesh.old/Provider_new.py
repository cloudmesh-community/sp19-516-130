# all this code has been taken and modified from 
#https://github.com/samlopezf/google-drive-api-tutorial
#https://developers.google.com/drive/api/v3/manage-uploads


from __future__ import print_function
import httplib2
import os, io
import sys
from apiclient import discovery
from oauth2client import tools
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
import mimetypes

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

    def create_dir(self, service='gdrive', directory=None):
        file_metadata = {'name': directory, 'mimeType': 'application/vnd.google-apps.folder'}
        self.driveService = driveService

        file = driveService.files().create(body=file_metadata,
                                           fields='id').execute()

        print('Folder ID: %s' % file.get('id'))
        return file

    def list(self, service='gdrive', source=None, recursive=False):
        size = 10
        if recursive:
            self.size = size
            results = driveService.files().list(pageSize=size,
                                                fields="nextPageToken, files(id, name,mimeType)").execute()
            items = results.get('files', [])
            if not items:
                print('No files found.')
            else:
                return items
        else:
            queryParams = "name='" + source + "' and trashed=false"
            sourceid = driveService.files().list(q=queryParams, pageSize=size,
                                                 fields="nextPageToken, files(id)").execute()
            fileId = sourceid['files'][0]['id']
            queryParams = "'" + fileId + "' in parents"
            results = driveService.files().list(q=queryParams, pageSize=size,
                                                fields="nextPageToken, files(id, name, mimeType)").execute()
            items = results.get('files', [])
            # print(items)
            if not items:
                print('No files found.')
            else:
                return items

    def search(self, service='gdrive', directory=None, filename=None,
               recursive=False):
        if(recursive):
            found = False
            listOfFiles = self.list(recursive=True)
            print(listOfFiles)
            for file in listOfFiles:
                print(file)
                if (file['name'] == filename):
                    found = True
                    break
                else:
                    continue
            return found
        else:
            found = False
            listOfFiles = self.list(source=directory, recursive=False)
            print(listOfFiles)
            for file in listOfFiles:
                print(file)
                if(file['name']==filename):
                    found = True
                    break
                else:
                    continue
            return found

    def delete(self, service='gdrive', filename=None, recursive=False):  # this is working
        file_id = ""
        if(recursive):
            items = Provider.list(self, recursive=True)

            for i in range(len(items)):
                if items[i]['name'] == filename:
                    file_id = items[i]['id']

            self.driveService = driveService
            try:
                driveService.files().delete(fileId=file_id).execute()
            except:  # errors.HttpError, error:
                return 'An error occurred:'  # %s' % error
        else:
            items = Provider.list(self, recursive=True)
            for i in range(len(items)):
                if items[i]['name'] == filename:
                    file_id = items[i]['id']
            self.driveService = driveService
            try:
                driveService.files().delete(fileId=file_id).execute()
            except:  # errors.HttpError, error:
                return 'An error occurred:'  # %s' % error

    def get(self, service=None, source=None, destination=None, recursive=False):
        if not os.path.exists(source):
            os.makedirs(source)

        if recursive:
            queryParams = "name='" + destination + "' and trashed=false"
            sourceid = driveService.files().list(q=queryParams,
                                                 fields="nextPageToken, files(id, name, mimeType)").execute()
            print(sourceid)
            fileId = sourceid['files'][0]['id']
            fileName = sourceid['files'][0]['name']
            mimeType = sourceid['files'][0]['mimeType']
            if mimeType == 'application/vnd.google-apps.folder':
                items = self.list(source=destination, recursive=False)
                for item in items:
                    if (item['mimeType'] != 'application/vnd.google-apps.folder'):
                        print("dbsakjdjksa")
                        print(item['mimeType'])
                        self.download(source, item['id'], item['name'], item['mimeType'])
            else:
                self.download(source, fileId, fileName, mimeType)
        else:
            queryParams = "name='" + destination + "' and trashed=false"
            sourceid = driveService.files().list(q=queryParams, fields="nextPageToken, files(id, name, mimeType)").execute()
            print(sourceid)
            fileId = sourceid['files'][0]['id']
            fileName = sourceid['files'][0]['name']
            mimeType = sourceid['files'][0]['mimeType']
            if mimeType=='application/vnd.google-apps.folder':
                items = self.list(source=destination, recursive=False)
                for item in items:
                    if(item['mimeType']!='application/vnd.google-apps.folder'):
                        print("dbsakjdjksa")
                        print(item['mimeType'])
                        self.downloadFile(source, item['id'], item['name'], item['mimeType'])
            else:
                self.downloadFile(source, fileId, fileName, mimeType)

    def put(self, service=None, source=None, destination=None, recursive=False):
        if recursive:
            pass
        else:
            if(os.path.isdir(source)):
                queryParams = "name='" + destination + "' and trashed=false"
                sourceid = driveService.files().list(q=queryParams,
                                                     fields="nextPageToken, files(id, name, mimeType)").execute()
                fileParentId = None
                print(sourceid)
                if(len(sourceid['files'])==0):
                    parentFile = self.create_dir(directory=destination)
                    fileParentId = parentFile['id']
                else:
                    print(sourceid['files'][0]['id'])
                    fileParentId = sourceid['files'][0]['id']

                for f in os.listdir(source):
                    if os.path.isfile(os.path.join(source, f)):
                        self.uploadFile(source=source, filename=f, parentId=fileParentId)
            else:
                queryParams = "name='" + destination + "' and trashed=false"
                sourceid = driveService.files().list(q=queryParams,
                                                     fields="nextPageToken, files(id, name, mimeType)").execute()
                fileParentId = None
                print(sourceid)
                if (len(sourceid['files']) == 0):
                    parentFile = self.create_dir(directory=destination)
                    fileParentId = parentFile['id']
                else:
                    print(sourceid['files'][0]['id'])
                    fileParentId = sourceid['files'][0]['id']

                self.uploadFile(source=None, filename=source, parentId=fileParentId)



    def uploadFile(self, source, filename, parentId):
        file_metadata = {'name': filename, 'parents':[parentId]}
        self.driveService = driveService
        if (source==None):
            filepath = filename
        else:
            filepath = source + '/' + filename
        media = MediaFileUpload(filepath,
                                mimetype=mimetypes.guess_type(filename)[0])
        file = driveService.files().create(body=file_metadata,
                                           media_body=media,
                                           fields='id').execute()

    def downloadFile(self, source, file_id, fileName, mimeType):
        filepath = source + '/' + fileName + mimetypes.guess_extension(mimeType)
        request = driveService.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        with io.open(filepath, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())

scopes = 'https://www.googleapis.com/auth/drive'
clientSecretFile = 'client_secret.json'
applicationName = 'Drive API Python Quickstart'
authInst = authentication.authentication(scopes,clientSecretFile,applicationName)
credentials = authInst.get_credentials()


http = credentials.authorize(httplib2.Http())
driveService = discovery.build('drive', 'v3', http=http)

new_q = Provider(scopes,clientSecretFile,applicationName,authInst,credentials,http,driveService,scriptpath)
new_q.list('testy', recursive=True)
# new_q.create_dir(directory='jeevan')
# print(new_q.search(directory='testy', filename='photo_test.jpg',recursive=True))
#new_q.put("photo_test.jpg")
#new_q.get("photo_test.jpg")
# new_q.delete("jeevan")
# new_q.get(source='./test_new_code', destination='testy', recursive=False)
#new_q.put(source='GDriveStorage.csv', destination='testy_arv', recursive=False)
#fileName = "photo_test.jpg"
#query = "name contains " + str(fileName)
#print(query)
#new_q.searchFile("name contains 'photo_test'")
#new_q.searchFile('photo')