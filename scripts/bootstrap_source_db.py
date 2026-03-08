from __future__ import annotations

import sqlite3
from pathlib import Path

from app.core.config import settings


def bootstrap_source_db() -> Path:
    db_path = Path(settings.source_db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS customers")
        cursor.execute("DROP TABLE IF EXISTS orders")

        cursor.execute(
            """
            CREATE TABLE customers (
                customer_id INTEGER PRIMARY KEY,
                customer_name TEXT NOT NULL,
                country TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
            )
            """
        )

        cursor.executemany(
            "INSERT INTO customers(customer_id, customer_name, country) VALUES (?, ?, ?)",
            [
                (1, "Alice Martin", "France"),
                (2, "Bruno Morel", "Belgique"),
                (3, "Carla Rossi", "Italie"),
            ],
        )
        cursor.executemany(
            "INSERT INTO orders(order_id, customer_id, amount, status) VALUES (?, ?, ?, ?)",
            [
                (101, 1, 125.50, "paid"),
                (102, 1, 52.00, "pending"),
                (103, 2, 78.90, "paid"),
                (104, 3, 310.00, "cancelled"),
            ],
        )
        connection.commit()

    return db_path


def main() -> None:
    db_path = bootstrap_source_db()
    print(f"Base source SQLite initialisée: {db_path}")


if __name__ == "__main__":
    main()
