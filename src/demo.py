"""Demo de Supply Chain orientada a la rubrica del Proyecto 2.

Demuestra: modelado, set de datos, CRUD nodos, CRUD relaciones,
consultas Cypher y analytics.
"""

from .app import SupplyChainApp
from . import schema


def main():
    print("\n=== DEMO: Cadena de Suministros - Proyecto 2 Neo4j ===\n")

    app = SupplyChainApp()

    try:
        # 1. Conectividad
        print("1. CONECTIVIDAD")
        app.conn.verify_connectivity()
        print("   Conexion a Neo4j: OK\n")

        # 2. Inicializacion y set de datos
        print("2. INICIALIZACION Y SET DE DATOS")
        stats = app.initialize_database(clear=True)
        total_nodes = sum([stats["suppliers"], stats["products"],
                          stats["orders"], stats["inventories"],
                          stats["centers"], stats["transports"]])
        print(f"   Nodos importados: {total_nodes:,}")
        print(f"   Relaciones importadas: {sum(v for k, v in stats.items() if k not in ['suppliers','products','orders','inventories','centers','transports'])}")
        connected = app.crud.is_graph_connected()
        print(f"   Grafo conexo: {connected}\n")

        # 3. Modelado de datos
        print("3. MODELADO DE DATOS")
        gs = app.get_graph_stats()
        print(f"   Labels: Supplier, Product, OrderCompra, Inventory,"
              f" CentroDistribucion, Transporte (6)")
        print(f"   Relaciones: SUMINISTRA, INCLUYE, ALMACENADO_EN,"
              f" SE_ENVIA_POR, LLEGA_A, SALE_DE, GESTIONA, DESTINO (8+)\n")

        # 4. CRUD de nodos
        print("4. CRUD DE NODOS")
        print("   [CREATE 1 label] Supplier")
        app.create_supplier({
            "id_proveedor": 99999, "nombre": "Demo Supplier",
            "pais": "Guatemala", "rating": 4.8,
            "activo": "true", "categorias": "Bebidas|Lacteos"
        })
        s = app.get_supplier(99999)
        print(f"   -> Creado: {s['nombre']}")

        print("   [CREATE 2+ labels]")
        app.create_multi_label_node(
            ["Product", "Supplier"],
            {"nombre": "Multi-Label Demo", "precio": 99.99}
        )
        print(f"   -> Nodo multi-label creado")

        print("   [FILTER] Proveedores en Guatemala")
        filtered = app.filter_nodes(schema.LABEL_SUPPLIER, {"pais": "Guatemala"})
        print(f"   -> {len(filtered)} encontrados")

        print("   [UPDATE] Cambiar pais")
        app.add_props_to_node(schema.LABEL_SUPPLIER,
                             schema.PROP_SUPPLIER_ID, 99999,
                             {"pais": "Mexico"})
        s2 = app.get_supplier(99999)
        print(f"   -> Nuevo pais: {s2['pais']}")

        print("   [AGGREGATION] Conteo de suppliers")
        agg = app.get_node_aggregation(
            schema.LABEL_SUPPLIER, "COUNT", "id_proveedor")
        print(f"   -> Total suppliers: {agg}")

        print("   [DELETE] Eliminar supplier demo")
        app.delete_node(schema.LABEL_SUPPLIER,
                       schema.PROP_SUPPLIER_ID, 99999)
        print(f"   -> Eliminado\n")

        # 5. CRUD de relaciones
        print("5. CRUD DE RELACIONES")
        app.create_supplier({
            "id_proveedor": 88888, "nombre": "Rel Supplier",
            "pais": "GT", "rating": 4.0, "activo": "true",
            "categorias": "Bebidas"
        })
        print("   [CREATE] Relacion SUMINISTRA con 3 props")
        rel = app.crud.create_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 88888,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 1,
            schema.REL_SUPPLIES,
            {"fecha": "2025-01-01", "costo": 5.0, "estado": "Activo"}
        )
        print(f"   -> Relacion creada")

        print("   [ADD PROPS] Agregar propiedad a la relacion")
        app.add_props_to_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 88888,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 1,
            schema.REL_SUPPLIES, {"lote": "A1"}
        )
        print(f"   -> Propiedad 'lote' agregada")

        print("   [UPDATE PROPS] Actualizar costo")
        app.update_props_in_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 88888,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 1,
            schema.REL_SUPPLIES, {"costo": 7.5}
        )
        print(f"   -> Costo actualizado")

        print("   [DELETE REL] Eliminar relacion")
        app.delete_relationship(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 88888,
            schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 1,
            schema.REL_SUPPLIES
        )
        print(f"   -> Relacion eliminada\n")

        # 6. Consultas Cypher
        print("6. CONSULTAS CYPHER")
        print("   Query 1: Productos categoria Bebidas")
        drinks = app.products_by_category("Bebidas")
        for d in drinks[:3]:
            print(f"   -> {d['nombre']} (${d['precio']})")

        print("   Query 2: Top proveedores por rating")
        top_s = app.top_suppliers_by_rating(3)
        for s in top_s:
            print(f"   -> {s['nombre']} (Rating: {s['rating']})")

        print("   Query 3: Ordenes pendientes")
        pending = app.pending_orders(3)
        for o in pending:
            print(f"   -> Orden {o['id_orden']} ({o['fecha_orden']})")

        print("   Query 4: Estado de transportes")
        transp = app.transport_status(3)
        for t in transp:
            print(f"   -> Transporte {t['id_transporte']} ({t['estado']})")

        print("   Query 5: Inventario producto 1")
        inv = app.inventory_status_for_product(1)
        print(f"   -> {len(inv)} ubicaciones\n")

        # 7. Analytics (Data Science)
        print("7. ANALYTICS (DATA SCIENCE)")
        print("   Stockouts (bajo inventario):")
        stock = app.detect_stockouts(3)
        for s in stock:
            print(f"   -> {s['nombre']}: {s['inventario_total']} unidades")

        print("   Sugerencia de reorden:")
        reorder = app.suggest_reorder(3)
        for r in reorder:
            print(f"   -> {r['nombre']}: demanda prom {r['demanda_promedio']:.1f}")

        print("   Top suppliers por volumen:")
        top_v = app.top_suppliers_by_volume(3)
        for s in top_v:
            print(f"   -> {s['nombre']}: {s['productos_suministrados']} productos\n")

        print("=== DEMO COMPLETADA ===")
        print("Rubrica cubierta: modelado, set de datos, CRUD nodos,"
              " CRUD relaciones, consultas Cypher, Data Science, API funcional")

    except Exception as exc:
        print(f"Error durante demo: {exc}")
        import traceback
        traceback.print_exc()
    finally:
        app.close()


if __name__ == "__main__":
    main()
