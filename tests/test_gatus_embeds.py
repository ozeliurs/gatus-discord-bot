import unittest
from unittest.mock import Mock, patch
import discord

from src.gatus_embeds import GatusEmbed, GatusHealthEmbed, GatusGroupHealthEmbed
from src.gatus import nanoseconds_to_human_readable
from src.constants import EMOJI_HELMET, EMOJI_SUCCESS, EMOJI_WARNING

class TestGatusHealthEmbed(unittest.TestCase):
    def setUp(self):
        self.mock_service_status = Mock()
        self.mock_service_status.monitor_group = "TestGroup"
        self.mock_service_status.monitor_name = "TestService"
        self.mock_service_status.status = [Mock(success=True, duration=100000000) for _ in range(5)]

    def test_init(self):
        embed = GatusHealthEmbed(self.mock_service_status)
        self.assertEqual(embed.title, f"{EMOJI_HELMET} **Gatus**")
        self.assertEqual(embed.description, "Status for **TestGroup/TestService**")
        self.assertEqual(embed.color, discord.Color.green())

    def test_add_status(self):
        embed = GatusHealthEmbed(self.mock_service_status)
        self.assertIn("Status", [field.name for field in embed.fields])
        self.assertEqual(embed.fields[0].value, f"{EMOJI_SUCCESS} UP")

    def test_add_history(self):
        embed = GatusHealthEmbed(self.mock_service_status)
        self.assertIn("History", [field.name for field in embed.fields])
        self.assertEqual(embed.fields[1].value, EMOJI_SUCCESS * 5)

    @patch('src.gatus.nanoseconds_to_human_readable')
    def test_add_ping_info(self, mock_nanoseconds_to_human_readable):
        mock_nanoseconds_to_human_readable.return_value = "100ms"
        embed = GatusHealthEmbed(self.mock_service_status)
        self.assertIn(":white_check_mark: Min Ping", [field.name for field in embed.fields])
        self.assertIn(":white_check_mark: Avg Ping", [field.name for field in embed.fields])
        self.assertIn(":white_check_mark: Max Ping", [field.name for field in embed.fields])

class TestGatusGroupHealthEmbed(unittest.TestCase):
    def setUp(self):
        self.mock_service = Mock()
        self.mock_service.status = [Mock(success=True)]
        self.mock_service.monitor_name = "TestService"

    def test_init(self):
        embed = GatusGroupHealthEmbed("TestGroup", [self.mock_service])
        self.assertEqual(embed.title, f"{EMOJI_HELMET} **Gatus Group Health**")
        self.assertEqual(embed.description, "Status for group **TestGroup**")
        self.assertEqual(embed.color, discord.Color.green())

    def test_set_group_status_all_up(self):
        embed = GatusGroupHealthEmbed("TestGroup", [self.mock_service])
        self.assertEqual(embed.fields[0].name, "Group Status")
        self.assertEqual(embed.fields[0].value, EMOJI_SUCCESS)

    def test_set_group_status_mixed(self):
        mock_service_down = Mock()
        mock_service_down.status = [Mock(success=False)]
        embed = GatusGroupHealthEmbed("TestGroup", [self.mock_service, mock_service_down])
        self.assertEqual(embed.fields[0].name, "Group Status")
        self.assertEqual(embed.fields[0].value, EMOJI_WARNING)

    def test_add_service_statuses(self):
        embed = GatusGroupHealthEmbed("TestGroup", [self.mock_service])
        self.assertEqual(embed.fields[1].name, "TestService")
        self.assertEqual(embed.fields[1].value, EMOJI_SUCCESS)
