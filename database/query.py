import pytz
from typing import List, Dict
from models import schemas
from bson import ObjectId
from pymongo.database import Database
from datetime import datetime, timedelta
from pymongo.collection import Collection
from config.config import (
    offline_server_delete_time_in_days,
    timezone,
    user_vote_cooldown_in_hours,
)


def get_my_collection(db: Database, collection: str) -> Collection:
    return db.get_collection(collection)


def get_document_count(collection: Collection) -> int:
    return collection.count_documents({})


def get_all_servers(collection: Collection) -> List[schemas.ServerMinimal]:
    servers = collection.find()
    return [schemas.ServerMinimal(**server) for server in servers]


def get_all_server_names_with_ids(collection: Collection) -> List[Dict[str, str]]:
    servers = collection.find({}, {"server_address": 1})
    return [
        {"id": str(server["_id"]), "server_address": server["server_address"]}
        for server in servers
    ]


def get_ranked_servers(
    collection: Collection, client_ip: str, page: int
) -> List[schemas.ServerListView]:
    now = datetime.now(pytz.timezone(timezone))
    selected_time_ago = now - timedelta(hours=user_vote_cooldown_in_hours)

    start_rank = (page - 1) * 10 + 1
    end_rank = start_rank + 9

    servers_cursor = collection.aggregate(
        [
            {"$match": {"ranking_position": {"$gte": start_rank, "$lte": end_rank}}},
            {"$sort": {"ranking_position": 1}},
            {"$limit": 10},
            {
                "$project": {
                    "server_address": 1,
                    "server_status": 1,
                    "server_version": 1,
                    "server_votes": 1,
                    "players_online": 1,
                    "players_max": 1,
                    "ranking_position": 1,
                    "votes": 1,
                }
            },
            {
                "$addFields": {
                    "liked": {
                        "$gt": [
                            {
                                "$size": {
                                    "$filter": {
                                        "input": "$votes",
                                        "as": "vote",
                                        "cond": {
                                            "$and": [
                                                {
                                                    "$eq": [
                                                        "$$vote.user_address",
                                                        client_ip,
                                                    ]
                                                },
                                                {
                                                    "$gte": [
                                                        "$$vote.timestamp",
                                                        selected_time_ago,
                                                    ]
                                                },
                                            ]
                                        },
                                    }
                                }
                            },
                            0,
                        ]
                    }
                }
            },
        ]
    )

    servers = []
    for server in servers_cursor:
        servers.append(
            schemas.ServerListView(
                server_address=server["server_address"],
                server_status=server["server_status"],
                server_version=server["server_version"],
                server_votes=server["server_votes"],
                players_online=server["players_online"],
                players_max=server["players_max"],
                ranking_position=server["ranking_position"],
                liked=server["liked"],
            )
        )

    return servers


def add_contact_request(
    collection: Collection, contact_request: schemas.ContactRequest
) -> bool:
    contact_data = contact_request.model_dump()

    result = collection.insert_one(contact_data)
    return result.acknowledged


def add_server_to_database(collection: Collection, server: schemas.Server) -> bool:
    if is_server_in_database(collection, server.server_address):
        return False

    highest_ranked_server = collection.find_one({}, sort=[("ranking_position", -1)])

    if highest_ranked_server:
        new_ranking_position = highest_ranked_server["ranking_position"] + 1
    else:
        new_ranking_position = server.ranking_position

    server_data = server.model_dump()
    server_data["ranking_position"] = new_ranking_position

    result = collection.insert_one(server_data)
    return result.acknowledged


def add_vote_to_server(
    collection: Collection, client_ip: str, server_name: str
) -> bool:
    now = datetime.now(pytz.timezone(timezone))
    selected_time_ago = now - timedelta(hours=user_vote_cooldown_in_hours)
    print(now)

    pipeline = [
        {"$match": {"server_address": server_name}},
        {
            "$project": {
                "already_voted": {
                    "$gt": [
                        {
                            "$size": {
                                "$filter": {
                                    "input": "$votes",
                                    "as": "vote",
                                    "cond": {
                                        "$and": [
                                            {"$eq": ["$$vote.user_address", client_ip]},
                                            {
                                                "$gte": [
                                                    "$$vote.timestamp",
                                                    selected_time_ago,
                                                ]
                                            },
                                        ]
                                    },
                                }
                            }
                        },
                        0,
                    ]
                }
            }
        },
    ]

    check_result = list(collection.aggregate(pipeline))
    if check_result and check_result[0].get("already_voted", False):
        return False

    result = collection.update_one(
        {"server_address": server_name},
        {
            "$inc": {"server_votes": 1},
            "$push": {"votes": {"timestamp": now, "user_address": client_ip}},
        },
    )

    return result.modified_count > 0


def set_server_offline(collection: Collection, server_id: str) -> bool:
    now = datetime.now(pytz.timezone(timezone))

    result = collection.update_one(
        {"_id": ObjectId(server_id)},
        {
            "$set": {
                "server_status": False,
                "server_last_check_timestamp": now,
                "server_last_offline_timestamp": now,
            }
        },
    )

    return result.modified_count > 0


