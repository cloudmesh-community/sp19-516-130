from __future__ import print_function
from docopt import docopt

import Provider
import auth

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

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()


http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

if __name__ == "__main__":
    new_q = Provider.Provider(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME,authInst,credentials,http,drive_service,scriptpath)
    #new_q.createFolder("testy")
    #new_q.put("photo_test.jpg")
    #new_q.get("photo_test.jpg")
    #new_q.delete("photo_test.jpg")
    #fileName = "photo_test.jpg"
    #query = "name contains " + str(fileName)
    #print(query)
    #new_q.searchFile("name contains 'photo_test'")
    #new_q.searchFile('photo')
    #new_q.listFiles()