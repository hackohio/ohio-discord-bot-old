import asyncio
import nextcord
from nextcord.ext import commands, application_checks
import records
import config

_intents = nextcord.Intents.default()
_intents.members = True

_bot = commands.Bot(intents=_intents)
_bot.default_guild_ids.append(config.discord_guild_id)

_MAX_TEAM_SIZE = 4
_TEAM_FORMATION_TIMEOUT = 60


async def _handle_permission_error(interaction: nextcord.Interaction, error: nextcord.ApplicationError):
    if isinstance(error, application_checks.errors.ApplicationMissingRole):
        await interaction.send(ephemeral=True,
                               content='You do not have permission to use this command.')
    else:
        raise error


async def _handle_team_formation_timeout(interaction: nextcord.Interaction, team_id: int):
    if records.team_exists(team_id) and records.get_team_size(team_id) <= 1:
        for record in records.get_team_members(team_id):
            await interaction.guild.get_member(record[0]).remove_roles(interaction.guild.get_role(config.discord_team_assigned_role_id))
            records.remove_from_team(record[0])
        await _delete_team(interaction.guild, team_id)
        await interaction.followup.send(ephemeral=True,
                                        content='Team formation timed out. Teams must have at least two members 1 minute after creation to be saved. You must re-create your team and use the `/addmember` command to add members to your team within one minute of using the `/createteam` command.')


async def _delete_team(guild: nextcord.Guild, team_id: int):
    await guild.get_role(records.get_team_role_id(team_id)).delete()
    await guild.get_channel(records.get_team_text_channel_id(team_id)).delete()
    # await guild.get_channel(records.get_team_category_channel_id(team_id)).delete()
    records.drop_team(team_id)


@_bot.event
async def on_ready():
    print(
        f'STATUS: Connected to Discord as "{ _bot.user }", ID { _bot.user.id }')


@_bot.slash_command(description="Verify your Discord account as a participant for this event")
async def verify(
    interaction: nextcord.Interaction,
    email: str = nextcord.SlashOption(
        description="Email address used to register for this event",
        required=True)):

    await interaction.response.defer(ephemeral=True)

    # User is already verified as a participant
    if records.is_verified_participant(interaction.user.id):
        await interaction.followup.send(ephemeral=True,
                                        content=f'Verification failed. You have already been verified. Head over to the {_bot.get_channel(config.discord_start_here_channel_id).mention} channel for instructions on your next steps.')
        return

    # User is not in the registration records
    if not records.participant_response_exists(
            email.lower(), str(interaction.user.name)):
        await interaction.followup.send(ephemeral=True,
                                        content=f'Verification failed. No registration record with email address `<{email}>` and Discord username `{interaction.user.name}` could be found. Registration is required to participate in this event. If you have not already registered, please register at {config.contact_registration_link}, then run the `/verify` command again. Please contact an organizer at `<{config.contact_organizer_email}>` or in the {_bot.get_channel(config.discord_ask_an_organizer_channel_id).mention} channel if you believe this is an error.')
        return

    # Happy case
    records.add_participant(interaction.user.id, email.lower())
    await interaction.user.add_roles(interaction.guild.get_role(
        config.discord_participant_role_id), interaction.guild.get_role(config.discord_verified_role_id))
    await interaction.followup.send(ephemeral=True,
                                    content=f'Verification succeeded. You now have access to the Discord server. Head over to the {_bot.get_channel(config.discord_start_here_channel_id).mention} channel for instructions on your next steps.')


@_bot.slash_command(description="Verify your Discord account as a mentor for this event")
async def mentify(
    interaction: nextcord.Interaction,
    email: str = nextcord.SlashOption(
        description="Email address used to register for this event",
        required=True)):

    await interaction.response.defer(ephemeral=True)

    # User is already verified as a mentor
    if records.is_verified_mentor(interaction.user.id):
        await interaction.followup.send(ephemeral=True,
                                        content=f'Verification failed. You have already been verified.')
        return

    # User is not in the registration records
    if not records.mentor_response_exists(
            email.lower(), str(interaction.user.name)):
        await interaction.followup.send(ephemeral=True,
                                        content=f'Verification failed. No registration record with email address `<{email}>` and Discord uername `{interaction.user.name}` could be found. Please contact an organizer at `<{config.contact_organizer_email}>` or in the {_bot.get_channel(config.discord_ask_an_organizer_channel_id).mention} channel if you believe this is an error.')
        return

    # Happy case
    records.add_mentor(interaction.user.id, email.lower())
    await interaction.user.add_roles(interaction.guild.get_role(
        config.discord_mentor_role_id), interaction.guild.get_role(config.discord_all_access_pass_role_id), interaction.guild.get_role(config.discord_verified_role_id))
    await interaction.followup.send(ephemeral=True,
                                    content=f'Verification succeeded. You now have access to the Discord server.')


