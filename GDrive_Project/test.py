import Provider

new_q = Provider.Provider(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME,authInst,credentials,http,drive_service,scriptpath)
new_q.put("photo_test.jpg")
#new_q.get("photo_test.jpg")
#new_q.delete("photo_test.jpg")
fileName = "photo_test.jpg"
#query = "name contains " + str(fileName)
#print(query)
#new_q.searchFile("name contains 'photo_test'")
#new_q.searchFile('photo')