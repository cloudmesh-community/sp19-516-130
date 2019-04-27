import io
import json
import mimetypes
import os
from pathlib import Path
import argparse
import httplib2
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload
from cloudmesh.common.util import path_expand
from cloudmesh.management.configuration.config import Config
from cloudmesh.storage.StorageABC import StorageABC
from cloudmesh.storage.provider.gdrive.Authentication import Authentication
from apiclient import discovery

class Provider(StorageABC):

    def __init__(self, service='gdrive', config="~/.cloudmesh/cloudmesh4.yaml"):
        
        super(Provider, self).__init__(service=service, config=config)
        self.limitFiles = 1000
        self.scopes = 'https://www.googleapis.com/auth/drive'
        # This is max value that can be set according to gdrive api
        self.clientSecretFile = path_expand(
            '~/.cloudmesh/gdrive/client_secret.json')
        self.applicationName = 'Drive API Python Quickstart'
        self.config = Config()
        print(os.path.abspath('~/.cloudmesh/cloudmesh4.yml'))
        self.generate_key_json()
        self.flags = self.generate_flags_json()
        self.authInst = Authentication(self.scopes,
                                       self.clientSecretFile,
                                       self.applicationName, flags=self.flags)
        self.credentials = self.authInst.get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.driveService = discovery.build('drive', 'v3', http=self.http)
        self.size = None
        self.cloud = service
        self.service = service

    def generate_flags_json(self):
        credentials = self.config.credentials("storage", "gdrive")
        args = argparse.Namespace(auth_host_name=credentials["auth_host_name"],
                                  auth_host_port=credentials["auth_host_port"],
                                  logging_level='ERROR', noauth_local_webserver=False)
        return args

    def generate_key_json(self):
        credentials = self.config.credentials("storage", "gdrive")
        config_path = '~/.cloudmesh/gdrive/client_secret.json'
        path = Path(path_expand(config_path)).resolve()
        config_folder = os.path.dirname(path)
        if not os.path.exists(config_folder):
            os.makedirs(config_folder)

        data = {"installed": {
            "client_id": credentials["client_id"],
            "project_id": credentials["project_id"],
            "auth_uri": credentials["auth_uri"],
            "token_uri": credentials["token_uri"],
            "client_secret": credentials["client_secret"],
            "auth_provider_x509_cert_url": credentials[
                "auth_provider_x509_cert_url"],
            "redirect_uris": credentials["redirect_uris"]
        }
        }
        with open(self.clientSecretFile, 'w') as fp:
            json.dump(data, fp)

    def put(self, service=None, source=None, destination=None, recursive=False):
        if recursive:
            if os.path.isdir(source):
                query_params = "name='" + destination + "' and trashed=false"
                sourceid = self.driveService.files().list(q=query_params,
                                                          fields="nextPageToken, files(id, name, mimeType)").execute()
                file_parent_id = None
                print(sourceid)
                if len(sourceid['files']) == 0:
                    parent_file = self.create_dir(directory=destination)
                    file_parent_id = parent_file['id']
                else:
                    print(sourceid['files'][0]['id'])
                    file_parent_id = sourceid['files'][0]['id']

                for f in os.listdir(source):
                    if os.path.isfile(os.path.join(source, f)):
                        self.upload_file(source=source, filename=f,
                                         parent_it=file_parent_id)
            else:
                query_params = "name='" + destination + "' and trashed=false"
                sourceid = self.driveService.files().list(q=query_params,
                                                          fields="nextPageToken, files(id, name, mimeType)").execute()
                file_parent_id = None
                print(sourceid)
                if len(sourceid['files']) == 0:
                    parent_file = self.create_dir(directory=destination)
                    file_parent_id = parent_file['id']
                else:
                    print(sourceid['files'][0]['id'])
                    file_parent_id = sourceid['files'][0]['id']

                return self.upload_file(source=None, filename=source, parent_it=file_parent_id)
        else:
            if os.path.isdir(source):
                query_params = "name='" + destination + "' and trashed=false"
                sourceid = self.driveService.files().list(q=query_params,
                                                          fields="nextPageToken, files(id, name, mimeType)").execute()
                file_parent_id = None
                print(sourceid)
                if len(sourceid['files']) == 0:
                    parent_file = self.create_dir(directory=destination)
                    file_parent_id = parent_file['id']
                else:
                    print(sourceid['files'][0]['id'])
                    file_parent_id = sourceid['files'][0]['id']

                for f in os.listdir(source):
                    if os.path.isfile(os.path.join(source, f)):
                        self.upload_file(source=source, filename=f,
                                         parent_it=file_parent_id)
            else:
                query_params = "name='" + destination + "' and trashed=false"
                sourceid = self.driveService.files().list(q=query_params,
                                                          fields="nextPageToken, files(id, name, mimeType)").execute()
                file_parent_id = None
                print(sourceid)
                if len(sourceid['files']) == 0:
                    parent_file = self.create_dir(directory=destination)
                    file_parent_id = parent_file['id']
                else:
                    print(sourceid['files'][0]['id'])
                    file_parent_id = sourceid['files'][0]['id']

                return self.upload_file(source=None, filename=source, parent_it=file_parent_id)

    def get(self, service=None, source=None, destination=None, recursive=False):
        if not os.path.exists(source):
            os.makedirs(source)

        if recursive:
            query_params = "name='" + destination + "' and trashed=false"
            sourceid = self.driveService.files().list(q=query_params,
                                                      fields="nextPageToken, files(id, name, mimeType)").execute()
            print(sourceid)
            file_id = sourceid['files'][0]['id']
            file_name = sourceid['files'][0]['name']
            mime_type = sourceid['files'][0]['mimeType']
            if mime_type == 'application/vnd.google-apps.folder':
                items = self.driveService.files().list(pageSize=self.limitFiles,
                                                     fields="nextPageToken, files(id, name,mimeType)").execute()
                for item in items:
                    if item['mimeType'] != 'application/vnd.google-apps.folder':
                        print("dbsakjdjksa")
                        print(item['mimeType'])
                        return self.download(source, item['id'], item['name'], item['mimeType'])
            else:
                return self.download(source, file_id, file_name, mime_type)
        else:
            query_params = "name='" + destination + "' and trashed=false"
            sourceid = self.driveService.files().list(q=query_params,
                                                      fields="nextPageToken, files(id, name, mimeType)").execute()
            print(sourceid)
            file_id = sourceid['files'][0]['id']
            file_name = sourceid['files'][0]['name']
            mime_type = sourceid['files'][0]['mimeType']
            if mime_type == 'application/vnd.google-apps.folder':
                items = self.driveService.files().list(pageSize=self.limitFiles,
                                                     fields="nextPageToken, files(id, name,mimeType)").execute()
                for item in items:
                    if item['mimeType'] != 'application/vnd.google-apps.folder':
                        print("dbsakjdjksa")
                        print(item['mimeType'])
                        return self.download_file(source, item['id'], item['name'], item['mimeType'])
            else:
                return self.download_file(source, file_id, file_name, mime_type)

    def delete(self, service='gdrive', filename=None,
               recursive=False):  # this is working
        file_id = ""
        if recursive:
            items = Provider.list(self, recursive=True)
            for i in range(len(items)):
                if items[i]['name'] == filename:
                    file_id = items[i]['id']

            try:
                self.driveService.files().delete(fileId=file_id).execute()
            except:  # errors.HttpError, error:
                return 'An error occurred:'  # %s' % error
        else:
            items = Provider.list(self, recursive=True)
            for i in range(len(items)):
                if items[i]['name'] == filename:
                    file_id = items[i]['id']
            try:
                self.driveService.files().delete(fileId=file_id).execute()
            except:  # errors.HttpError, error:
                return 'An error occurred:'  # %s' % error
        return "deleted"

    def create_dir(self, service='gdrive', directory=None):
        file_metadata = {'name': directory,
                         'mimeType': 'application/vnd.google-apps.folder'}
        file = self.driveService.files().create(body=file_metadata,
                                                fields='id').execute()
        print('Folder ID: %s' % file.get('id'))
        return file

    def list(self, service='gdrive', source=None, recursive=False):
        if recursive:
            results = self.driveService.files().list(pageSize=self.limitFiles,
                                                     fields="nextPageToken, files(id, name,mimeType)").execute()
            items = results.get('files', [])
            if not items:
                print('No files found.')
            else:
                return items
        else:
            query_params = "name='" + source + "' and trashed=false"
            sourceid = self.driveService.files().list(q=query_params,
                                                      pageSize=self.limitFiles,
                                                      fields="nextPageToken, files(id)").execute()
            file_id = sourceid['files'][0]['id']
            query_params = "'" + file_id + "' in parents"
            results = self.driveService.files().list(q=query_params,
                                                     pageSize=self.limitFiles,
                                                     fields="nextPageToken, files(id, name, mimeType)").execute()
            items = results.get('files', [])
            print(items)
            if not items:
                print('No files found.')
            else:
                return items

    def search(self, service='gdrive', directory=None, filename=None,
               recursive=False):
        if recursive:
            found = False
            list_of_files = self.driveService.files().list(pageSize=self.limitFiles,
                                                     fields="nextPageToken, files(id, name,mimeType)").execute()
            print(list_of_files)
            for file in list_of_files:
                print(file)
                if file['name'] == filename:
                    found = True
                    break
                else:
                    continue
            return found
        else:
            found = False
            list_of_files = self.driveService.files().list(pageSize=self.limitFiles,
                                                     fields="nextPageToken, files(id, name,mimeType)").execute()
            print(list_of_files)
            for file in list_of_files:
                print(file)
                if file['name'] == filename:
                    found = True
                    break
                else:
                    continue
            return found

    def upload_file(self, source, filename, parent_it):
        file_metadata = {'name': filename, 'parents': [parent_it]}
        self.driveService = self.driveService
        if source is None:
            filepath = filename
        else:
            filepath = source + '/' + filename
        media = MediaFileUpload(filepath,
                                mimetype=mimetypes.guess_type(filename)[0])
        file = self.driveService.files().create(body=file_metadata,
                                                media_body=media,
                                                fields='id').execute()
        return file

    def download_file(self, source, file_id, file_name, mime_type):
        filepath = source + '/' + file_name + mimetypes.guess_extension(mime_type)
        request = self.driveService.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        with io.open(filepath, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())
        return filepath


new_q = Provider(scopes,clientSecretFile,applicationName,authInst,credentials,http,driveService,scriptpath)
#new_q.createFolder("testy")
#new_q.put("photo_test.jpg")
#new_q.getf("testy")
#new_q.delete("photo_test.jpg")
#fileName = "photo_test.jpg"
#query = "name contains " + str(fileName)
#print(query)
#new_q.searchFile("name contains 'photo_test'")
#new_q.searchFile('photo')
new_q.listFiles()