# @_bot.slash_command(description="Verify your Discord account as a judge for this event")
# async def judgify(
    # interaction: nextcord.Interaction,
    # email: str = nextcord.SlashOption(
    #     description="Email address used to register for this event",
    #     required=True)):

    # await interaction.response.defer(ephemeral=True)

    # # User is already verified as a judge
    # if records.is_verified_judge(interaction.user.id):
    #     await interaction.followup.send(ephemeral=True,
    #                                     content=f'Verification failed. You have already been verified. Head over to the {_bot.get_channel(config.discord_start_here_channel_id).mention} channel for instructions on your next steps.')
    #     return

    # # User is not in the registration records
    # if not records.judge_response_exists(email.lower(), str(interaction.user.name)):
    #     await interaction.followup.send(ephemeral=True,
    #                                     content=f'Verification failed. No registration record with email address `<{email}>` and Discord username `{interaction.user.name}` could be found. Please contact an organizer at `<{config.contact_organizer_email}>` or in the {_bot.get_channel(config.discord_ask_an_organizer_channel_id).mention} channel if you believe this is an error.')
    #     return

    # # Happy case
    # records.add_judge(interaction.user.id, email.lower())
    # await interaction.user.add_roles(interaction.guild.get_role(
    #     config.discord_judge_role_id), interaction.guild.get_role(config.discord_all_access_pass_role_id), interaction.guild.get_role(config.discord_verified_role_id))
    # await interaction.followup.send(ephemeral=True,
    #                                 content=f'Verification succeeded. You now have access to the Discord server.')


@_bot.slash_command(description="Manually verify a Discord account as a participant for this event (Organizers only)")
@application_checks.has_role(config.discord_organizer_role_id)
async def overify(
        interaction: nextcord.Interaction,
        member: nextcord.Member = nextcord.SlashOption(
            description="The user to verify as a participant",
            required=True
        ),
        email: str = nextcord.SlashOption(
            description="The email address of the participant",
            required=True
        )):

    await interaction.response.defer(ephemeral=True)

    records.add_participant(member.id, email.lower())
    await member.add_roles(interaction.guild.get_role(config.discord_participant_role_id), interaction.guild.get_role(config.discord_verified_role_id))

    await interaction.followup.send(ephemeral=True,
                                    content=f'`{member} <{email}>` has been manually verified as a participant.')

overify.error(_handle_permission_error)


@_bot.slash_command(description="Manually verify a Discord account as a mentor for this event (Organizers only)")
@application_checks.has_role(config.discord_organizer_role_id)
async def omentify(
        interaction: nextcord.Interaction,
        member: nextcord.Member = nextcord.SlashOption(
            description="The user to verify as a mentor",
            required=True
        ),
        email: str = nextcord.SlashOption(
            description="The email address of the mentor",
            required=True
        )):

    await interaction.response.defer(ephemeral=True)

    records.add_mentor(member.id, email.lower())
    await member.add_roles(interaction.guild.get_role(
        config.discord_mentor_role_id), interaction.guild.get_role(config.discord_all_access_pass_role_id), interaction.guild.get_role(config.discord_verified_role_id))

    await interaction.followup.send(ephemeral=True,
                                    content=f'`{member} <{email}>` has been manually verified as a mentor.')

omentify.error(_handle_permission_error)


# @_bot.slash_command(description="Manually verify a Discord account as a judge for this event (Organizers only)")
# @application_checks.has_role(config.discord_organizer_role_id)
# async def ojudgify(
#         interaction: nextcord.Interaction,
#         member: nextcord.Member = nextcord.SlashOption(
#             description="The user to verify as a judge",
#             required=True
#         ),
#         email: str = nextcord.SlashOption(
#             description="The email address of the judge",
#             required=True
#         )):

#     await interaction.response.defer(ephemeral=True)

#     records.add_judge(member.id, email.lower())
#     await member.add_roles(interaction.guild.get_role(
#         config.discord_judge_role_id), interaction.guild.get_role(config.discord_all_access_pass_role_id), interaction.guild.get_role(config.discord_verified_role_id))

#     await interaction.followup.send(ephemeral=True,
#                                     content=f'`{member} <{email}>` has been manually verified as a judge.')

# ojudgify.error(_handle_permission_error)


