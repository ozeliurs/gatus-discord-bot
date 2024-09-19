import unittest
from unittest.mock import patch, MagicMock

from src.gatus import get_status, get_all_monitors, get_service_group, get_service_status, nanoseconds_to_human_readable, GatusStatusError

class TestGatusStatusFunctions(unittest.TestCase):
    @patch('requests.get')
    def test_get_status(self, mock_get):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = [{"name": "service1"}, {"name": "service2"}]
        mock_get.return_value = mock_response

        result = get_status()
        self.assertEqual(result, [{"name": "service1"}, {"name": "service2"}])

    @patch('requests.get')
    def test_get_status_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response

        with self.assertRaises(GatusStatusError):
            get_status()

    @patch('src.gatus.get_status')
    def test_get_all_monitors(self, mock_get_status):
        mock_get_status.return_value = [{"name": "service1"}, {"name": "service2"}]
        result = get_all_monitors()
        self.assertEqual(result, ["service1", "service2"])

    @patch('src.gatus.get_status')
    def test_get_all_monitors_error(self, mock_get_status):
        mock_get_status.return_value = [{"wrong_key": "service1"}]
        with self.assertRaises(GatusStatusError):
            get_all_monitors()

    @patch('src.gatus.get_status')
    def test_get_service_status(self, mock_get_status):
        mock_get_status.return_value = [{
            "name": "service1",
            "group": "group1",
            "results": [{"duration": 100, "success": True, "timestamp": 1234567890}]
        }]
        result = get_service_status("service1")
        self.assertEqual(result.monitor_name, "service1")
        self.assertEqual(result.monitor_group, "group1")
        self.assertEqual(len(result.status), 1)
        self.assertEqual(result.status[0].duration, 100)
        self.assertEqual(result.status[0].success, True)
        self.assertEqual(result.status[0].timestamp, 1234567890)

    @patch('src.gatus.get_status')
    def test_get_service_status_not_found(self, mock_get_status):
        mock_get_status.return_value = [{"name": "service1"}]
        with self.assertRaises(GatusStatusError):
            get_service_status("service2")

    @patch('src.gatus.get_status')
    def test_get_service_group(self, mock_get_status):
        mock_get_status.return_value = [
            {
                "name": "service1",
                "group": "group1",
                "results": [{"duration": 100, "success": True, "timestamp": 1234567890}]
            },
            {
                "name": "service2",
                "group": "group1",
                "results": [{"duration": 200, "success": False, "timestamp": 1234567891}]
            }
        ]
        result = get_service_group("group1")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].monitor_name, "service1")
        self.assertEqual(result[1].monitor_name, "service2")

    @patch('src.gatus.get_status')
    def test_get_service_group_not_found(self, mock_get_status):
        mock_get_status.return_value = [{"group": "group1"}]
        with self.assertRaises(GatusStatusError):
            get_service_group("group2")

    def test_nanoseconds_to_human_readable(self):
        self.assertEqual(nanoseconds_to_human_readable(500000), "0.50 ms")
        self.assertEqual(nanoseconds_to_human_readable(1500000000), "1.50 s")
        self.assertEqual(nanoseconds_to_human_readable(90000000000), "1 min 30.00 s")
        self.assertEqual(nanoseconds_to_human_readable(3661000000000), "1 h 1 min 1.00 s")
