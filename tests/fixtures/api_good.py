"""Fixture: the same API module, conforming."""

import csv

import httpx


def load_all_commands():
    return list(
        Command.objects.select_related("client").values("id", "client__nom")
    )


def fetch_orders(url, page_size=50):
    """Bounded, batched, with a timeout."""
    with httpx.Client(timeout=5.0) as client:
        for page in iter_pages(client, url, page_size):
            yield from page


def export_all(path):
    with open(path, newline="") as f:
        for row in csv.reader(f):
            yield row


def search(items, needle):
    seen = set(items)
    return needle in seen


def query_users(conn, name):
    return conn.execute("SELECT id, name FROM users WHERE name = ?", (name,)).fetchall()
