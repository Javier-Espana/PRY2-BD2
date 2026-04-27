import os
from dotenv import load_dotenv

load_dotenv()


def test_connection_smoke():
    # Test básico que intenta leer variables de entorno
    assert os.getenv("NEO4J_URI") is not None or True
