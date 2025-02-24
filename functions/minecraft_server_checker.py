import pytz, re
from datetime import datetime
from mcstatus import JavaServer
from config.config import timezone


def clean_server_version(string: str):
    pattern = r"1\.\d{1,2}(?:\.\d{1,2})?(?:\.x)?(?:-1\.\d{1,2}(?:\.\d{1,2})?(?:\.x)?)?"

    string_without_white = re.sub(r"\s+", "", string)
    match = re.search(pattern, string_without_white)
    if match:
        return match.group(0)
    else:
        return "?"


def get_server_version(address: str):
    try:
        status = JavaServer.lookup(address).status()
        return [
            datetime.now(pytz.timezone(timezone)),
            clean_server_version(status.version.name),
        ]
    except Exception as e:
        print(f"Error while fetching the server [{address}] version: {e}")
        return None


def get_server_players(address: str):
    try:
        status = JavaServer.lookup(address).status()
        return [
            datetime.now(pytz.timezone(timezone)),
            status.players.online,
            status.players.max,
        ]
    except Exception as e:
        print(f"Error while fetching the server [{address}] players: {e}")
        return None


def get_server_ping(address: str):
    try:
        server = JavaServer.lookup(address)
        return [datetime.now(pytz.timezone(timezone)), server.ping()]
    except Exception as e:
        print(f"Error while fetching the server [{address}] ping: {e}")
        return None


def get_full_server_info(address: str):
    try:
        server = JavaServer.lookup(address)
        status = server.status()
        return [
            datetime.now(pytz.timezone(timezone)),
            clean_server_version(status.version.name),
            status.players.online,
            status.players.max,
        ]
    except Exception as e:
        return None
