import os
import sqlite3

_DATABASE_FILE = 'records.db'

_PARTICIPANT_REG_RESPONSES_TABLE_NAME = 'participant_reg_responses'
_MENTOR_REG_RESPONSES_TABLE_NAME = 'judge_reg_responses'
_JUDGE_REG_RESPONSES_TABLE_NAME = 'judge_reg_responses'

_PARTICIPANT_TABLE_NAME = 'participants'
_MENTOR_TABLE_NAME = 'mentors'
_JUDGE_TABLE_NAME = 'judges'


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
        f'CREATE TABLE {_PARTICIPANT_TABLE_NAME} ( discord_id INTEGER PRIMARY KEY, email TEXT OT NULL, team_id REFERENCES teams(id) )')
    cursor.execute(
        f'CREATE TABLE {_MENTOR_TABLE_NAME} ( discord_id INTEGER PRIMARY KEY, email TEXT NOT NULL )')
    cursor.execute(
        f'CREATE TABLE {_JUDGE_TABLE_NAME} ( discord_id INTEGER PRIMARY KEY, email TEXT NOT NULL )')

    # Teams
    cursor.execute('CREATE TABLE teams ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, category_channel_id INTEGER NOT NULL, text_channel_id INTEGER NOT NULL, voice_channel_id INTEGER NOT NULL, role_id INTEGER NOT NULL )')


def add_participant_response_entry(email: str, discord_tag: str):
    """Add a participant registration response entry to the records.

    Args:
        email (str): The email address for the entry to add
        discord_tag (str): The Discord tahg for the entry to add
    """

    _cursor.execute('INSERT INTO {_PARTICIPANT_REG_RESPONSES_TABLE_NAME} ( email, discord_tag ) VALUES ( :email, :discord_tag )', {
                    'email': email, 'discord_tag': discord_tag})


def add_mentor_response_entry(email: str, discord_tag: str):
    """Add a mentor registration response entry to the records.

    Args:
        email (str): The email address for the entry to add
        discord_tag (str): The Discord tahg for the entry to add
    """

    _cursor.execute('INSERT INTO {_MENTOR_REG_RESPONSES_TABLE_NAME} ( email, discord_tag ) VALUES ( :email, :discord_tag )', {
                    'email': email, 'discord_tag': discord_tag})


def add_judge_response_entry(email: str, discord_tag: str):
    """Add a judge registration response entry to the records.

    Args:
        email (str): The email address for the entry to add
        discord_tag (str): The Discord tahg for the entry to add
    """

    _cursor.execute('INSERT INTO {_JUDGE_REG_RESPONSES_TABLE_NAME} ( email, discord_tag ) VALUES ( :email, :discord_tag )', {
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

    return _cursor.execute('SELECT COUNT(*) FROM {_PARTICIPANT_REG_RESPONSES_TABLE_NAME} WHERE email=:email AND discord_tag=:discord_tag', {
        'email': email, 'discord_tag': discord_tag}).fetchone()[0] > 0


def mentor_response_exists(email: str, discord_tag: str) -> bool:
    """Check if there exists a mentor registration response entry with the
    given email address and Discord tag.

    Args:
        email (str): The email address
        discord_tag (str): The Discord tag

    Returns:
        bool: If there is a record with the given email address and Discord tag
    """

    return _cursor.execute('SELECT COUNT(*) FROM {_MENTOR_REG_RESPONSES_TABLE_NAME} WHERE email=:email AND discord_tag=:discord_tag', {
        'email': email, 'discord_tag': discord_tag}).fetchone()[0] > 0


def judge_response_exists(email: str, discord_tag: str) -> bool:
    """Check if there exists a judge registration response entry with the
    given email address and Discord tag.

    Args:
        email (str): The email address
        discord_tag (str): The Discord tag

    Returns:
        bool: If there is a record with the given email address and Discord tag
    """

    return _cursor.execute('SELECT COUNT(*) FROM {_JUDGE_REG_RESPONSES_TABLE_NAME} WHERE email=:email AND discord_tag=:discord_tag', {
        'email': email, 'discord_tag': discord_tag}).fetchone()[0] > 0


def add_participant(discord_id: int, email: str):
    """Add a record for a verified participant.

    There must not already exist a verified participant record with the same
    Discord ID.

    Args:
        discord_id (int): Discord ID of the participant
        email (str): Email address of the participant
    """

    _cursor.execute(f'INSERT INTO {_PARTICIPANT_TABLE_NAME} ( discord_id, email ) VALUES ( :discord_id, :email ) ', {
        'discord_id': discord_id, 'email': email
    })


def add_mentor(discord_id: int, email: str):
    """Add a record for a verified mentor.

    There must not already exist a verified mentor record with the same Discord
    ID.

    Args:
        discord_id (int): Discord ID of the mentor
        email (str): Email address of the mentor
    """

    _cursor.execute(f'INSERT INTO {_MENTOR_TABLE_NAME} ( discord_id, email ) VALUES ( :discord_id, :email ) ', {
        'discord_id': discord_id, 'email': email
    })


def add_judge(discord_id: int, email: str):
    """Add a record for a verified judge.

    There must not already exist a verified judge record with the same Discord
    ID.

    Args:
        discord_id (int): Discord ID of the judge
        email (str): Email address of the judge
    """

    _cursor.execute(f'INSERT INTO {_JUDGE_TABLE_NAME} ( discord_id, email ) VALUES ( :discord_id, :email ) ', {
        'discord_id': discord_id, 'email': email
    })


_db_file_exists = os.path.isfile(_DATABASE_FILE)
_connection = sqlite3.connect(_DATABASE_FILE, isolation_level=None)
_cursor = _connection.cursor()

if not _db_file_exists:
    _initialize_db(_cursor)

print('Hello!')
add_participant_response_entry('chen.10604@osu.edu', 'V⁰⁴#6118')
# print(participant_response_exists('chen.10604@osu.edu', 'V⁰⁴#6118'))
print('Goodbye!')
