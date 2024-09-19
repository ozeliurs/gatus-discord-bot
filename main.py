import discord
from discord import app_commands
import requests
from config import DISCORD_BOT_TOKEN
from gatus import get_service_status, get_service_group, GatusStatusError, nanoseconds_to_human_readable


bot = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(bot)

guild = ""


@tree.command(name="health", description="Check the health of a specific service")
async def health(interaction: discord.Interaction, service_name: str):
    try:
        service_status = get_service_status(service_name)

        embed_color = discord.Color.green() if service_status.status[-1].success else discord.Color.red()

        embed = discord.Embed(title=":helmet_with_white_cross: **Gatus**", color=embed_color)
        embed.description = f"Status for **{service_status.monitor_group}/{service_status.monitor_name}**"
        status_emoji = ":white_check_mark:" if service_status.status[-1].success else ":x:"
        status_text = "UP" if service_status.status[-1].success else "DOWN"

        embed.add_field(name="Status", value=f"{status_emoji} {status_text}", inline=False)
        status_history = ""
        for status in service_status.status:
            status_history += ":white_check_mark:" if status.success else ":x:"
        embed.add_field(name="History", value=status_history, inline=False)

        max_ping = max(status.duration for status in service_status.status)
        avg_ping = int(sum(status.duration for status in service_status.status) / len(service_status.status))
        min_ping = min(status.duration for status in service_status.status)

        # Define thresholds for ping categories (in nanoseconds)
        good_threshold = 200000000  # 200ms
        warning_threshold = 600000000  # 600ms

        # Determine emoji for each ping value
        min_emoji = ":white_check_mark:" if min_ping < good_threshold else (":warning:" if min_ping < warning_threshold else ":x:")
        avg_emoji = ":white_check_mark:" if avg_ping < good_threshold else (":warning:" if avg_ping < warning_threshold else ":x:")
        max_emoji = ":white_check_mark:" if max_ping < good_threshold else (":warning:" if max_ping < warning_threshold else ":x:")

        embed.add_field(name=f"{min_emoji} Min Ping", value=nanoseconds_to_human_readable(min_ping), inline=True)
        embed.add_field(name=f"{avg_emoji} Avg Ping", value=nanoseconds_to_human_readable(avg_ping), inline=True)
        embed.add_field(name=f"{max_emoji} Max Ping", value=nanoseconds_to_human_readable(max_ping), inline=True)
        await interaction.response.send_message(embed=embed)
    except GatusStatusError as e:
        await interaction.response.send_message(f"Error: {str(e)}")


@tree.command(name="ghealth", description="Check the health of all services in a group")
async def ghealth(interaction: discord.Interaction, group_name: str):
    try:
        service_group = get_service_group(group_name)
        embed = discord.Embed(title=":helmet_with_white_cross: **Gatus Group Health**", color=discord.Color.blue())
        embed.description = f"Status for group **{group_name}**"

        all_up = all(service.status[-1].success for service in service_group)
        all_down = all(not service.status[-1].success for service in service_group)

        if all_up:
            status_emoji = ":white_check_mark:"
            embed.color = discord.Color.green()
        elif all_down:
            status_emoji = ":x:"
            embed.color = discord.Color.red()
        else:
            status_emoji = ":warning:"
            embed.color = discord.Color.yellow()

        embed.add_field(name="Group Status", value=status_emoji, inline=False)

        for service in service_group:
            status_history = ""
            for status in service.status:
                status_history += ":white_check_mark:" if status.success else ":x:"
            embed.add_field(name=f"{service.monitor_name}", value=status_history, inline=False)

        await interaction.response.send_message(embed=embed)
    except GatusStatusError as e:
        await interaction.response.send_message(f"Error: {str(e)}")


@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1285980705456918568))
    print("Ready!")

# Run the bot
bot.run(DISCORD_BOT_TOKEN)
