import io
import json
import mimetypes
import os
from pathlib import Path
import httplib2
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload
from cloudmesh.common.util import path_expand
from cloudmesh.storage.StorageABC import StorageABC
from apiclient import discovgirery
from cloudmesh.DEBUG import VERBOSE
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage



class Provider(StorageABC):
    """
    cloudmesh:
      ...
      gdrive:
        cm:
            heading: GDrive
            host: dgrive.google.com
            label: GDrive
            kind: gdrive
            version: TBD
        default:
            directory: TBD
        credentials:
            logging_level: 'ERROR'
            noauth_local_webserver: False
            page_size: 1000
            name: cloudmesh
            scope: "https://www.googleapis.com/auth/drive"
            location_secret: ~/.cloudmesh/gdrive/client_secret.json
            location_gdrive_credentials: ~/.cloudmesh/gdrive/.credentials/google-drive-credentials.json
            client_id: "6111111111111111111hjhkhhj.apps.googleusercontent.com"
            project_id: "whatever-it-is"
            auth_uri: "https://accounts.google.com/o/oauth2/auth"
            token_uri: "https://oauth2.googleapis.com/token"
            client_secret: "aaaaaaaaaaaaaaaaaaa"
            auth_provider_x509_cert_url: "https://www.googleapis.com/oauth2/v1/certs"
            auth_host_name: "localhost"
            auth_host_port:
            - "8080"
            - "8090"
            redirect_uris:
            - "urn:ietf:wg:oauth:2.0:oob"
            - "http://localhost"

    """
    def generate_flags_json(self):
        credentials = self.config.credentials("storage", "gdrive")
        args = argparse.Namespace(auth_host_name=credentials["auth_host_name"],
                                  auth_host_port=credentials["auth_host_port"],
                                  logging_level='ERROR', noauth_local_webserver=False)
        return args

    def get_credentials(self):

        """
            We have stored the credentials in ".credentials"
            folder and there is a file named 'google-drive-credentials.json'
            that has all the credentials required for our authentication
            If there is nothing stored in it this program creates credentials
            json file for future authentication
            Here the authentication type is OAuth2
        :return:
        :rtype:
        """
        #
        # Why is this not read from the yaml file?
        path = Path(path_expand(self.credential_file)).resolve()
        if not os.path.exists(path):
            os.makedirs(path)

        credentials_path = (path / 'google-drive-credentials.json').resolve()
        print(credentials_path)

        store = Storage(credentials_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.client_secret_file,
                                                  self.scopes)
            flow.user_agent = self.application_name
            #
            # SHOUDL THE FLAGS NOT BE SET IN THE YAML FILE OR DOCOPTS OFTHE COMMAND?
            #
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)

        return credentials

    def __init__(self, service='gdrive', config="~/.cloudmesh/cloudmesh.yaml"):

        super(Provider, self).__init__(service=service, config=config)
        self.cloud = service
        self.service = service

        self.applicationName = self.credentials["name"]
        self.page_size = self.credentials["page_size"]
        if self.page_size > 1000:
            Console.error("page size must be smaller than 1000")
            sys.exit(1)
        self.scopes = self.credentials["scope"]
        self.flags = self.generate_flags_json()
        #
        # Create directories if they do not exists. typically they will all be in one dir
        # do not execute the for loop if the directories exist
        for path in [self.credentials["location_secret"], self.credentials["location_gdrive_credentials"]]:
            path = os.path.dirname(Path(path).resolve())
            if not os.path.exists(path):
                os.makedirs(path)
        self.clientSecretFile = path_expand(self.credentials["location"])
        self.write_json_key(self.clientSecretFile, self.credentials)
        #This is the end of the if condition
        self.authInst = self.get_credentials()
        self.gdrive_credentials = self.authInst.get_credentials()
        self.http = self.gdrive_credentials.authorize(httplib2.Http())
        self.driveService = discovery.build('drive', 'v3', http=self.http)

    def write_json_key(self, path, credentials):

        directory = os.path.dirname(Path(path).resolve())
        if not os.path.exists(directory):
            os.makedirs(directory)

        #update the data based on the information of yaml file
        data = {
                "installed": {
                    "client_id": credentials["client_id"],
                    "project_id": credentials["project_id"],
                    "auth_uri": credentials["auth_uri"],
                    "token_uri": credentials["token_uri"],
                    "client_secret": credentials["client_secret"],#is this correct?
                    "auth_provider_x509_cert_url": credentials[
                        "auth_provider_x509_cert_url"],
                    "redirect_uris": credentials["redirect_uris"]
                }
            }
            with open(path, 'w') as fp:
                json.dump(data, fp)

    def gdrive_sourceid(self, query_params):
        sourceid = self.driveService.files().list(
            q=query_params,
            fields="nextPageToken, files(id, name, mimeType)").execute()
        return sourceid

    def gdrive_parentid(self, sourceid, directory):
        file_parent_id = None
        if len(sourceid['files']) == 0:
            parent_file = self.create_dir(directory=directory)
            file_parent_id = parent_file['id']
        else:
            print(sourceid['files'][0]['id'])
            file_parent_id = sourceid['files'][0]['id']
        return file_parent_id

    def put(self, service=None, source=None, destination=None, recursive=False):
        result = []
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
    #This needs to be done for all the functions in the same manner
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
                items = self.list(source=destination, recursive=False)
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
                items = self.list(source=destination, recursive=False)
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
            items = self.list(self, recursive=True)
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
            list_of_files = self.list(recursive=True)
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
            list_of_files = self.list(source=directory, recursive=False)
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


        # Merge the authentication code in to provier code successfully --> done
        # make the credentials path clear i.e., reading from cloudmesh.yaml --> done
        #createdir, list, search, delete all are working good
        #put and get recursive way is not working well enough
        #as it is suggested by prof. gregor the below put, get method needs to be followed.
        #go through the mongodb sequentially and create the folders in that fashion
        #then go through the files and make files similar to that in a parallel or sequential way
