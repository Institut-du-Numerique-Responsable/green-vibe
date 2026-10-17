"""Fixture: an API module gathering every detectable anti-pattern."""

import json
import time

import requests


def load_all_commands():
    commands = []
    for cmd in Command.objects.all():
        # N+1: relation access inside the loop over a queryset
        client_name = cmd.client.nom
        commands.append({"id": cmd.id, "client": client_name})
    return commands


def fetch_orders(url):
    data = []
    for order_id in range(1000):
        # remote call without timeout, inside a loop
        resp = requests.get(url + "/orders/" + str(order_id))
        data.append(resp.json())
    return data


def export_all(path):
    # whole-file read without a context manager
    f = open(path)
    content = f.read()
    rows = [r.split(",") for r in content]
    return rows


def slow_search(items, needle):
    # nested scans over growing data
    for a in items:
        for b in items:
            if a == needle and b == a:
                pass


def blocking_wait():
    time.sleep(10)
    return "done"


def query_users(conn):
    # SELECT * built by string concatenation
    sql = "SELECT * FROM users WHERE name = " + user_input
    return conn.execute(sql).fetchall()


def cache():
    # unbounded memo dict, no TTL
    memo = {}
    if user_input not in memo:
        memo[user_input] = expensive(user_input)
    return memo[user_input]
