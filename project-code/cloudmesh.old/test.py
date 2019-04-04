from __future__ import print_function
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
    #new_q.putf("awer")