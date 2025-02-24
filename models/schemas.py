import datetime
from typing import List
from pydantic import BaseModel


class Vote(BaseModel):
    timestamp: datetime.datetime
    user_address: str


class Activity(BaseModel):
    timestamp: datetime.datetime
    players_online: int


class Server(BaseModel):
    server_address: str
    server_status: bool
    server_version: str
    server_owner: str = "system"
    server_votes: int = 0
    server_last_check_timestamp: datetime.datetime
    server_last_online_timestamp: datetime.datetime
    server_last_offline_timestamp: datetime.datetime | None = None
    players_online: int
    players_max: int
    ranking_position: int = 0
    votes: List[Vote] = []
    activity: List[Activity] = []


class ServerMinimal(BaseModel):
    server_address: str
    server_status: bool
    server_version: str
    server_owner: str = "system"
    server_votes: int = 0
    server_last_check_timestamp: datetime.datetime
    server_last_online_timestamp: datetime.datetime
    server_last_offline_timestamp: datetime.datetime | None = None
    players_online: int
    players_max: int
    ranking_position: int = 0


class ServerListView(BaseModel):
    server_address: str
    server_status: bool
    server_version: str
    server_votes: int
    players_online: int
    players_max: int
    ranking_position: int
    liked: bool


class ContactRequest(BaseModel):
    requester_name: str
    requester_email: str
    requester_message: str
    requester_timestamp: datetime.datetime
    requester_address: str
