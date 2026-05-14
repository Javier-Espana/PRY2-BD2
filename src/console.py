"""Consola interactiva para el Sistema de Cadena de Suministros.

Menu navegable que permite probar todas las funcionalidades
sin tocar codigo ni linea de comandos.
"""

import os
import sys
from .app import SupplyChainApp
from . import schema


class SupplyChainConsole:
    """Consola interactiva con menus para validar la rubrica."""

    def __init__(self):
        self.app = SupplyChainApp()
        self.initialized = False

    def _clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def _header(self, title: str):
        self._clear()
        print("=" * 62)
        print(f"  CADENA DE SUMINISTROS - Neo4j  |  {title}")
        print("=" * 62)

    def _press_enter(self):
        input("\n  Presiona ENTER para continuar...")

    def _input_int(self, prompt: str, default: int = 5) -> int:
        try:
            val = input(f"  {prompt} [{default}]: ").strip()
            return int(val) if val else default
        except ValueError:
            return default

    def _input_str(self, prompt: str, default: str = "") -> str:
        val = input(f"  {prompt}" + (f" [{default}]" if default else "") + ": ").strip()
        return val if val else default

    # ==================== MENUS PRINCIPALES ====================

    def menu_principal(self):
        while True:
            self._header("MENU PRINCIPAL")
            status = "Base de datos INICIALIZADA" if self.initialized else "Base de datos NO inicializada"
            print(f"\n  Estado: {status}")
            print(f"\n  1. Inicializar base de datos (generar + importar datos)")
            print(f"  2. Ver estadisticas del grafo")
            print(f"  3. CRUD de Nodos")
            print(f"  4. CRUD de Relaciones")
            print(f"  5. Consultas Cypher")
            print(f"  6. Analytics (Data Science)")
            print(f"  7. Ejecutar demo completa automatizada")
            print(f"  8. Verificar grafo conexo")
            print(f"  0. Salir")

            op = input("\n  Opcion: ").strip()

            if op == "1":
                self.menu_init()
            elif op == "2":
                self.menu_stats()
            elif op == "3":
                self.menu_crud_nodos()
            elif op == "4":
                self.menu_crud_relaciones()
            elif op == "5":
                self.menu_queries()
            elif op == "6":
                self.menu_analytics()
            elif op == "7":
                self.ejecutar_demo_completa()
            elif op == "8":
                self.menu_conectividad()
            elif op == "0":
                print("\n  Cerrando conexion...")
                self.app.close()
                print("  Hasta luego.\n")
                sys.exit(0)
            else:
                print("  Opcion invalida.")
                self._press_enter()

    # ==================== SUBMENUS ====================

    def menu_init(self):
        self._header("INICIALIZAR BASE DE DATOS")
        print("\n  Esto generara +5,400 nodos y +70,000 relaciones.")
        print("  Puede tardar entre 10-30 segundos.")
        confirm = input("\n  Continuar? (s/n): ").strip().lower()
        if confirm != "s":
            return

        print("\n  Generando datos...")
        try:
            stats = self.app.initialize_database(clear=True)
            self.initialized = True
            total_nodes = sum([
                stats["suppliers"], stats["products"], stats["orders"],
                stats["inventories"], stats["centers"], stats["transports"]
            ])
            print(f"\n  Base de datos inicializada!")
            print(f"    Nodos: {total_nodes:,}")
            print(f"    Relaciones importadas: {sum(v for k, v in stats.items() if k not in ['suppliers','products','orders','inventories','centers','transports'])}")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def menu_stats(self):
        self._header("ESTADISTICAS DEL GRAFO")
        if not self.initialized:
            print("\n  La base de datos no esta inicializada.")
            print("  Usa la opcion 1 del menu principal primero.")
            self._press_enter()
            return

        try:
            stats = self.app.get_graph_stats()
            print(f"\n  Suppliers:   {stats['total_suppliers']:,}")
            print(f"  Products:    {stats['total_products']:,}")
            print(f"  Orders:      {stats['total_orders']:,}")
            print(f"  Inventories: {stats['total_inventories']:,}")
            print(f"  Centers:     {stats['total_centers']:,}")
            print(f"  Transports:  {stats['total_transports']:,}")
            print(f"  -------------------------------")
            print(f"  TOTAL NODOS:      {stats['total_nodes']:,}")
            print(f"  TOTAL RELACIONES: {stats['total_relationships']:,}")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def menu_conectividad(self):
        self._header("VERIFICAR GRAFO CONEXO")
        if not self.initialized:
            print("\n  Base de datos no inicializada.")
            self._press_enter()
            return
        try:
            connected = self.app.crud.is_graph_connected()
            print(f"\n  Grafo conexo: {connected}")
            if connected:
                print("  Todos los nodos son alcanzables desde cualquier punto.")
            else:
                print("  ATENCION: Hay nodos aislados.")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def menu_crud_nodos(self):
        while True:
            self._header("CRUD DE NODOS")
            print(f"\n  1. Crear nodo (1 label)")
            print(f"  2. Crear nodo (2+ labels)")
            print(f"  3. Consultar 1 nodo")
            print(f"  4. Listar nodos")
            print(f"  5. Filtrar nodos")
            print(f"  6. Agregar propiedades a nodo")
            print(f"  7. Actualizar propiedades de nodo")
            print(f"  8. Eliminar propiedades de nodo")
            print(f"  9. Eliminar nodo")
            print(f"  10. Eliminar multiples nodos")
            print(f"  11. Agregacion (COUNT/AVG/SUM)")
            print(f"  0. Volver")

            op = input("\n  Opcion: ").strip()

            if op == "1":
                self._crud_create_single_label()
            elif op == "2":
                self._crud_create_multi_label()
            elif op == "3":
                self._crud_get_node()
            elif op == "4":
                self._crud_list_nodes()
            elif op == "5":
                self._crud_filter_nodes()
            elif op == "6":
                self._crud_add_props()
            elif op == "7":
                self._crud_update_props()
            elif op == "8":
                self._crud_remove_props()
            elif op == "9":
                self._crud_delete_node()
            elif op == "10":
                self._crud_delete_multiple_nodes()
            elif op == "11":
                self._crud_aggregation()
            elif op == "0":
                return

    def menu_crud_relaciones(self):
        while True:
            self._header("CRUD DE RELACIONES")
            print(f"\n  1. Crear relacion (con 3+ propiedades)")
            print(f"  2. Agregar propiedades a relacion")
            print(f"  3. Actualizar propiedades de relacion")
            print(f"  4. Eliminar propiedades de relacion")
            print(f"  5. Eliminar una relacion")
            print(f"  6. Eliminar multiples relaciones")
            print(f"  0. Volver")

            op = input("\n  Opcion: ").strip()

            if op == "1":
                self._rel_create()
            elif op == "2":
                self._rel_add_props()
            elif op == "3":
                self._rel_update_props()
            elif op == "4":
                self._rel_remove_props()
            elif op == "5":
                self._rel_delete()
            elif op == "6":
                self._rel_delete_multiple()
            elif op == "0":
                return

    def menu_queries(self):
        while True:
            self._header("CONSULTAS CYPHER")
            print(f"\n  1. Productos por categoria")
            print(f"  2. Estado de inventario por producto")
            print(f"  3. Top proveedores por rating")
            print(f"  4. Ordenes pendientes")
            print(f"  5. Estado de transportes")
            print(f"  6. Inventario de un producto especifico")
            print(f"  0. Volver")

            op = input("\n  Opcion: ").strip()

            if op == "1":
                self._query_products_by_category()
            elif op == "2":
                self._query_inventory()
            elif op == "3":
                self._query_top_suppliers()
            elif op == "4":
                self._query_pending_orders()
            elif op == "5":
                self._query_transport()
            elif op == "6":
                self._query_product_inventory()
            elif op == "0":
                return

    def menu_analytics(self):
        while True:
            self._header("ANALYTICS (DATA SCIENCE)")
            print(f"\n  1. Detectar stockouts (bajo inventario)")
            print(f"  2. Sugerir reorden (demanda historica)")
            print(f"  3. Top proveedores por volumen")
            print(f"  4. Resumen de transportes")
            print(f"  0. Volver")

            op = input("\n  Opcion: ").strip()

            if op == "1":
                self._analytics_stockouts()
            elif op == "2":
                self._analytics_reorder()
            elif op == "3":
                self._analytics_top_suppliers()
            elif op == "4":
                self._analytics_transport()
            elif op == "0":
                return

    # ==================== OPERACIONES CRUD NODOS ====================

    def _crud_create_single_label(self):
        self._header("CREAR NODO (1 LABEL)")
        label = input("\n  Label (Supplier/Product/OrderCompra/Inventory/CentroDistribucion/Transporte): ").strip()
        nombre = input("  Nombre: ").strip()
        try:
            node_id = 90000 + hash(nombre) % 10000
            if label == "Supplier":
                result = self.app.create_supplier({
                    "id_proveedor": node_id, "nombre": nombre,
                    "pais": "Guatemala", "rating": 4.0,
                    "activo": "true", "categorias": "General"
                })
            elif label == "Product":
                result = self.app.create_product({
                    "id_producto": node_id, "nombre": nombre,
                    "categoria": "General", "precio": 10.0,
                    "perecedero": "false", "fecha_expiracion": ""
                })
            else:
                result = self.app.crud.create_node_single_label(
                    label, {"nombre": nombre})
            print(f"\n  Nodo creado exitosamente.")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _crud_create_multi_label(self):
        self._header("CREAR NODO (2+ LABELS)")
        labels = input("\n  Labels separados por coma (ej: Product,Supplier): ").strip()
        nombre = input("  Nombre: ").strip()
        try:
            labels_list = [l.strip() for l in labels.split(",")]
            result = self.app.create_multi_label_node(
                labels_list, {"nombre": nombre})
            print(f"\n  Nodo multi-label creado: {result}")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _crud_get_node(self):
        self._header("CONSULTAR 1 NODO")
        label = input("\n  Label: ").strip()
        id_prop = input("  Propiedad ID (ej: id_proveedor, id_producto): ").strip()
        id_val = input("  Valor ID: ").strip()
        try:
            result = self.app.crud.get_node_by_id(label, id_prop, id_val)
            if result:
                print(f"\n  Nodo encontrado:")
                for k, v in result.items():
                    print(f"    {k}: {v}")
            else:
                print("\n  Nodo no encontrado.")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _crud_list_nodes(self):
        self._header("LISTAR NODOS")
        label = input("\n  Label: ").strip()
        limit = self._input_int("Cantidad a mostrar", 5)
        try:
            nodes = self.app.crud.get_all_nodes(label)[:limit]
            if nodes:
                for i, n in enumerate(nodes, 1):
                    nombre = n.get('nombre', n.get('id_proveedor', n.get('id_producto', n.get('id_orden', 'N/A'))))
                    print(f"  {i}. {nombre}")
            else:
                print("  No se encontraron nodos.")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _crud_filter_nodes(self):
        self._header("FILTRAR NODOS")
        label = input("\n  Label: ").strip()
        prop = input("  Propiedad a filtrar (ej: pais, categoria): ").strip()
        value = input("  Valor: ").strip()
        try:
            results = self.app.filter_nodes(label, {prop: value})
            print(f"\n  Resultados: {len(results)}")
            for n in results[:5]:
                nombre = n.get('nombre', str(n.get(list(n.keys())[0], 'N/A')))
                print(f"    - {nombre}")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _crud_add_props(self):
        self._header("AGREGAR PROPIEDADES A NODO")
        label = input("\n  Label: ").strip()
        id_prop = input("  Propiedad ID: ").strip()
        id_val = input("  Valor ID: ").strip()
        prop_name = input("  Nombre de nueva propiedad: ").strip()
        prop_val = input("  Valor: ").strip()
        try:
            result = self.app.add_props_to_node(
                label, id_prop, id_val, {prop_name: prop_val})
            print(f"\n  Propiedad '{prop_name}' agregada.")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _crud_update_props(self):
        self._header("ACTUALIZAR PROPIEDADES DE NODO")
        label = input("\n  Label: ").strip()
        id_prop = input("  Propiedad ID: ").strip()
        id_val = input("  Valor ID: ").strip()
        prop_name = input("  Nombre de propiedad a actualizar: ").strip()
        prop_val = input("  Nuevo valor: ").strip()
        try:
            result = self.app.add_props_to_node(
                label, id_prop, id_val, {prop_name: prop_val})
            print(f"\n  Propiedad '{prop_name}' actualizada.")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _crud_remove_props(self):
        self._header("ELIMINAR PROPIEDADES DE NODO")
        label = input("\n  Label: ").strip()
        id_prop = input("  Propiedad ID: ").strip()
        id_val = input("  Valor ID: ").strip()
        props = input("  Propiedades a eliminar (separadas por coma): ").strip()
        try:
            prop_list = [p.strip() for p in props.split(",")]
            result = self.app.remove_props_from_node(
                label, id_prop, id_val, prop_list)
            print(f"\n  Propiedades eliminadas: {props}")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _crud_delete_node(self):
        self._header("ELIMINAR NODO")
        label = input("\n  Label: ").strip()
        id_prop = input("  Propiedad ID: ").strip()
        id_val = input("  Valor ID: ").strip()
        confirm = input(f"\n  Seguro que quieres eliminar {label} {id_val}? (s/n): ").strip().lower()
        if confirm != "s":
            return
        try:
            deleted = self.app.delete_node(label, id_prop, id_val)
            print(f"\n  Nodo eliminado: {deleted}")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _crud_delete_multiple_nodes(self):
        self._header("ELIMINAR MULTIPLES NODOS")
        label = input("\n  Label: ").strip()
        prop = input("  Propiedad para filtrar: ").strip()
        values = input("  Valores (separados por coma): ").strip()
        val_list = [v.strip() for v in values.split(",")]
        confirm = input(f"\n  Eliminar {label} donde {prop} IN {val_list}? (s/n): ").strip().lower()
        if confirm != "s":
            return
        try:
            deleted = self.app.delete_multiple_nodes(label, prop, val_list)
            print(f"\n  Nodos eliminados: {deleted}")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _crud_aggregation(self):
        self._header("AGREGACION SOBRE NODOS")
        label = input("\n  Label: ").strip()
        func = input("  Funcion (COUNT/AVG/SUM/MAX/MIN): ").strip()
        prop = input("  Propiedad: ").strip()
        try:
            result = self.app.get_node_aggregation(label, func, prop)
            print(f"\n  {func}({label}.{prop}) = {result}")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    # ==================== OPERACIONES CRUD RELACIONES ====================

    def _rel_create(self):
        self._header("CREAR RELACION CON PROPIEDADES")
        print("\n  Ejemplo: Supplier -> SUMINISTRA -> Product")
        from_label = input("  Label origen (ej: Supplier): ").strip()
        from_id_prop = input("  Propiedad ID origen (ej: id_proveedor): ").strip()
        from_id = input("  Valor ID origen: ").strip()
        to_label = input("  Label destino (ej: Product): ").strip()
        to_id_prop = input("  Propiedad ID destino (ej: id_producto): ").strip()
        to_id = input("  Valor ID destino: ").strip()
        rel_type = input("  Tipo de relacion (ej: SUMINISTRA): ").strip()
        print("\n  Propiedades de la relacion (minimo 3):")
        props = {}
        for i in range(3):
            k = input(f"    Propiedad {i+1} nombre: ").strip()
            v = input(f"    Propiedad {i+1} valor: ").strip()
            if k:
                props[k] = v
        try:
            result = self.app.crud.create_relationship(
                from_label, from_id_prop, from_id,
                to_label, to_id_prop, to_id, rel_type, props)
            print(f"\n  Relacion creada exitosamente.")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _rel_add_props(self):
        self._header("AGREGAR PROPIEDADES A RELACION")
        fl = input("\n  Label origen: ").strip()
        fi = input("  Propiedad ID origen: ").strip()
        fv = input("  Valor ID origen: ").strip()
        tl = input("  Label destino: ").strip()
        ti = input("  Propiedad ID destino: ").strip()
        tv = input("  Valor ID destino: ").strip()
        rt = input("  Tipo de relacion: ").strip()
        k = input("  Propiedad a agregar: ").strip()
        v = input("  Valor: ").strip()
        try:
            result = self.app.add_props_to_relationship(
                fl, fi, fv, tl, ti, tv, rt, {k: v})
            print(f"\n  Propiedad '{k}' agregada.")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _rel_update_props(self):
        self._header("ACTUALIZAR PROPIEDADES DE RELACION")
        fl = input("\n  Label origen: ").strip()
        fi = input("  Propiedad ID origen: ").strip()
        fv = input("  Valor ID origen: ").strip()
        tl = input("  Label destino: ").strip()
        ti = input("  Propiedad ID destino: ").strip()
        tv = input("  Valor ID destino: ").strip()
        rt = input("  Tipo de relacion: ").strip()
        k = input("  Propiedad a actualizar: ").strip()
        v = input("  Nuevo valor: ").strip()
        try:
            result = self.app.update_props_in_relationship(
                fl, fi, fv, tl, ti, tv, rt, {k: v})
            print(f"\n  Propiedad '{k}' actualizada.")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _rel_remove_props(self):
        self._header("ELIMINAR PROPIEDADES DE RELACION")
        fl = input("\n  Label origen: ").strip()
        fi = input("  Propiedad ID origen: ").strip()
        fv = input("  Valor ID origen: ").strip()
        tl = input("  Label destino: ").strip()
        ti = input("  Propiedad ID destino: ").strip()
        tv = input("  Valor ID destino: ").strip()
        rt = input("  Tipo de relacion: ").strip()
        props = input("  Propiedades a eliminar (separadas por coma): ").strip()
        try:
            plist = [p.strip() for p in props.split(",")]
            result = self.app.remove_props_from_relationship(
                fl, fi, fv, tl, ti, tv, rt, plist)
            print(f"\n  Propiedades eliminadas.")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _rel_delete(self):
        self._header("ELIMINAR RELACION")
        fl = input("\n  Label origen: ").strip()
        fi = input("  Propiedad ID origen: ").strip()
        fv = input("  Valor ID origen: ").strip()
        tl = input("  Label destino: ").strip()
        ti = input("  Propiedad ID destino: ").strip()
        tv = input("  Valor ID destino: ").strip()
        rt = input("  Tipo de relacion: ").strip()
        confirm = input(f"\n  Eliminar {rt}? (s/n): ").strip().lower()
        if confirm != "s":
            return
        try:
            deleted = self.app.delete_relationship(
                fl, fi, fv, tl, ti, tv, rt)
            print(f"\n  Relacion eliminada: {deleted}")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _rel_delete_multiple(self):
        self._header("ELIMINAR MULTIPLES RELACIONES")
        rt = input("\n  Tipo de relacion: ").strip()
        fl = input("  Label origen (para filtrar): ").strip()
        fp = input("  Propiedad para filtrar: ").strip()
        vals = input("  Valores (separados por coma): ").strip()
        vlist = [v.strip() for v in vals.split(",")]
        try:
            deleted = self.app.delete_multiple_relationships(
                rt, fl, fp, vlist)
            print(f"\n  Relaciones eliminadas: {deleted}")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    # ==================== CONSULTAS ====================

    def _query_products_by_category(self):
        self._header("PRODUCTOS POR CATEGORIA")
        cat = input("\n  Categoria (ej: Bebidas, Lacteos): ").strip()
        try:
            results = self.app.products_by_category(cat)
            print(f"\n  Productos en '{cat}': {len(results)}")
            for r in results[:10]:
                print(f"    {r['nombre']} - ${r['precio']}")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _query_inventory(self):
        self._header("ESTADO DE INVENTARIO POR PRODUCTO")
        pid = self._input_int("ID del producto", 1)
        try:
            results = self.app.inventory_status_for_product(pid)
            print(f"\n  Ubicaciones de inventario: {len(results)}")
            for r in results[:5]:
                print(f"    {r['ubicacion']}: {r['cantidad']} unidades (max {r['capacidad_max']})")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _query_top_suppliers(self):
        self._header("TOP PROVEEDORES POR RATING")
        lim = self._input_int("Cuantos mostrar", 5)
        try:
            results = self.app.top_suppliers_by_rating(lim)
            for i, r in enumerate(results, 1):
                print(f"  {i}. {r['nombre']} - {r['pais']} - Rating: {r['rating']}")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _query_pending_orders(self):
        self._header("ORDENES PENDIENTES")
        lim = self._input_int("Cuantas mostrar", 5)
        try:
            results = self.app.pending_orders(lim)
            print(f"\n  Ordenes pendientes: {len(results)}")
            for r in results:
                print(f"    Orden {r['id_orden']} - {r['fecha_orden']} - Urgente: {r['urgente']}")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _query_transport(self):
        self._header("ESTADO DE TRANSPORTES")
        lim = self._input_int("Cuantos mostrar", 5)
        try:
            results = self.app.transport_status(lim)
            for r in results:
                print(f"    Transporte {r['id_transporte']} - {r['tipo']} - {r['estado']}")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _query_product_inventory(self):
        self._header("INVENTARIO DE PRODUCTO")
        pid = self._input_int("ID del producto", 1)
        try:
            results = self.app.inventory_status_for_product(pid)
            print(f"\n  {len(results)} ubicaciones encontradas.")
            for r in results:  # type: ignore[assignment]
                print(f"    Inventario {r['id_inventario']}: {r['cantidad']} en {r['ubicacion']}")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    # ==================== ANALYTICS ====================

    def _analytics_stockouts(self):
        self._header("DETECTAR STOCKOUTS")
        lim = self._input_int("Cuantos mostrar", 5)
        try:
            results = self.app.detect_stockouts(lim)
            print(f"\n  Productos con menor inventario:")
            for r in results:
                print(f"    {r['nombre']}: {r['inventario_total']} unidades")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _analytics_reorder(self):
        self._header("SUGERIR REORDEN")
        lim = self._input_int("Cuantos mostrar", 5)
        try:
            results = self.app.suggest_reorder(lim)
            print(f"\n  Productos a reordenar:")
            for r in results:
                print(f"    {r['nombre']}: demanda promedio {r['demanda_promedio']:.1f}")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _analytics_top_suppliers(self):
        self._header("TOP PROVEEDORES POR VOLUMEN")
        lim = self._input_int("Cuantos mostrar", 5)
        try:
            results = self.app.top_suppliers_by_volume(lim)
            for i, r in enumerate(results, 1):
                print(f"  {i}. {r['nombre']}: {r['productos_suministrados']} productos")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    def _analytics_transport(self):
        self._header("RESUMEN DE TRANSPORTES")
        lim = self._input_int("Cuantos mostrar", 5)
        try:
            results = self.app.transport_overview(lim)
            for r in results:
                print(f"    {r['id_transporte']} - {r['tipo']} - {r['estado']}")
        except Exception as e:
            print(f"\n  Error: {e}")
        self._press_enter()

    # ==================== DEMO AUTOMATICA ====================

    def ejecutar_demo_completa(self):
        self._header("DEMO COMPLETA AUTOMATICA")
        print("\n  Ejecutando todas las funcionalidades...\n")

        if not self.initialized:
            print("  [1/8] Inicializando base de datos...")
            try:
                self.app.initialize_database(clear=True)
                self.initialized = True
                print("  -> OK")
            except Exception as e:
                print(f"  -> ERROR: {e}")
                self._press_enter()
                return
        else:
            print("  [1/8] Base de datos ya inicializada")

        try:
            print("  [2/8] Verificando grafo conexo...")
            c = self.app.crud.is_graph_connected()
            print(f"  -> {'SI' if c else 'NO'}")

            print("  [3/8] CRUD de nodos...")
            self.app.create_supplier({
                "id_proveedor": 77777, "nombre": "Demo Console",
                "pais": "GT", "rating": 5.0, "activo": "true",
                "categorias": "Bebidas"
            })
            s = self.app.get_supplier(77777)
            print(f"  -> Nodo creado y leido: {s['nombre']}")
            multi = self.app.create_multi_label_node(
                ["Product", "Supplier"], {"nombre": "Multi Demo"})
            print(f"  -> Nodo multi-label creado")
            self.app.add_props_to_node(schema.LABEL_SUPPLIER,
                                      schema.PROP_SUPPLIER_ID, 77777,
                                      {"temp": "valor"})
            self.app.remove_props_from_node(schema.LABEL_SUPPLIER,
                                           schema.PROP_SUPPLIER_ID, 77777,
                                           ["temp"])
            print(f"  -> Propiedades agregadas y eliminadas")
            self.app.delete_node(schema.LABEL_SUPPLIER,
                                schema.PROP_SUPPLIER_ID, 77777)
            print(f"  -> Nodo eliminado")

            print("  [4/8] CRUD de relaciones...")
            rel = self.app.crud.create_relationship(
                schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 1,
                schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 1,
                schema.REL_SUPPLIES,
                {"fecha": "2025-01-01", "costo": 5.0, "estado": "Activo"})
            self.app.add_props_to_relationship(
                schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 1,
                schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 1,
                schema.REL_SUPPLIES, {"demo": "ok"})
            self.app.remove_props_from_relationship(
                schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 1,
                schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 1,
                schema.REL_SUPPLIES, ["demo"])
            self.app.delete_relationship(
                schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 1,
                schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, 1,
                schema.REL_SUPPLIES)
            print(f"  -> Relacion: crear -> modificar -> eliminar OK")

            print("  [5/8] Consultas Cypher...")
            q1 = len(self.app.products_by_category("Bebidas"))
            q2 = len(self.app.top_suppliers_by_rating(3))
            q3 = len(self.app.pending_orders(5))
            q4 = len(self.app.transport_status(5))
            print(f"  -> {q1} productos en Bebidas, {q2} top suppliers, "
                  f"{q3} pendientes, {q4} transportes")

            print("  [6/8] Analytics...")
            a1 = len(self.app.detect_stockouts(3))
            a2 = len(self.app.suggest_reorder(3))
            print(f"  -> {a1} stockouts, {a2} sugerencias reorden")

            print("  [7/8] Agregaciones...")
            agg = self.app.get_node_aggregation(
                schema.LABEL_SUPPLIER, "COUNT", "id_proveedor")
            print(f"  -> Total suppliers: {agg}")

            print("  [8/8] Estadisticas finales...")
            stats = self.app.get_graph_stats()
            print(f"  -> Nodos: {stats['total_nodes']:,}")
            print(f"  -> Relaciones: {stats['total_relationships']:,}")

            print(f"\n  DEMO COMPLETADA EXITOSAMENTE")
            print(f"  Todos los criterios de la rubrica fueron ejecutados.")

        except Exception as e:
            print(f"\n  Error en demo: {e}")
            import traceback
            traceback.print_exc()

        self._press_enter()


def main():
    """Entry point de la consola interactiva."""
    console = SupplyChainConsole()
    try:
        console.menu_principal()
    except KeyboardInterrupt:
        print("\n\n  Saliendo...")
        console.app.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
