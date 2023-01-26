import os
import sqlite3

_DATABASE_FILE = "records.db"
_db_file_exists = os.path.isfile(_DATABASE_FILE)

_connection = sqlite3.connect(_DATABASE_FILE)
_cursor = _connection.cursor()

if not _db_file_exists:
    _cursor.execute(
        "CREATE TABLE participants ( id INTEGER PRIMARY KEY AUTOINCREMENT, email, discord_tag, discord_id, team_id REFERENCES teams(id) )")
    _cursor.execute(
        "CREATE TABLE teams ( id INTEGER PRIMARY KEY AUTOINCREMENT, name, role_id, channel_category_id, channel_text_id, channel_voice_id )")


class Participant:
    def __init__(self, record):
        self._id, self._email, self._discord_tag, self._discord_id, self._team_id = record

    def get_by_id(id):
        """Retrieves the participant with a matching ID

        Parameters:
            id: ID address to match

        Returns:
            a Participant associated with the record with the matching ID
        """
        return _cursor.execute("SELECT * FROM participants WHERE id=:id", {"id": id}).fetchone()

    def get_by_discord_id(discord_id):
        """Retrieves the participant with a matching discord ID

        Parameters:
            discord_id: discord ID address to match

        Returns:
            a Participant associated with the record with the matching discord
            ID, or None if no such record exists
        """
        retrieved_record = _cursor.execute(
            "SELECT * FROM participants WHERE discord_id=:discord_id", {"discord_id": discord_id}).fetchone()
        return None if retrieved_record is None else Participant(retrieved_record)

    def get_by_email(email):
        """Retrieves the participant with a matching email

        Parameters:
            email: email address to match

        Returns:
            a Participant associated with the record with the matching email, or
            None if no such record exists
        """
        retrieved_record = _cursor.execute(
            "SELECT * FROM participants WHERE email=:email", {"email": email}).fetchone()
        return None if retrieved_record is None else Participant(retrieved_record)

    def insert_record(email, discord_tag):
        """Insert a new participant record, updating an existing record if one
        with a matching email exists and has not been verified.

        Parameters:
            email: email address of participant
            discord_tag: discord tag of participant

        Returns:
            a Participant associated with this record
        """

        participant = Participant.get_by_email(email)

        if participant is None:
            _cursor.execute("INSERT INTO participants ( email, discord_tag ) VALUES (:email, :discord_tag)", {
                            "email": email, "discord_tag": discord_tag})
            _connection.commit()
            participant = Participant(_cursor.execute(
                "SELECT * FROM participants WHERE id=:id", {"id": _cursor.lastrowid}).fetchone())
        elif not participant.verified and participant.discord_tag != discord_tag:
            participant.discord_tag = discord_tag

        return participant

    @property
    def discord_tag(self):
        return self._discord_tag

    @discord_tag.setter
    def discord_tag(self, value):
        self._discord_tag = value
        _cursor.execute("UPDATE participants SET discord_tag=:discord_tag WHERE id=:id", {
                        "discord_tag": value, "id": self._id})
        _connection.commit()

    @property
    def team_id(self):
        return self._team_id

    @team_id.setter
    def team_id(self, value):
        self._team_id = value

        if value is None:
            _cursor.execute(
                "UPDATE participants SET team_id=NULL WHERE id=:id", {"id": self._id})
        else:
            _cursor.execute("UPDATE participants SET team_id=:team_id WHERE id=:id", {
                            "team_id": value, "id": self._id})

        _connection.commit()

    @property
    def discord_id(self):
        return self._discord_id

    @discord_id.setter
    def discord_id(self, value):
        self._discord_id = value
        _cursor.execute("UPDATE participants SET discord_id=:discord_id WHERE id=:id", {
                        "discord_id": value, "id": self._id})
        _connection.commit()

    @property
    def verified(self):
        return self.discord_id is not None

    @property
    def teamed(self):
        return self.team_id is not None


class Team:
    def __init__(self, record):
        self._id, self._name, self._role_id, self._channel_category_id, self._channel_text_id, self._channel_voice_id = record

    def get_by_id(id):
        return _cursor.execute("SELECT * FROM teams WHERE id=:id", {"id": id}).fetchone()

    def create(name, role_id, channel_category_id, channel_text_id, channel_voice_id):
        _cursor.execute("INSERT INTO teams ( name, role_id, channel_category_id, channel_text_id, channel_voice_id ) VALUES ( :name, :role_id, :channel_category_id, :channel_text_id, :channel_voice_id )", {
                        "name": name, "role_id": role_id, "channel_category_id": channel_category_id, "channel_text_id": channel_text_id, "channel_voice_id": channel_voice_id})
        _connection.commit()
        return Team(_cursor.execute("SELECT * FROM teams WHERE id=:id", {"id": _cursor.lastrowid}).fetchone())

    def drop(id):
        _cursor.execute("DELETE FROM teams WHERE id=:id", {"id": id})
        _connection.commit()

    def add_participant(self, participant):
        participant.team_id = self._id

    def drop_participant(self, participant):
        participant.team_id = None

    @property
    def size(self):
        return len(_cursor.execute("SELECT id FROM participants WHERE team_id=:team_id", {"team_id": self._id}).fetchall())

    @property
    def participants(self):
        return map(Participant.get_by_id, _cursor.execute("SELECT id FROM participants WHERE team_id=:team_id", {"team_id": self._id}).fetchall())

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        _cursor.execute("UPDATE teams SET name=:name WHERE id=:id", {
                        "name": value, "id": self._id})
        _connection.commit()

    @property
    def role_id(self):
        return self._role_id

    @property
    def channel_category_id(self):
        return self._channel_category_id

    @property
    def channel_text_id(self):
        return self._channel_text_id

    @property
    def channel_voice_id(self):
        return self._channel_voice_id
