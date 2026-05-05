"""Configuración y utilidades para cargar credenciales y parámetros.

Usar variables de entorno o un archivo `.env` local (no subir credenciales).
"""
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Neo4jConfig:
    uri: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user: str = os.getenv("NEO4J_USER", "neo4j")
    password: str = os.getenv("NEO4J_PASSWORD", "password")
    database: str = os.getenv("NEO4J_DATABASE", "neo4j")


def get_config() -> Neo4jConfig:
    return Neo4jConfig()
