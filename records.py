import os
import sqlite3

_DATABASE_FILE = 'records.db'

_PARTICIPANT_REG_RESPONSES_TABLE_NAME = 'participant_reg_responses'
_MENTOR_REG_RESPONSES_TABLE_NAME = 'mentor_reg_responses'
_JUDGE_REG_RESPONSES_TABLE_NAME = 'judge_reg_responses'

_PARTICIPANT_TABLE_NAME = 'participants'
_MENTOR_TABLE_NAME = 'mentors'
_JUDGE_TABLE_NAME = 'judges'

_TEAM_TABLE_NAME = 'teams'


def _initialize_db(cursor: sqlite3.Cursor):
    # Registration form responses
    cursor.execute(
        f'CREATE TABLE {_PARTICIPANT_REG_RESPONSES_TABLE_NAME} ( email TEXT NOT NULL, discord_tag TEXT NOT NULL )')
    cursor.execute(
        f'CREATE TABLE {_MENTOR_REG_RESPONSES_TABLE_NAME} ( email TEXT NOT NULL, discord_tag TEXT NOT NULL )')
    cursor.execute(
        f'CREATE TABLE {_JUDGE_REG_RESPONSES_TABLE_NAME} ( email TEXT NOT NULL, discord_tag TEXT NOT NULL )')

    # Verified users
    cursor.execute(
        f'CREATE TABLE {_PARTICIPANT_TABLE_NAME} ( discord_id INTEGER PRIMARY KEY, email TEXT OT NULL, team_id REFERENCES {_TEAM_TABLE_NAME}(id) )')
    cursor.execute(
        f'CREATE TABLE {_MENTOR_TABLE_NAME} ( discord_id INTEGER PRIMARY KEY, email TEXT NOT NULL )')
    cursor.execute(
        f'CREATE TABLE {_JUDGE_TABLE_NAME} ( discord_id INTEGER PRIMARY KEY, email TEXT NOT NULL )')

    # Teams
    cursor.execute(f'CREATE TABLE {_TEAM_TABLE_NAME} ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, category_channel_id INTEGER NOT NULL, text_channel_id INTEGER NOT NULL, voice_channel_id INTEGER NOT NULL, role_id INTEGER NOT NULL )')


def add_participant_response_entry(email: str, discord_tag: str):
    """Add a participant registration response entry to the records.

    Args:
        email (str): The email address for the entry to add
        discord_tag (str): The Discord tahg for the entry to add
    """

    _cursor.execute(
        f'INSERT INTO {_PARTICIPANT_REG_RESPONSES_TABLE_NAME} ( email, discord_tag ) VALUES ( :email, :discord_tag )', {
            'email': email, 'discord_tag': discord_tag})


def add_mentor_response_entry(email: str, discord_tag: str):
    """Add a mentor registration response entry to the records.

    Args:
        email (str): The email address for the entry to add
        discord_tag (str): The Discord tahg for the entry to add
    """

    _cursor.execute(
        f'INSERT INTO {_MENTOR_REG_RESPONSES_TABLE_NAME} ( email, discord_tag ) VALUES ( :email, :discord_tag )', {
            'email': email, 'discord_tag': discord_tag})


def add_judge_response_entry(email: str, discord_tag: str):
    """Add a judge registration response entry to the records.

    Args:
        email (str): The email address for the entry to add
        discord_tag (str): The Discord tahg for the entry to add
    """

    _cursor.execute(
        f'INSERT INTO {_JUDGE_REG_RESPONSES_TABLE_NAME} ( email, discord_tag ) VALUES ( :email, :discord_tag )', {
            'email': email, 'discord_tag': discord_tag})


def participant_response_exists(email: str, discord_tag: str) -> bool:
    """Check if there exists a participant registration response entry with the
    given email address and Discord tag.

    Args:
        email (str): The email address
        discord_tag (str): The Discord tag

    Returns:
        bool: If there is a record with the given email address and Discord tag
    """

    return _cursor.execute(
        f'SELECT COUNT(*) FROM {_PARTICIPANT_REG_RESPONSES_TABLE_NAME} WHERE email=:email AND discord_tag=:discord_tag',
        {
            'email': email,
            'discord_tag': discord_tag}).fetchone()[0] > 0


def mentor_response_exists(email: str, discord_tag: str) -> bool:
    """Check if there exists a mentor registration response entry with the
    given email address and Discord tag.

    Args:
        email (str): The email address
        discord_tag (str): The Discord tag

    Returns:
        bool: If there is a record with the given email address and Discord tag
    """

    return _cursor.execute(
        f'SELECT COUNT(*) FROM {_MENTOR_REG_RESPONSES_TABLE_NAME} WHERE email=:email AND discord_tag=:discord_tag',
        {
            'email': email,
            'discord_tag': discord_tag}).fetchone()[0] > 0


