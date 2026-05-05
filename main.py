#!/usr/bin/env python3
"""Entry point: api, console, demo, check, test, connected, init."""

import argparse
import subprocess
import sys


def run_init(clear: bool) -> None:
    from src.app import SupplyChainApp

    app = SupplyChainApp()
    try:
        app.initialize_database(clear=clear)
    except RuntimeError as exc:
        print(str(exc))
    finally:
        app.close()


def run_check() -> None:
    """Verificar conectividad, stats y grafo conexo."""
    from src.neo4j_conn import get_connection

    print("Verificando conexion a Neo4j...")
    conn = get_connection()
    try:
        conn.verify_connectivity()
        print("  Conectividad: OK")
    except RuntimeError as exc:
        print(f"  ERROR: {exc}")
        sys.exit(1)

    from src.app import SupplyChainApp
    app = SupplyChainApp()
    app.conn = conn
    app.crud.conn = conn
    app.importer.conn = conn

    try:
        stats = app.get_graph_stats()
        print(f"  Nodos totales:      {stats['total_nodes']:,}")
        print(f"  Relaciones totales: {stats['total_relationships']:,}")
        print(f"  Suppliers:    {stats['total_suppliers']:,}")
        print(f"  Products:     {stats['total_products']:,}")
        print(f"  Orders:       {stats['total_orders']:,}")
        print(f"  Inventories:  {stats['total_inventories']:,}")
        print(f"  Centers:      {stats['total_centers']:,}")
        print(f"  Transports:   {stats['total_transports']:,}")

        if stats['total_nodes'] > 0:
            connected = app.crud.is_graph_connected()
            status = "SI" if connected else "NO"
            print(f"  Grafo conexo:       {status}")
            if stats['total_nodes'] >= 5000 and connected:
                print(f"\n  OK: {stats['total_nodes']:,} nodos, "
                      f"{stats['total_relationships']:,} relaciones, grafo conexo")
        else:
            print("\n  Base de datos vacia. Ejecuta: python main.py --mode init")
    finally:
        app.close()


def run_connected() -> None:
    """Verificar unicamente si el grafo es conexo."""
    from src.app import SupplyChainApp

    app = SupplyChainApp()
    try:
        app.conn.verify_connectivity()
        connected = app.crud.is_graph_connected()
        if connected:
            print("SI - el grafo es conexo")
        else:
            print("NO - el grafo NO es conexo")
    except RuntimeError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
    finally:
        app.close()


def run_tests() -> None:
    """Ejecutar suite de pruebas con pytest."""
    print("Ejecutando tests...\n")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v"],
        capture_output=False,
    )
    sys.exit(result.returncode)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cadena de Suministros - Neo4j (Proyecto 2)"
    )
    parser.add_argument(
        "--mode",
        choices=["api", "console", "demo", "init", "check", "connected", "test"],
        default="console",
        help="Modo de ejecucion",
    )
    parser.add_argument("--host", default="0.0.0.0", help="API host")
    parser.add_argument("--port", type=int, default=5000, help="API port")
    parser.add_argument("--debug", action="store_true", help="Enable API debug")
    parser.add_argument(
        "--keep-data",
        action="store_true",
        help="No limpiar la BD durante init",
    )
    args = parser.parse_args()

    if args.mode == "api":
        try:
            from src import api as api_module
        except ModuleNotFoundError:
            print("Falta 'flask'. Instala dependencias: pip install -r requirements.txt")
            return
        api_module.run_api(host=args.host, port=args.port, debug=args.debug)
    elif args.mode == "console":
        from src.console import main as console_main
        console_main()
    elif args.mode == "demo":
        try:
            from src import demo as demo_module
        except Exception as exc:
            print(f"Error al importar demo: {exc}")
            return
        demo_module.main()
    elif args.mode == "check":
        run_check()
    elif args.mode == "connected":
        run_connected()
    elif args.mode == "test":
        run_tests()
    else:
        run_init(clear=not args.keep_data)


if __name__ == "__main__":
    main()
