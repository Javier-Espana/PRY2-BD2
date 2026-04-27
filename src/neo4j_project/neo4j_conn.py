"""Wrapper pequeño para la conexión al servidor Neo4j.

Provee un gestor de sesión seguro y útil para el resto del proyecto.
"""
from neo4j import GraphDatabase
from typing import Callable, Any
from .config import get_config


class Neo4jConnection:
    def __init__(self, config=None):
        self.config = config or get_config()
        self._driver = GraphDatabase.driver(self.config.uri, auth=(self.config.user, self.config.password))

    def close(self):
        if hasattr(self, "_driver") and self._driver:
            self._driver.close()

    def execute_write(self, fn: Callable, *args, **kwargs) -> Any:
        with self._driver.session() as session:
            return session.write_transaction(lambda tx: fn(tx, *args, **kwargs))

    def execute_read(self, fn: Callable, *args, **kwargs) -> Any:
        with self._driver.session() as session:
            return session.read_transaction(lambda tx: fn(tx, *args, **kwargs))


def get_connection():
    return Neo4jConnection()
