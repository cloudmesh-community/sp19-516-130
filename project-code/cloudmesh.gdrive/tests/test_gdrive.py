from pprint import pprint
from cloudmesh.common.util import HEADING
from cloudmesh.gdrive.api.manager import Provider
from cloudmesh.management.configuration.config import Config
from cloudmesh.common.Printer import Printer

# nosetest -v --nopature
# nosetests -v --nocapture tests/test_gdrive.py

class TestName:


    def setup(self):

        scopes = 'https://www.googleapis.com/auth/drive'
        clientSecretFile = 'client_secret.json'
        applicationName = 'Drive API Python Quickstart'
        authInst = authentication.authentication(scopes, clientSecretFile, applicationName)
        credentials = authInst.get_credentials()

        http = credentials.authorize(httplib2.Http())
        drive_service = discovery.build('drive', 'v3', http=http)

        self.p = Provider.Provider(scopes,
                                   clientSecretFile,
                                   applicationName,
                                   authInst,
                                   credentials,
                                   http,
                                   drive_service,
                                  scriptpath)

    def test_01_configuration(self):
        HEADING()
        config = Config()
        credential = config["cloudmesh.storage.gdrive"]
        pprint(credential)

    def test_02_createFolder(self):
        HEADING()
        self.p.create_dir("testy")

        files = self.p.list()
        for entry in files:
            if entry["name"] == "testy":
                assert True

        assert False



class other:


    def test_02_git(self):
        HEADING()
        config = Config()
        username = config["cloudmesh.profile.github"]
        print ("Username:", username)
        keys = self.sshkey.get_from_git(username)
        pprint (keys)
        print(Printer.flatwrite(keys,
                            sort_keys=("name"),
                            order=["name", "fingerprint"],
                            header=["Name", "Fingerprint"])
              )

        assert len(keys) > 0
"""from __future__ import print_function
from docopt import docopt

# all this code has been taken and modified from 
#https://github.com/samlopezf/google-drive-api-tutorial
#https://developers.google.com/drive/api/v3/manage-uploads


import Provider
import authentication

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

scopes = 'https://www.googleapis.com/auth/drive'
clientSecretFile = 'client_secret.json'
applicationName = 'Drive API Python Quickstart'
authInst = authentication.authentication(scopes,clientSecretFile,applicationName)
credentials = authInst.get_credentials()


http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

if __name__ == "__main__":
    new_q = Provider.Provider(scopes,clientSecretFile,applicationName,authInst,credentials,http,drive_service,scriptpath)
    #new_q.createFolder("testy")
    #new_q.put("google_download.jpg")
    #new_q.getf("google_download.jpg")
    #new_q.deletef("google_download.jpg")
    #fileName = "photo_test.jpg"
    #query = "name contains " + str(fileName)
    #print(query)
    #new_q.searchFile("name contains 'photo_test'")
    #new_q.searchFile('photo')
    new_q.listFiles()
"""