def update_server_online(
    collection: Collection,
    server_id: str,
    server_version: str,
    players_online: int,
    players_max: int,
    update_time: datetime,
) -> bool:

    result = collection.update_one(
        {"_id": ObjectId(server_id)},
        {
            "$set": {
                "server_status": True,
                "server_version": server_version,
                "server_last_check_timestamp": update_time,
                "server_last_online_timestamp": update_time,
                "players_online": players_online,
                "players_max": players_max,
            },
            "$push": {
                "activity": {"timestamp": update_time, "players_online": players_online}
            },
        },
    )

    return result.modified_count > 0


# def update_server_rankings(collection: Collection):
#     servers = collection.find(
#         {}, {"server_status": 1, "players_online": 1, "server_votes": 1, "_id": 1}
#     )

#     if servers:
#         sorted_servers = sorted(
#             servers,
#             key=lambda server: (
#                 server["server_status"] == False,
#                 -(0.3 * server["players_online"] + 0.7 * server["server_votes"]),
#             ),
#         )

#         for rank, server in enumerate(sorted_servers, start=1):
#             collection.update_one(
#                 {"_id": server["_id"]}, {"$set": {"ranking_position": rank}}
#             )


def update_server_rankings(collection: Collection):

    pipeline = [
        {
            "$set": {
                "score": {
                    "$add": [
                        {"$multiply": [0.25, "$players_online"]},
                        {"$multiply": [0.75, "$server_votes"]},
                    ]
                }
            }
        },
        {
            "$set": {
                "composite": {
                    "$subtract": [
                        {
                            "$multiply": [
                                {"$cond": ["$server_status", 0, 1]},
                                1000000000,
                            ]
                        },
                        "$score",
                    ]
                }
            }
        },
        {
            "$setWindowFields": {
                "sortBy": {"composite": 1},
                "output": {"ranking_position": {"$documentNumber": {}}},
            }
        },
        {"$unset": ["score", "composite"]},
        {
            "$merge": {
                "into": collection.name,
                "on": "_id",
                "whenMatched": "merge",
                "whenNotMatched": "fail",
            }
        },
    ]

    list(collection.aggregate(pipeline))


def is_server_in_database(collection: Collection, address: str) -> bool:
    return collection.find_one({"server_address": address}) is not None


def count_servers_by_address(collection: Collection, search_value: str) -> int:
    search_value = search_value.lower()
    query = {"server_address": {"$regex": search_value, "$options": "i"}}
    return collection.count_documents(query)


def search_ranked_servers(
    collection: Collection, client_ip: str, search_value: str
) -> List[schemas.ServerListView]:
    now = datetime.now(pytz.timezone(timezone))
    selected_time_ago = now - timedelta(hours=user_vote_cooldown_in_hours)
    search_value = search_value.lower()

    servers_cursor = collection.aggregate(
        [
            {"$match": {"server_address": {"$regex": search_value, "$options": "i"}}},
            {
                "$addFields": {
                    "match_score": {
                        "$cond": {
                            "if": {"$eq": ["$server_address", search_value]},
                            "then": 2,
                            "else": {
                                "$cond": {
                                    "if": {
                                        "$regexMatch": {
                                            "input": "$server_address",
                                            "regex": f"{search_value}",
                                        }
                                    },
                                    "then": 1.5,
                                    "else": 1,
                                }
                            },
                        }
                    }
                }
            },
            {"$sort": {"match_score": -1, "ranking_position": 1}},
            {"$limit": 100},
            {
                "$project": {
                    "server_address": 1,
                    "server_status": 1,
                    "server_version": 1,
                    "server_votes": 1,
                    "players_online": 1,
                    "players_max": 1,
                    "ranking_position": 1,
                    "votes": 1,
                }
            },
            {
                "$addFields": {
                    "liked": {
                        "$gt": [
                            {
                                "$size": {
                                    "$filter": {
                                        "input": "$votes",
                                        "as": "vote",
                                        "cond": {
                                            "$and": [
                                                {
                                                    "$eq": [
                                                        "$$vote.user_address",
                                                        client_ip,
                                                    ]
                                                },
                                                {
                                                    "$gte": [
                                                        "$$vote.timestamp",
                                                        selected_time_ago,
                                                    ]
                                                },
                                            ]
                                        },
                                    }
                                }
                            },
                            0,
                        ]
                    }
                }
            },
        ]
    )

    servers = []
    for server in servers_cursor:
        servers.append(
            schemas.ServerListView(
                server_address=server["server_address"],
                server_status=server["server_status"],
                server_version=server["server_version"],
                server_votes=server["server_votes"],
                players_online=server["players_online"],
                players_max=server["players_max"],
                ranking_position=server["ranking_position"],
                liked=server["liked"],
            )
        )

    return servers


def remove_inactive_servers(collection: Collection):
    cutoff_date = datetime.now(pytz.timezone(timezone)) - timedelta(
        days=offline_server_delete_time_in_days
    )

    pipeline = [
        {
            "$match": {
                "server_status": False,
                "server_last_offline_timestamp": {"$ne": None},
                "server_last_offline_timestamp": {"$lt": cutoff_date},
            }
        },
        {"$project": {"_id": 1}},
    ]

    inactive_servers = collection.aggregate(pipeline)

    for server in inactive_servers:
        collection.delete_one({"_id": server["_id"]})
