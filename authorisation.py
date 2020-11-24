import os
import pickle
import getpass
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
#we'll add deregister to delete the token

creds = None

def token_exists():
    """checks if the token file exists or not"""

    if os.path.exists('token.pickle'):
        # print('token_exists')
        return True
    return False


def get_creds():
    """gets credentials from the token"""
    
    with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    return creds


def token_valid():
    """Checks if the token is valid(not expired)"""

    if os.path.exists('token.pickle') and creds and creds.valid:
        # print('Token is valid')
        return True
    return False


def register_user():
    """Creates a new user"""

    print("Please enter your username and password to register")
    user = getpass.getuser()
    print(f'Username: {user}')
    password = getpass.getpass(prompt='Password: ')
    pass_comfirm = getpass.getpass(prompt='Confirm password: ')

    if password == pass_comfirm:
        print(f"Welcome to Code Clinic {user}")
    else:
        print("ERROR! Passwords don't match")
    user_details = {
        "user_name" : user,
        "password" : password   
    }
    with open('secret.json') as json_file:
        data = json.load(json_file)

    temp = data['user_infomation']
    temp.append(user_details)

    with open('secret.json','w') as f: 
        json.dump(data, f, indent=4) 
        

def user_login():
    """"logs in an existing user"""

    global creds

    print("Please enter your username and password to login")
    user = getpass.getuser()
    print(f'Username: {user}')
    password = getpass.getpass(prompt='Password: ')

    with open('secret.json') as json_file:
        json_object = json.load(json_file)
        
    user_details = {
        "user_name" : user,
        "password" : password   
    }

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())


    if user_details in json_object["user_infomation"]:
        print("Sucessful Login")
    else:
        print("Incorrect username or password")

creds = get_creds()