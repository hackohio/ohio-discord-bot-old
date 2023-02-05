import nextcord
from nextcord.ext import commands
import records
import util

_intents = nextcord.Intents.default()

_bot = commands.Bot(intents=_intents)
_bot.default_guild_ids.append(int(util.config['discord']['guild_id']))


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


def start():
    _bot.run(util.config['discord']['token'])
