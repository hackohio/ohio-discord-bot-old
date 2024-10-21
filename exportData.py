import csv
import records
import os

#For all teams in the teamDB, get teamName and all users associated with it
# TeamData = [Team ID, TeamName, Member1, Member2, Member3, Member4]

HIGHEST_TEAM_ID = records.get_max_team_id()
team_data_list = []

for team_id in range(HIGHEST_TEAM_ID):
    team_data = []
    #If the team exists
    if (records.team_exists(team_id)):
        #Store id and name
        team_data.append(team_id)
        team_data.append(records.get_team_id) 
        
        #Look for members
        team_members = records.get_team_members(team_id)
        for member in team_members:
            team_data.append(member)

        #Append to data list
        team_data_list.append(team_data)

#----------- Export Data to CSV ---------------#

EXPORT_FILENAME = 'team_export.csv'

#Remove file if it exists so it can be overwritten
if os.path.isfile(EXPORT_FILENAME): os.remove(EXPORT_FILENAME)

with open(EXPORT_FILENAME, 'w') as csv_file:

    #Export Header Items
    headers = ['Team ID', 'Team name', 'Member1', 'Member2', 'Member3', 'Member4']
    writer = csv.DictWriter(csv_file, fieldnames=headers)
    writer.writeheader()

    #Add Rows of Data
    for team in team_data_list:
        writer.writerow(team)







