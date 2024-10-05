import records
import csv


'''
- Pull Data from CSV file
- For every entry, call the add_participant() method
'''


# FILENAME = "leaders.csv" 
# ATTR_DIS = "Discord is required"
# ATTR_EMAIL = "Q3"

FILENAME = "participants.csv" 
ATTR_DIS = "Discord Username"
ATTR_EMAIL = "Email"

with open(FILENAME, 'r') as csv_file:

    #Find delimiter of csv
    try:
        dialect = csv.Sniffer().sniff(csv_file.read(1024))    #Find type of delimiter "; or ,"
    except: 
        raise BaseException("Cannot determine iterator in csv file (; or ,)")
    csv_file.seek(0)

    #Attempt to Read file
    try:
        reader = csv.DictReader(csv_file, delimiter=",")
    except:
        raise BaseException("Cannot read/import csv file. Check format and resubmit")
    
    #Search through file for relevant user data
    userArr = []
    for user in reader:
        userData = {}
        
        #Gather email and discord_username
        for attr in user:

            #Find attributes and add them to user profile
            if(attr == ATTR_DIS and user[attr] != ""):
                userData['discord_username'] = user[attr]

            if(attr == ATTR_EMAIL and user[attr] != ""):
                userData['email'] = user[attr]

        if(userData):
            userArr.append(userData)
        

    #Add userArr Data to DB
    for i in range(len(userArr)):
        if ("participants" in FILENAME):
            try:
                records.add_participant_response_entry(userArr[i]['email'], userArr[i]['discord_username'])
                print(f'User {i}: Added')
            except:
                print("Error adding data to DB")
                break
        elif ("leaders" in FILENAME):
            try:
                records.add_mentor_response_entry(userArr[i]['email'], userArr[i]['discord_username'])
                print(f'Leader {i}: Added')
            except:
                print("Error adding data to DB")
                break

    #Check that all user have been entered
    for i in range(len(userArr)):
        if ("participants" in FILENAME):
            if not (records.participant_response_exists(userArr[i]['email'], userArr[i]['discord_username'])):
                print(f"User {i}: not found in Database")
        elif ("leaders" in FILENAME):
            if not (records.mentor_response_exists(userArr[i]['email'], userArr[i]['discord_username'])):
                print(f"Leader {i}: not found in Database")