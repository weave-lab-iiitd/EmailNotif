# EmailNotif

Steps to run the program:

1. Install necessary dependencies:
$ pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

2. Enable Gmail API

https://console.developers.google.com/apis/dashboard

  a. Go to the dashboard, and search for Gmail API and enable it.

![image](https://user-images.githubusercontent.com/16020553/113885577-93501e00-97dd-11eb-8a5d-604d9e65b119.png)


  b. create an OAuth 2.0 client ID by creating credentials (Go to the Create Credentials button):
  
  ![image](https://user-images.githubusercontent.com/16020553/113885804-c4305300-97dd-11eb-9b22-299d7a85afc2.png)

  c. Select Desktop App as the Application type and preceed, you'll see a window like this:
  
  ![image](https://user-images.githubusercontent.com/16020553/113885860-d01c1500-97dd-11eb-9255-7ac31e2c7d8e.png)

  d. We download our credentials file and save it as credentials.json in the current directory where we have stored the program files.
  
 3. In the program, change our_email to your address with which you created API authorization.
 4. The first time you run the program, you will be redirected to the browser to authenticate. This will create token.pickle file after authenticating with Google in your browser. After this, every time you run the program, authentication is not required. 
 
 ![image](https://user-images.githubusercontent.com/16020553/113886400-4587e580-97de-11eb-8b2a-04dff641d64b.png)

4. Necessary changes to be made within the program while calling search_messages() function as per the requirement.
