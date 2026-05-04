#!/usr/bin/env python3
"""Entry point for running API, demo, or initialization.

This file now performs lazy imports so that running `--mode demo` or
`--mode init` doesn't require Flask to be installed unless `--mode api`
is used.
"""

import argparse


def run_init(clear: bool) -> None:
    from src.app import SupplyChainApp

    app = SupplyChainApp()
    try:
        app.initialize_database(clear=clear)
    except RuntimeError as exc:
        print(str(exc))
    finally:
        app.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Project entry point")
    parser.add_argument(
        "--mode",
        choices=["api", "demo", "init"],
        default="api",
        help="Execution mode",
    )
    parser.add_argument("--host", default="0.0.0.0", help="API host")
    parser.add_argument("--port", type=int, default=5000, help="API port")
    parser.add_argument("--debug", action="store_true", help="Enable API debug")
    parser.add_argument(
        "--keep-data",
        action="store_true",
        help="Do not clear the database during init",
    )
    args = parser.parse_args()

    if args.mode == "api":
        try:
            from src import api as api_module
        except ModuleNotFoundError:
            print(
                "Falta la dependencia 'flask'. Instala las dependencias con: pip install -r requirements.txt"
            )
            return
        api_module.run_api(host=args.host, port=args.port, debug=args.debug)
    elif args.mode == "demo":
        try:
            from src import demo as demo_module
        except Exception as exc:
            print(f"Error al importar el módulo demo: {exc}")
            return
        demo_module.main()
    else:
        run_init(clear=not args.keep_data)


if __name__ == "__main__":
    main()
