import time
import sys
from dotenv import load_dotenv
from pathlib import Path
import sys

# Cargar .env desde la raíz
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env')

# Asegurar que el paquete `src` sea importable cuando ejecutamos desde scripts/
sys.path.insert(0, str(ROOT))

print('Esperando 60 segundos antes de intentar conectar a Neo4j (por favor espera)...')
time.sleep(60)

try:
    from src.neo4j_conn import get_connection
except Exception as e:
    print('Error importando el wrapper de Neo4j:', e)
    sys.exit(2)

conn = get_connection()
print('Intentando verify_connectivity()...')
try:
    conn.verify_connectivity()
    print('Conectividad verificada: OK')
    conn.close()
    sys.exit(0)
except Exception as exc:
    print('Error al verificar conectividad:', exc)
    sys.exit(1)
