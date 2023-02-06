import nextcord
from nextcord.ext import commands, application_checks
import records
import util

_intents = nextcord.Intents.default()

_bot = commands.Bot(intents=_intents)
_bot.default_guild_ids.append(int(util.config['discord']['guild_id']))


def create_team_channels(team: records.Team):
    pass


def delete_team_channels(team: records.Team):
    pass


@_bot.event
async def on_ready():
    print(
        f'STATUS: Connected to Discord as "{ _bot.user }", ID { _bot.user.id }')


@_bot.slash_command(description="Verify your Discord account for this event")
async def verify(
        interaction: nextcord.Interaction,
        email: str = nextcord.SlashOption(
            description="The email address you used to register for this event",
            required=True)):

    await interaction.response.defer(ephemeral=True)

    record = records.Participant.get_by_discord_id(interaction.user.id)

    # Participant is already verified
    if record is not None:
        await interaction.followup.send(ephemeral=True,
                                        content=f"You have already been verified. Head over to the { _bot.get_channel(int(util.config['discord']['start_here_channel_id'])).mention } channel for instructions on next steps.")
        return

    record = records.Participant.get_by_email(email)

    # Participant email not found
    if record is None:
        await interaction.followup.send(ephemeral=True,
                                        content=f"Verification failed. The email address `<{email}>` could not be found in our records. Registration is required in order to participate in this event. If you have not already registered, please register at { util.config['contact']['registration_link'] }, then run the `verify` command again. Please contact an organizer at `<{ util.config['contact']['organizer_email'] }`> or in the { _bot.get_channel(int(util.config['discord']['ask_organizer_channel_id'])).mention } channel if you believe this is an error.")
        return

    tag = f'{interaction.user.name}#{interaction.user.discriminator}'

    # Discord tag doesn't match records
    if record.discord_tag != tag:
        await interaction.followup.send(ephemeral=True,
                                        content=f"Verification failed. The email address `<{email}>` does not match your Discord tag `{tag}` in our records. Please contact an organizer at `<{ util.config['contact']['organizer_email'] }`> or in the { _bot.get_channel(int(util.config['discord']['ask_organizer_channel_id'])).mention } channel if you believe this is an error.")
        return

    record.discord_id = interaction.user.id

    await interaction.followup.send(ephemeral=True,
                                    content=f"You have been successfully verified. You now have access to the Discord server. Head over to the { _bot.get_channel(int(util.config['discord']['start_here_channel_id'])).mention } channel for instructions on next steps.")


@_bot.slash_command(description="Manually verify a participant")
@application_checks.has_role(int(util.config['discord']['organizer_role_id']))
async def manualverify(
        interaction: nextcord.Interaction,
        member: nextcord.Member = nextcord.SlashOption(
            description="The member to manually verify as a participant",
            required=True
        ),
        email: str = nextcord.SlashOption(
            description="The email address associated with the participant",
            required=True
        )):

    await interaction.response.defer(ephemeral=True)

    tag = f'{member.name}#{member.discriminator}'
    record = records.Participant.get_by_discord_tag(tag)

    if record is None:
        record = records.Participant.insert_record(email, tag)
    else:
        record.email = email

    record.discord_id = member.id

    await interaction.followup.send(ephemeral=True,
                                    content=f'`{tag}` has been manually verified as a Participant with email `{email}`')


@_bot.slash_command(description="Create a new team for this event")
async def createteam(
        interaction: nextcord.Interaction,
        name: str = nextcord.SlashOption(
            description="Name of your team",
            required=True
        ),
        participant1: nextcord.Member = nextcord.SlashOption(
            description="Participant to add to your team",
            required=True
        ),
        participant2: nextcord.Member = nextcord.SlashOption(
            description="Participant to add to your team",
            required=False
        ),
        participant3: nextcord.Member = nextcord.SlashOption(
            description="Participant to add to your team",
            required=False
        )):

    await interaction.response.defer

    participants = [interaction.user, participant1]
    if participant2 is not None:
        participants.append(participant2)
    if participant3 is not None:
        participants.append(participant3)

    participant_records = {}

    for participant in participants:
        participant_records[participant] = records.Participant.get_by_discord_id(
            participant.id)

    # Check if participants are not verified
    unverified_participants = filter(
        lambda pair: pair[1] is None, participant_records.items())
    if len(unverified_participants) > 0:
        unverified_tags = map(
            lambda pair: f'{pair[0].name}#{pair[0].discriminator}', unverified_participants)
        await interaction.followup.send(ephemeral=True,
                                        content=f"Team creation failed. These user(s) have not been verified: { ', '.join(unverified_tags) }")
        return

    # Check if participants are all not in teams
    teamed_participants = filter(
        lambda pair: pair[1].teamed, participant_records.items())
    if len(teamed_participants) > 0:
        teamed_tags = map(
            lambda pair: f'{pair[0].name}#{pair[0].discriminator}', teamed_participants)
        await interaction.followup.send(ephemeral=True,
                                        content=f"Team creation failed. These user(s) are already in a team: { ', '.join(teamed_tags) }")
        return


def start():
    _bot.run(util.config['discord']['token'])
