import re, time, math
from database.connection import db
from config.config import (
    server_list_collection,
    server_list_update_in_seconds,
    servers_status_update_in_seconds,
)
from database.query import (
    get_my_collection,
    update_server_rankings,
    remove_inactive_servers,
    get_all_server_names_with_ids,
    set_server_offline,
    update_server_online,
)
from functions.minecraft_server_checker import get_full_server_info
from email_validator import validate_email, EmailNotValidError


def address_checker(address: str) -> bool:
    if address is None:
        return False

    regex = re.compile(
        r"""
            ^(
                (?:
                    (?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.
                    (?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.
                    (?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.
                    (?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])
                )
                |
                (?:
                    (?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}
                )
            )
            (?:\:(\d{1,5}))?$
            """,
        re.VERBOSE,
    )
    match = regex.match(address)
    if not match:
        return False

    ip_address = match.group(1)

    if ip_address and re.match(
        r"^(10\.|172\.(1[6-9]|2[0-9]|3[0-1])\.|192\.168\.|127\.)", ip_address
    ):
        return False

    if re.match(r".*\.local$", address):
        return False

    return True


def list_updater():
    while True:
        remove_inactive_servers(get_my_collection(db, server_list_collection))
        update_server_rankings(get_my_collection(db, server_list_collection))
        time.sleep(server_list_update_in_seconds)


def servers_updater():
    while True:
        servers = get_all_server_names_with_ids(
            get_my_collection(db, server_list_collection)
        )

        for server in servers:
            server_info = get_full_server_info(server["server_address"])

            if server_info is None:
                set_server_offline(
                    get_my_collection(db, server_list_collection), server["id"]
                )
            else:
                update_server_online(
                    get_my_collection(db, server_list_collection),
                    server["id"],
                    server_info[1],
                    server_info[2],
                    server_info[3],
                    server_info[0],
                )

            time.sleep(0.5)

        time.sleep(servers_status_update_in_seconds)


def get_max_pages(max_elements: int):
    max_pages = math.ceil(max_elements / 10)
    return max_pages


def page_button_navigation(current_page_number: int, max_elements: int, max_pages: int):
    if max_elements > 0:
        left_button_value = current_page_number - 1
        right_button_value = current_page_number + 1
        left_button_is_disabled = 0
        right_button_is_disabled = 0

        if current_page_number == 1:
            left_button_value = 1
            left_button_is_disabled = 1

        if current_page_number == max_pages:
            right_button_value = max_pages
            right_button_is_disabled = 1

        return [
            left_button_value,
            right_button_value,
            left_button_is_disabled,
            right_button_is_disabled,
        ]
    else:
        return [1, 1, 1, 1]


def email_checker(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
