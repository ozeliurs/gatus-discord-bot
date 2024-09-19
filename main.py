import discord
from discord import app_commands
import requests
from config import DISCORD_BOT_TOKEN
from gatus import get_service_status, get_service_group, GatusStatusError, nanoseconds_to_human_readable
from gatus_embeds import GatusHealthEmbed, GatusGroupHealthEmbed

bot = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(bot)


@tree.command(name="health", description="Check the health of a specific service")
async def health(interaction: discord.Interaction, service_name: str):
    try:
        service_status = get_service_status(service_name)
        embed = GatusHealthEmbed(service_status)
        await interaction.response.send_message(embed=embed)
    except GatusStatusError as e:
        await interaction.response.send_message(f"Error: {str(e)}")

@tree.command(name="ghealth", description="Check the health of all services in a group")
async def ghealth(interaction: discord.Interaction, group_name: str):
    try:
        service_group = get_service_group(group_name)
        embed = GatusGroupHealthEmbed(group_name, service_group)
        await interaction.response.send_message(embed=embed)
    except GatusStatusError as e:
        await interaction.response.send_message(f"Error: {str(e)}")


@bot.event
async def on_ready():
    await tree.sync()
    print("Ready!")

@bot.event
async def on_guild_join(guild):
    await tree.sync(guild=guild)
    print(f"Synced commands to guild: {guild.name}")

# Run the bot
bot.run(DISCORD_BOT_TOKEN)
