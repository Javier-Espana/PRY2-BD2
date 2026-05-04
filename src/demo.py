"""Demo de Supply Chain - Demostración interactiva del sistema.

Ejecuta consultas y operaciones CRUD básicas del sistema de cadena de suministros.
"""

from .app import SupplyChainApp
from .queries import CypherQueries


def main():
    """Ejecutar demo interactiva."""
    print("\n=== DEMO: Sistema de Cadena de Suministros ===\n")

    app = SupplyChainApp()

    try:
        # Verificar conectividad
        print("Verificando conexión a Neo4j...")
        app.conn.verify_connectivity()
        print("Conexión exitosa.\n")

        # Mostrar estadísticas
        print("Estadísticas del grafo:")
        stats = app.get_graph_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        print()

        # Listar proveedores
        print("Top 5 proveedores:")
        suppliers = app.list_suppliers(limit=5)
        for s in suppliers:
            print(f"  - {s.get('nombre', 'N/A')} (ID: {s.get('supplier_id', 'N/A')})")
        print()

        # Listar productos
        print("Top 5 productos:")
        products = app.list_products(limit=5)
        for p in products:
            print(f"  - {p.get('nombre', 'N/A')} (Categoría: {p.get('categoria', 'N/A')})")
        print()

        # Listar órdenes
        print("Top 5 órdenes:")
        orders = app.list_orders(limit=5)
        for o in orders:
            print(f"  - Orden {o.get('order_id', 'N/A')} (Estado: {o.get('estado', 'N/A')})")
        print()

        # Listar centros de distribución
        print("Centros de distribución:")
        centers = app.list_centers(limit=5)
        for c in centers:
            print(f"  - {c.get('nombre', 'N/A')} (Ciudad: {c.get('ciudad', 'N/A')})")
        print()

        print("\nDemo completada exitosamente.")

    except Exception as exc:
        print(f"Error durante demo: {exc}")
    finally:
        app.close()


if __name__ == "__main__":
    main()
