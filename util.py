import configparser

_CONFIG_FILENAME = 'config.ini'

# Required configuration entries in _CONFIG_FILENAME, a list of tuples of
# (section: str, option: str)
_REQUIRED_CONFIG_ENTRIES = [
    ("discord", "guild_id"),
    ("discord", "token"),
]

config = configparser.ConfigParser()

try:
    config.read(_CONFIG_FILENAME)
except configparser.Error:
    print("ERROR: Error reading config file")
    exit(1)

for entry in _REQUIRED_CONFIG_ENTRIES:
    entry_value = config.get(entry[0], entry[1])
    if entry_value is None:
        print(
            f'ERROR: Missing required config entry "{entry[1]}" in section "{entry[0]}"')
        exit(1)
