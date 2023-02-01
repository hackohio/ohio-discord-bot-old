import configparser

_config = configparser.ConfigParser()

try:
    _config.read_file("config.ini")
except configparser.Error:
    print("ERROR: Error reading config file")
    exit(1)


def discord_guild_id():
    """Get the Guild ID for the Discord server.

    Returns:
        guild ID for the Discord server
    """
    id = _config.get("discord", "guild_id")

    if id is None:
        print("ERROR: Missing config entry -- Discord guild_id")
        exit(1)

    return id
