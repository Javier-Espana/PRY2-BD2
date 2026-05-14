"""Fixtures compartidos para todas las suites de prueba."""

import os
import pytest
from dotenv import load_dotenv

load_dotenv()

from src.neo4j_conn import Neo4jConnection, get_connection
from src.app import SupplyChainApp


@pytest.fixture(scope="session")
def neo4j_uri():
    uri = os.getenv("NEO4J_URI")
    if not uri:
        pytest.fail("NEO4J_URI no esta definida. Configura el archivo .env")
    return uri


@pytest.fixture(scope="session")
def neo4j_user():
    return os.getenv("NEO4J_USER", "neo4j")


@pytest.fixture(scope="session")
def neo4j_password():
    password = os.getenv("NEO4J_PASSWORD")
    if not password:
        pytest.fail("NEO4J_PASSWORD no esta definida. Configura el archivo .env")
    return password


@pytest.fixture(scope="session")
def conn(neo4j_uri, neo4j_user, neo4j_password):
    connection = Neo4jConnection()
    try:
        connection.verify_connectivity()
    except RuntimeError as exc:
        pytest.fail(f"No se pudo conectar a Neo4j: {exc}")
    yield connection
    connection.close()


@pytest.fixture
def clean_db(conn):
    conn.execute_write(lambda tx: tx.run("MATCH (n) DETACH DELETE n"))
    yield
    conn.execute_write(lambda tx: tx.run("MATCH (n) DETACH DELETE n"))


@pytest.fixture
def app(conn):
    application = SupplyChainApp()
    application.conn = conn
    application.crud.conn = conn
    application.importer.conn = conn
    application.queries.conn = conn
    application.analytics.conn = conn
    yield application
    application.conn = None


@pytest.fixture
def test_supplier_data():
    return {
        "id_proveedor": 99901,
        "nombre": "Test Supplier",
        "pais": "Guatemala",
        "rating": 4.5,
        "activo": "true",
        "categorias": "Bebidas|Alimentos",
    }


@pytest.fixture
def test_product_data():
    return {
        "id_producto": 88801,
        "nombre": "Test Product",
        "categoria": "Bebidas",
        "precio": 10.5,
        "perecedero": "false",
        "fecha_expiracion": "",
    }
