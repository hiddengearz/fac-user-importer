import requests
import csv
import os
import json
import sys

usersFile = ""
showHelp = False
username = ""
password = ""
ip = ""

for i, arg in enumerate(sys.argv):
    if '-h' in arg or '-help' in arg:
        showHelp = True
    elif '-f' in arg or '--file' in arg:
        usersFile = str(sys.argv[i+1])
    elif '-u' in arg or '--username' in arg:
        username = str(sys.argv[i+1])
    elif '-p' in arg or '--password' in arg:
        password = str(sys.argv[i+1])
    elif '-ip' in arg:
        ip = str(sys.argv[i+1])


if showHelp:
    print("-f, --file\t\t\t <filename.csv> The csv must have 3 columns column A for UserID, column B for Display Name and Column C for Email." +
    "The first row will be ignored as I assume it's headers e.g userid, name and emal")
    print("-u, --username\t\t\t <username> The username to login with")
    print("-p, --password\t\t\t <password> The API-Key to login with")
    print("-ip \t\t\t <ip> The IP of the fortiauthenticator")

else:
    payload = {"active": "true", "token_auth":"true","token_type":"ftm"}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

    completedUsers = []
    errors = []

    path = os.getcwd()

    with open(usersFile, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    for i,userData in enumerate(data):
        if i > 0:
            url = "https://" + ip + "/api/v1/ldapusers?email=" + userData[2]
            resp = requests.get(url, auth=(username, password), verify=False, headers=headers)
            if resp.status_code == 200:
                if len(resp.json()) == 2:
                    user = resp.json()
                    tmp = user["objects"]
                    try:
                        url2 = "https://" + ip + "/api/v1/ldapusers/" + str(tmp[0]["id"]) + "/"
                        resp2 = requests.patch(url2, json=payload, auth=(username, password), verify=False, headers=headers)
                        #print("Completed " + str(userData[2]))
                        completedUsers.append(str(userData[2]))
                    except:
                        errors.append('Error: not able to add token to ' + userData[2])
                
                else:
                    errors.append('Error: muletiple accounts found for ' + userData[2])
            else:
                errors.append(f'Error: unable to find an account with email: ' + userData[2])

    for user in completedUsers:
        print("Added: " + user)

    print("ERRRORS")
    for error in errors:
        print(error)

#resp = requests.post(url, json=payload, auth=(username, password), verify=False, headers=headers)
#resp2 = requests.get(url2, auth=(username, password), verify=False, headers=headers)
#print(resp)
#print(resp.content)
#print("####################################################################################################################################")
#print(resp2)
#print(resp2.json())