def judge_response_exists(email: str, discord_tag: str) -> bool:
    """Check if there exists a judge registration response entry with the
    given email address and Discord tag.

    Args:
        email (str): The email address
        discord_tag (str): The Discord tag

    Returns:
        bool: If there is a record with the given email address and Discord tag
    """

    return _cursor.execute(
        f'SELECT COUNT(*) FROM {_JUDGE_REG_RESPONSES_TABLE_NAME} WHERE email=:email AND discord_tag=:discord_tag',
        {
            'email': email,
            'discord_tag': discord_tag}).fetchone()[0] > 0


def add_participant(discord_id: int, email: str):
    """Add a record for a verified participant.

    There must not already exist a verified participant record with the same
    Discord ID.

    Args:
        discord_id (int): Discord ID of the participant
        email (str): Email address of the participant
    """

    _cursor.execute(
        f'INSERT INTO {_PARTICIPANT_TABLE_NAME} ( discord_id, email ) VALUES ( :discord_id, :email ) ', {
            'discord_id': discord_id, 'email': email})


def add_mentor(discord_id: int, email: str):
    """Add a record for a verified mentor.

    There must not already exist a verified mentor record with the same Discord
    ID.

    Args:
        discord_id (int): Discord ID of the mentor
        email (str): Email address of the mentor
    """

    _cursor.execute(
        f'INSERT INTO {_MENTOR_TABLE_NAME} ( discord_id, email ) VALUES ( :discord_id, :email ) ', {
            'discord_id': discord_id, 'email': email})


def add_judge(discord_id: int, email: str):
    """Add a record for a verified judge.

    There must not already exist a verified judge record with the same Discord
    ID.

    Args:
        discord_id (int): Discord ID of the judge
        email (str): Email address of the judge
    """

    _cursor.execute(
        f'INSERT INTO {_JUDGE_TABLE_NAME} ( discord_id, email ) VALUES ( :discord_id, :email ) ', {
            'discord_id': discord_id, 'email': email})


def is_verified_participant(discord_id: int) -> bool:
    """Check if a Discord user is verified as a participant.

    Args:
        discord_id (int): Discord ID of the Discord user

    Returns:
        bool: If the Discord user is verified as a participant
    """

    return _cursor.execute(
        f'SELECT COUNT(*) FROM {_PARTICIPANT_TABLE_NAME} WHERE discord_id=:discord_id', {
            'discord_id': discord_id}).fetchone()[0] > 0


def is_verified_mentor(discord_id: int) -> bool:
    """Check if a Discord user is verified as a mentor.

    Args:
        discord_id (int): Discord ID of the Discord user

    Returns:
        bool: If the Discord user is verified as a mentor
    """

    return _cursor.execute(
        f'SELECT COUNT(*) FROM {_MENTOR_TABLE_NAME} WHERE discord_id=:discord_id', {
            'discord_id': discord_id}).fetchone()[0] > 0


def is_verified_judge(discord_id: int) -> bool:
    """Check if a Discord user is verified as a judge.

    Args:
        discord_id (int): Discord ID of the Discord user

    Returns:
        bool: If the Discord user is verified as a judge
    """

    return _cursor.execute(
        f'SELECT COUNT(*) FROM {_JUDGE_TABLE_NAME} WHERE discord_id=:discord_id', {
            'discord_id': discord_id}).fetchone()[0] > 0


def create_team(
        name: str,
        category_channel_id: int,
        text_channel_id: int,
        voice_channel_id: int,
        role_id: int) -> int:
    """Create a record for a new team.

    Requires that no team record with the same name, category channel ID, text
    channele ID, voice channel ID, or role ID exists.

    Args:
        name (str): The name of the team
        category_channel_id (int): The ID of the team's category channel
        text_channel_id (int): The ID of the team's text channel
        voice_channel_id (int): The ID of the team's voice channel
        role_id (int): The ID of the team's role

    Returns:
        int: The ID of the team record
    """

    _cursor.execute(f'INSERT INTO {_TEAM_TABLE_NAME} ( name, category_channel_id, text_channel_id, voice_channel_id, role_id ) VALUES ( :name, :category_channel_id, :text_channel_id, :voice_channel_id, :role_id )', {
                    'name': name, 'category_channel_id': category_channel_id, 'text_channel_id': text_channel_id, 'voice_channel_id': voice_channel_id, 'role_id': role_id})
    return _cursor.lastrowid


def drop_team(team_id: int):
    """Drop a record for a team.

    Args:
        team_id (int): The ID of the team record
    """

    _cursor.execute(
        f'DELETE FROM {_TEAM_TABLE_NAME} WHERE id=:id', {'id': team_id})


def is_team_name_used(name: str) -> bool:
    """Check if a team record with the given name exists.

    Args:
        name (str): The team name to check

    Returns:
        bool: If there exists a team record with the given name
    """

    return _cursor.execute(
        f'SELECT COUNT(*) FROM {_TEAM_TABLE_NAME} WHERE name=:name', {
            'name': name}).fetchone()[0] > 0


