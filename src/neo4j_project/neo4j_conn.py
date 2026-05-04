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

    def verify_connectivity(self) -> None:
        try:
            self._driver.verify_connectivity()
        except Exception as exc:
            raise RuntimeError(
                "No se pudo conectar a Neo4j en el URI configurado. "
                "Verifica NEO4J_URI, NEO4J_USER y NEO4J_PASSWORD."
            ) from exc

    def execute_write(self, fn: Callable, *args, **kwargs) -> Any:
        with self._driver.session() as session:
            if hasattr(session, "execute_write"):
                return session.execute_write(lambda tx: fn(tx, *args, **kwargs))
            return session.write_transaction(lambda tx: fn(tx, *args, **kwargs))

    def execute_read(self, fn: Callable, *args, **kwargs) -> Any:
        with self._driver.session() as session:
            if hasattr(session, "execute_read"):
                return session.execute_read(lambda tx: fn(tx, *args, **kwargs))
            return session.read_transaction(lambda tx: fn(tx, *args, **kwargs))


def get_connection():
    return Neo4jConnection()