@_bot.slash_command(description="Create a new team for this event")
@application_checks.has_role(config.discord_participant_role_id)
async def createteam(
        interaction: nextcord.Interaction,
        name: str = nextcord.SlashOption(
            description="Team name",
            required=True
        )):

    await interaction.response.defer(ephemeral=True)

    # Participant is already in a team
    # if records.is_participant_in_team(interaction.user.id):
    #     await interaction.followup.send(ephemeral=True,
    #                                     content=f'Team creation failed. You are already in the team {interaction.guild.get_role(records.get_team_role_id(records.get_team_id(interaction.user.id))).mention}. To create a new team, you must not currently be in a team.')
    #     return

    if len(name) > 90:
        await interaction.followup.send(ephemeral=True,
                                        content=f'Team creation failed. The team name `{name}` exceeds 90 characters. Team names must be between 1 and 90 characters long.')
        return

    # Team name is taken
    # if records.is_team_name_used(name):
    #     await interaction.followup.send(ephemeral=True,
    #                                     content=f'Team creation failed. There is already a team with the name `{name}`.')
    #     return


    team_role = await interaction.guild.create_role(name=name)
    
    #If new channel needs to be made
    team_id = records.get_max_team_id() + 1
    max_category_num = 3
    while(team_id > max_category_num):
        max_category_num += 3

    if (team_id == max_category_num - 2):
        category_channel = await interaction.guild.create_category_channel(name=f'Teams {max_category_num-2}-{max_category_num}',
                                                                        overwrites={
                                                                            team_role: nextcord.PermissionOverwrite(view_channel=True),
                                                                            interaction.guild.get_role(config.discord_all_access_pass_role_id): nextcord.PermissionOverwrite(view_channel=True)})
    else:
        #Find valid team below team id
        search_team_id = team_id - 1
        while(not records.team_exists(search_team_id)):
            search_team_id -= 1

        category_channel = interaction.guild.get_channel(records.get_team_category_channel_id(search_team_id))

    text_channel = await category_channel.create_text_channel(name=f'##-{name.lower().replace(" ", "-")}-text',
                                                                overwrites={
                                                                team_role: nextcord.PermissionOverwrite(view_channel=True),
                                                                interaction.guild.get_role(config.discord_all_access_pass_role_id): nextcord.PermissionOverwrite(view_channel=True)})

    team_id = records.create_team(
        name,
        text_channel.id,
        category_channel.id,
        team_role.id)
    
    records.add_to_team(interaction.user.id, team_id)
    await text_channel.edit(name=f'{team_id}-{name.lower().replace(" ", "-")}-text')
    await interaction.user.add_roles(team_role, interaction.guild.get_role(config.discord_team_assigned_role_id))
    await interaction.followup.send(ephemeral=True,
                                    content=f'Team creation succeeded. {team_role.mention} created. Make sure to add members to your team using the `/addmember` command. Teams with fewer than 2 members will be deleted after 1 minute.')




    # Start team formation timer
    await asyncio.sleep(_TEAM_FORMATION_TIMEOUT)
    await _handle_team_formation_timeout(interaction, team_id)

createteam.error(_handle_permission_error)


@_bot.slash_command(description="Add a member to your team")
@application_checks.has_role(config.discord_participant_role_id)
async def addmember(
        interaction: nextcord.Interaction,
        member: nextcord.Member = nextcord.SlashOption(
            description="Member to add",
            required=True
        )):

    await interaction.response.defer(ephemeral=True)

    # Not in a team
    if not records.is_participant_in_team(interaction.user.id):
        await interaction.followup.send(ephemeral=True,
                                        content=f'Failed to add team member. You are not currently in a team. You must be in a team to add a team member.')
        return

    # Team is full
    if records.get_team_size(records.get_team_id(
            interaction.user.id)) > _MAX_TEAM_SIZE:
        await interaction.followup.send(ephemeral=True,
                                        content=f'Failed to add team member. There is no space in your team. Teams can have a maximum of {_MAX_TEAM_SIZE} members.')
        return

    # Unverified member
    if not records.is_verified_participant(member.id):
        await interaction.followup.send(ephemeral=True,
                                        content=f'Failed to add team member. `{member}` is not a verified participant. All team members must be verified participants.')
        return

    # Member already in a team
    if records.is_participant_in_team(member.id):
        await interaction.followup.send(ephemeral=True,
                                        content=f'Failed to add team member. {member.mention} is already in a team. To join your team, they must leave their current team.')
        return

    # Happy path
    team_id = records.get_team_id(interaction.user.id)
    team_role = interaction.guild.get_role(records.get_team_role_id(team_id))
    records.add_to_team(member.id, team_id)
    await member.add_roles(team_role, interaction.guild.get_role(config.discord_team_assigned_role_id))
    await interaction.followup.send(ephemeral=True,
                                    content=f'Team member added successfully. {member.mention} has been added to {team_role.mention}.')
addmember.error(_handle_permission_error)


@_bot.slash_command(description="Leave your current team")
@application_checks.has_role(config.discord_participant_role_id)
async def leaveteam(
        interaction: nextcord.Interaction):

    await interaction.response.defer(ephemeral=True)

    # Not in a team
    if not records.is_participant_in_team(interaction.user.id):
        await interaction.followup.send(ephemeral=True,
                                        content=f'Failed to leave team. You are not currently in a team.')
        return

    # Happy path
    team_id = records.get_team_id(interaction.user.id)
    team_name = records.get_team_name(team_id)
    records.remove_from_team(interaction.user.id)
    await interaction.user.remove_roles(interaction.guild.get_role(records.get_team_role_id(team_id)), interaction.guild.get_role(config.discord_team_assigned_role_id))
    if records.get_team_size(team_id) == 0:
        await _delete_team(interaction.guild, team_id)

    await interaction.followup.send(ephemeral=True,
                                    content=f'Team left successfully. You have left `{team_name}`.')

leaveteam.error(_handle_permission_error)


def start():
    _bot.run(config.discord_token)
