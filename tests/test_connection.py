"""Smoke tests: validacion rapida del proyecto."""

import os
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.mark.smoke
def test_env_variables_loaded():
    """Las variables de entorno deben estar definidas."""
    assert os.getenv("NEO4J_URI") is not None, "NEO4J_URI no esta definida"
    assert os.getenv("NEO4J_USER") is not None, "NEO4J_USER no esta definida"
    assert os.getenv("NEO4J_PASSWORD") is not None, "NEO4J_PASSWORD no esta definida"


@pytest.mark.smoke
def test_all_modules_importable():
    """Todos los modulos del proyecto deben ser importables."""
    from src import config, neo4j_conn, schema, importer, data_generator
    from src.crud_operations import CrudOperations
    from src.queries import CypherQueries
    from src.recommendation import AnalyticsEngine
    from src.app import SupplyChainApp
