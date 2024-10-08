import discord

from src.gatus import nanoseconds_to_human_readable
from src.constants import EMOJI_HELMET, EMOJI_SUCCESS, EMOJI_WARNING, EMOJI_FAILURE

class GatusEmbed(discord.Embed):
    def __init__(self, title, description, color):
        super().__init__(title=title, description=description, color=color)

class GatusHealthEmbed(GatusEmbed):
    def __init__(self, service_status):
        embed_color = discord.Color.green() if service_status.status[-1].success else discord.Color.red()
        super().__init__(title=f"{EMOJI_HELMET} **Gatus**",
                         description=f"Status for **{service_status.monitor_group}/{service_status.monitor_name}**",
                         color=embed_color)

        self._add_status(service_status)
        self._add_history(service_status)
        self._add_ping_info(service_status)

    def _add_status(self, service_status):
        status_emoji = EMOJI_SUCCESS if service_status.status[-1].success else EMOJI_FAILURE
        status_text = "UP" if service_status.status[-1].success else "DOWN"
        self.add_field(name="Status", value=f"{status_emoji} {status_text}", inline=False)

    def _add_history(self, service_status):
        status_history = "".join(EMOJI_SUCCESS if status.success else EMOJI_FAILURE for status in service_status.status)
        self.add_field(name="History", value=status_history, inline=False)

    def _add_ping_info(self, service_status):
        max_ping = max(status.duration for status in service_status.status)
        avg_ping = int(sum(status.duration for status in service_status.status) / len(service_status.status))
        min_ping = min(status.duration for status in service_status.status)

        good_threshold = 200000000  # 200ms
        warning_threshold = 600000000  # 600ms

        min_emoji = self._get_ping_emoji(min_ping, good_threshold, warning_threshold)
        avg_emoji = self._get_ping_emoji(avg_ping, good_threshold, warning_threshold)
        max_emoji = self._get_ping_emoji(max_ping, good_threshold, warning_threshold)

        self.add_field(name=f"{min_emoji} Min Ping", value=nanoseconds_to_human_readable(min_ping), inline=True)
        self.add_field(name=f"{avg_emoji} Avg Ping", value=nanoseconds_to_human_readable(avg_ping), inline=True)
        self.add_field(name=f"{max_emoji} Max Ping", value=nanoseconds_to_human_readable(max_ping), inline=True)

    def _get_ping_emoji(self, ping, good_threshold, warning_threshold):
        if ping < good_threshold:
            return EMOJI_SUCCESS
        elif ping < warning_threshold:
            return EMOJI_WARNING
        else:
            return EMOJI_FAILURE


class GatusGroupHealthEmbed(GatusEmbed):
    def __init__(self, group_name, service_group):
        super().__init__(title=f"{EMOJI_HELMET} **Gatus Group Health**",
                            description=f"Status for group **{group_name}**",
                            color=discord.Color.blue())

        self._set_group_status(service_group)
        self._add_service_statuses(service_group)

    def _set_group_status(self, service_group):
        all_up = all(service.status[-1].success for service in service_group)
        all_down = all(not service.status[-1].success for service in service_group)

        if all_up:
            status_emoji = EMOJI_SUCCESS
            self.color = discord.Color.green()
        elif all_down:
            status_emoji = EMOJI_FAILURE
            self.color = discord.Color.red()
        else:
            status_emoji = EMOJI_WARNING
            self.color = discord.Color.yellow()

        self.add_field(name="Group Status", value=status_emoji, inline=False)

    def _add_service_statuses(self, service_group):
        for service in service_group:
            status_history = "".join(EMOJI_SUCCESS if status.success else EMOJI_FAILURE for status in service.status)
            self.add_field(name=f"{service.monitor_name}", value=status_history, inline=False)
