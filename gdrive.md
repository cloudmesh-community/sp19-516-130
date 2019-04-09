
## Google Drive
Google Drive is a file storing platform where an user can store all his/her files in the google drive. Here files <br />
can be of any form ranging from documents to audio / video or image files. In free account each user will be <br />
given around 15 GB of free data space to be stored. We can create folders and subfolders in the Google Drive <br />
to store our data. <br />
 
Each file will be stored in Google cloud with a unique URL and it’s up to the user to make the file <br />
sharable or not. Google Drive is reliable and if an user has different devices and if he/she wants to access <br />
those files then Google Drive is needed in this case as he can have access to his file as all his files <br />
are stored in the cloud. The user does not need to install any kind of software in order to view these files.<br />
  
   
## Google Docs
Google docs is especially designed for viewing or editing or sharing the documents like Docs, Sheets, <br />
Slides, Forms. No need to install any software to access or edit these. And google doc can be sharable with <br />
editable option. There is an automatic mechanism to convert Microsoft documents to Google Docs. <br />

**Google Docs:** Google docs is a broader term for Google sheets, Google slides and Google forms. <br />

**Google Sheets:** Just like Microsoft excel sheet Google sheets has almost all of the functionalities. <br />
Google sheets can be shared with other people and can concurrently work on it and can edit it. We can change <br />
the font size, type as we want. We can use the formulas to calculate some mathematical expressions. This can be <br />
readily transformed to .csv or .xlsx format.<br />

**Google Slides:** Just like Microsoft PowerPoint presentation, Google has Googleslides. We can do small <br />
animations, transformations of slides. This can be shared with other people to edit this on real time basis.  <br />
We can change the font size, type of these as we want. <br />

**Google Forms:** Out of all Google docs this is the most powerful tool when anyone wants to collect data from <br />
other people. One can make a Google form and can share it via the link. The one who opens this link will see a <br />
form to fill. We can add many different types of survey questions with multiple choice or Multiple options, <br />
or text entries or date entries or choose from a list entry. This google forms can be used to conduct surveys <br />
within a close group like teachers, students or employees. <br />

**In a broader picture Google docs is just a subset of Google Drive**  <br />


## Python Google Drive API:

### Step-by-step process <br />

Before writing the Python interface for Google Drive, we need to setup an email account, with that email <br />
account we will get a set of google services and one of them is Google Drive with 15 GB overall storage. <br />

After that we need to go through the Google Drive Quick start guide given below: <br />
https://developers.google.com/drive/api/v3/quickstart/python  <br /> <br />

There we can see Enable API option as shown in the below picture: <br /> <br />

![image1](https://user-images.githubusercontent.com/26592419/55688921-6fd30e00-594c-11e9-9ced-da3202f39935.png)


Once we enable that we will get credentials.json file where all of our credentials are stored that can be used <br />
to communicate with our Google Drive through Python Interface. <br />
After that, we will be redirected to a page where we need to create our own project as shown in the below picture:<br /> <br />

![image2](https://user-images.githubusercontent.com/26592419/55689362-7e6ff400-5951-11e9-945e-0727a63f9357.png)

As we see below we need to select Google Drive API from here  <br /> <br />

![gd1](https://user-images.githubusercontent.com/26592419/55689509-32be4a00-5953-11e9-9fc8-8e7a8d87588b.png)


After that, we need to obtain the client_secret file as shown below:<br />
(The file that is downloaded as client_id.json needs to be renamed as client_secret.json) <br /> <br /> 

![image3](https://user-images.githubusercontent.com/26592419/55689414-22f23600-5952-11e9-83ff-5e21a2329455.png)

After this we need to click Done otherwise it would not set the Google Drive API <br /> 

After this if we run Authentication.py we will be redirected to our default browser to put our our login id and password and <br />
after that it asks to authenticate our credentials. If we allow that as shown below: <br /> <br />

![gd2](https://user-images.githubusercontent.com/26592419/55689531-99436800-5953-11e9-8aff-2ba64a481506.png)


We will get the screen something like given below (as the authentication pipeline has bees completed). <br /> <br />

![gd3](https://user-images.githubusercontent.com/26592419/55689565-f63f1e00-5953-11e9-978e-8a5c2b2f8228.png)

If the authentication flow is completed then the Authentication.py will create a "google-drive-credentials.json" file in <br />
".credentials" folder. This file can be used for future purposes. If we delete this file then the Authentication.py <br />
will again ask for login id and password and again create that file automatically. <br /> <br />

**So, now with the client_secret.json, google-drive-credentials.json and with Authentication.py and Provider.py our setup is ready**

<br />

Once all these steps are done correctly, then we can use the Python program interface to transfer the files <br />
between our Python program and Google Drive.<br />






## References:
https://www.cloudwards.net/how-does-google-drive-work/ <br />
https://whatis.techtarget.com/definition/Google-Docs <br />
https://www.techopedia.com/definition/13626/google-docs <br />
https://www.technokids.com/blog/apps/reasons-to-use-google-forms-with-your-students/ <br />
https://developers.google.com/drive/api/v3/quickstart/python <br />
https://github.com/samlopezf/google-drive-api-tutorial <br />
https://developers.google.com/drive/api/v3/manage-uploads <br />

