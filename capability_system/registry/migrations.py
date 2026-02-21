from __future__ import annotations

from capability_system.persistence.database import Database


def run_migrations(database: Database) -> None:
    database.initialize()
