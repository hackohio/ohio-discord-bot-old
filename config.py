import configparser

_CONFIG_FILENAME = 'config.ini'

# Required configuration entries in _CONFIG_FILENAME, a list of tuples of
# (section: str, option: str)
_REQUIRED_CONFIG_ENTRIES = [
    ('discord', 'guild_id'),
    ('discord', 'token'),
    ('discord', 'start_here_channel_id'),
    ('discord', 'ask_an_organizer_channel_id'),
    ('discord', 'organizer_role_id'),
    ('discord', 'participant_role_id'),
    ('discord', 'mentor_role_id'),
    ('discord', 'judge_role_id'),
    ('discord', 'team_assigned_role_id'),
    ('discord', 'all_access_pass_role_id'),
    ('contact', 'registration_link'),
    ('contact', 'organizer_email'),
]

_config = configparser.ConfigParser()

try:
    _config.read(_CONFIG_FILENAME)
except configparser.Error:
    print("ERROR: Error reading config file")
    exit(1)

for entry in _REQUIRED_CONFIG_ENTRIES:
    entry_value = _config.get(entry[0], entry[1])
    if entry_value is None:
        print(
            f'ERROR: Missing required config entry "{entry[1]}" in section "{entry[0]}"')
        exit(1)

discord_guild_id = int(_config['discord']['guild_id'])
discord_token = _config['discord']['token']
discord_start_here_channel_id = int(_config['discord']['start_here_channel_id'])
discord_ask_an_organizer_channel_id = int(_config['discord']['ask_an_organizer_channel_id'])
discord_organizer_role_id = int(_config['discord']['organizer_role_id'])
discord_participant_role_id = int(_config['discord']['participant_role_id'])
discord_mentor_role_id = int(_config['discord']['mentor_role_id'])
discord_judge_role_id = int(_config['discord']['judge_role_id'])
discord_team_assigned_role_id = int(_config['discord']['team_assigned_role_id'])
discord_all_access_pass_role_id = int(_config['discord']['all_access_pass_role_id'])
contact_registration_link = _config['contact']['registration_link']
contact_organizer_email = _config['contact']['organizer_email']
