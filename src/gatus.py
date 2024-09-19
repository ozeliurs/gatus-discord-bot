from dataclasses import dataclass
from typing import List

import requests

from src.config import GATUS_API_URL


class GatusStatusError(Exception):
    pass


@dataclass
class Status:
    duration: int
    success: bool
    timestamp: int


@dataclass
class ServiceStatus:
    monitor_name: str
    monitor_group: str
    status: List[Status]


def get_status():
    response = requests.get(f"{GATUS_API_URL}/v1/endpoints/statuses")

    if not response.ok:
        raise GatusStatusError(f"Failed to fetch service statuses.\nStatus Code: {response.status_code}\nResponse: {response.text}")

    return response.json()


def get_all_monitors() -> List[str]:
    services = get_status()

    try:
        return [service['name'] for service in services]
    except KeyError:
        raise GatusStatusError("Invalid response structure.")


def get_service_status(service_name: str) -> ServiceStatus:
    services = get_status()
    service = next((s for s in services if s['name'] == service_name), None)

    if not service:
        raise GatusStatusError(f"Service '{service_name}' not found.")

    return ServiceStatus(
        monitor_name=service['name'],
        monitor_group=service['group'],
        status=[Status(
            duration=s['duration'],
            success=s['success'],
            timestamp=s['timestamp']
        ) for s in service['results']]
    )


def get_service_group(group: str) -> List[ServiceStatus]:
    services = get_status()
    group_services = [s for s in services if s['group'] == group]

    if not group_services:
        raise GatusStatusError(f"No services found in group '{group}'.")

    return [ServiceStatus(
        monitor_name=service['name'],
        monitor_group=service['group'],
        status=[Status(
            duration=s['duration'],
            success=s['success'],
            timestamp=s['timestamp']
        ) for s in service['results']]
    ) for service in group_services]


def nanoseconds_to_human_readable(ns: int) -> str:
    seconds = ns / 1_000_000_000
    if seconds < 1:
        return f"{ns / 1_000_000:.2f} ms"
    elif seconds < 60:
        return f"{seconds:.2f} s"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        remaining_seconds = seconds % 60
        return f"{minutes} min {remaining_seconds:.2f} s"
    else:
        hours = int(seconds / 3600)
        remaining_minutes = int((seconds % 3600) / 60)
        remaining_seconds = seconds % 60
        return f"{hours} h {remaining_minutes} min {remaining_seconds:.2f} s"


def main():
    try:
        print(get_all_monitors())
        service_name = "ozeliurs-com"
        service_status = get_service_status(service_name)
        print(service_status)
    except GatusStatusError as e:
        print(e)


if __name__ == "__main__":
    main()