def is_participant_in_team(discord_id: int) -> bool:
    """Check if a participant is in a team.

    Requires that discord_id is the Discord ID of a verfiied participant record.

    Args:
        discord_id (int): Discord ID of the participant

    Returns:
        bool: If the participant is in a team
    """

    return _cursor.execute(
        f'SELECT team_id FROM {_PARTICIPANT_TABLE_NAME} WHERE discord_id=:discord_id', {
            'discord_id': discord_id}).fetchone()[0] is not None


def get_team_id(discord_id: int) -> int:
    """Get the team record ID for a participant.

    Requires that discord_id is the Discord ID of a verified participant record
    and that the participant is in a team.

    Args:
        discord_id (int): Discord ID of the participant

    Returns:
        int: The ID of the participant's team
    """

    return _cursor.execute(
        f'SELECT team_id FROM {_PARTICIPANT_TABLE_NAME} WHERE discord_id=:discord_id', {
            'discord_id': discord_id}).fetchone()[0]


def add_to_team(discord_id: int, team_id: int):
    """Add a participant to a team.

    Requires that discord_id is the Discord ID of a verified participant record
    and that team_id is the ID of a team record.

    Args:
        discord_id (int): Discord ID of the participant
        team_id (int): ID of the team record
    """

    _cursor.execute(
        f'UPDATE {_PARTICIPANT_TABLE_NAME} SET team_id=:team_id WHERE discord_id=:discord_id', {
            'discord_id': discord_id, 'team_id': team_id})


def remove_from_team(discord_id: int):
    """Remove a participant from their team.

    Requires that discord_id is the Discord ID of a verified participant record.

    Args:
        discord_id (int): Discord ID of the participant
    """

    _cursor.execute(
        f'UPDATE {_PARTICIPANT_TABLE_NAME} SET team_id=NULL WHERE discord_id=:discord_id', {
            'discord_id': discord_id})


def get_team_size(team_id: int) -> int:
    """Get the number of members in a team.

    Requires that team_id is the ID of a team record.

    Args:
        team_id (int): ID of the team record
    """

    return _cursor.execute(
        f'SELECT COUNT(*) FROM {_PARTICIPANT_TABLE_NAME} WHERE team_id=:team_id', {
            'team_id': team_id}).fetchone()[0]


def get_team_name(team_id: int) -> str:
    """Get the name of a team.

    Requires that team_id is the ID of a team record.

    Args:
        team_id (int): ID of the team record

    Returns:
        str: Name of the team
    """

    return _cursor.execute(
        f'SELECT name FROM {_TEAM_TABLE_NAME} WHERE id=:team_id', {
            'team_id': team_id}).fetchone()[0]


def get_team_role_id(team_id: int) -> int:
    """Get the role ID for a team.

    Requires that team_id is the ID of a team record.

    Args:
        team_id (int): ID of the team record

    Returns:
        int: ID of the team role
    """

    return _cursor.execute(
        f'SELECT role_id FROM {_TEAM_TABLE_NAME} WHERE id=:team_id', {
            'team_id': team_id}).fetchone()[0]


def get_team_category_channel_id(team_id: int) -> int:
    """Get the category channel ID for a team.

    Requires that team_id is the ID of a team record.

    Args:
        team_id (int): ID of the team record

    Returns:
        int: ID of the team category channel
    """

    return _cursor.execute(
        f'SELECT category_channel_id FROM {_TEAM_TABLE_NAME} WHERE id=:team_id', {
            'team_id': team_id}).fetchone()[0]


def get_team_text_channel_id(team_id: int) -> int:
    """Get the text channel ID for a team.

    Requires that team_id is the ID of a team record.

    Args:
        team_id (int): ID of the team record

    Returns:
        int: ID of the team text channel
    """

    return _cursor.execute(
        f'SELECT text_channel_id FROM {_TEAM_TABLE_NAME} WHERE id=:team_id', {
            'team_id': team_id}).fetchone()[0]


def get_team_voice_channel_id(team_id: int) -> int:
    """Get the voice channel ID for a team.

    Requires that team_id is the ID of a team record.

    Args:
        team_id (int): ID of the team record

    Returns:
        int: ID of the team voice channel
    """

    return _cursor.execute(
        f'SELECT voice_channel_id FROM {_TEAM_TABLE_NAME} WHERE id=:team_id', {
            'team_id': team_id}).fetchone()[0]


def team_exists(team_id: int) -> bool:
    """Check if there exists a team record with a given team ID.

    Args:
        team_id (int): ID to check

    Returns:
        bool: If there exists a team with ID team_id
    """

    return _cursor.execute(
        f'SELECT COUNT(*) FROM {_TEAM_TABLE_NAME} WHERE id=:team_id', {
            'team_id': team_id}).fetchone()[0] > 0


_db_file_exists = os.path.isfile(_DATABASE_FILE)
_connection = sqlite3.connect(_DATABASE_FILE, isolation_level=None)
_cursor = _connection.cursor()

if not _db_file_exists:
    _initialize_db(_cursor)
