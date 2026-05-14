"""Aplicación principal para la Cadena de Suministros.

Proporciona funciones de inicialización, importación y operaciones CRUD
mínimas para interactuar con el modelo supply-chain definido en `schema.py`.
"""

from typing import Dict, List, Any, Optional
from .neo4j_conn import get_connection
from .crud_operations import CrudOperations
from .data_generator import DataGenerator
from .importer import DataImporter
from .queries import CypherQueries
from .recommendation import AnalyticsEngine
from . import schema


class SupplyChainApp:
    """Aplicacion principal para operaciones de cadena de suministros."""

    def __init__(self):
        self.conn = get_connection()
        self.crud = CrudOperations(self.conn)
        self.importer = DataImporter(self.conn)
        self.queries = CypherQueries(self.conn)
        self.analytics = AnalyticsEngine(self.conn)

    def initialize_database(self, clear: bool = True, data_dir: str = "data") -> Dict[str, int]:
        """Generar datos de ejemplo e importarlos en Neo4j.

        Devuelve un diccionario con el conteo de nodos/relaciones importados.
        """
        self.conn.verify_connectivity()

        if clear:
            self.importer.clear_database()

        DataGenerator.generate_all(data_dir)
        self.importer.create_indexes()

        stats = {
            "suppliers": self.importer.import_suppliers(f"{data_dir}/suppliers.csv"),
            "products": self.importer.import_products(f"{data_dir}/products.csv"),
            "orders": self.importer.import_orders(f"{data_dir}/orders.csv"),
            "inventories": self.importer.import_inventories(f"{data_dir}/inventories.csv"),
            "centers": self.importer.import_centers(f"{data_dir}/centers.csv"),
            "transports": self.importer.import_transports(f"{data_dir}/transports.csv"),
            "supplies": self.importer.import_supplies(f"{data_dir}/supplies.csv"),
            "includes": self.importer.import_includes(f"{data_dir}/includes.csv"),
            "stored_in": self.importer.import_stored_in(f"{data_dir}/stored_in.csv"),
            "sent_by": self.importer.import_sent_by(f"{data_dir}/sent_by.csv"),
            "arrives": self.importer.import_arrives_departs(f"{data_dir}/arrives.csv"),
            "manages": self.importer.import_manages(f"{data_dir}/manages.csv"),
            "destination": self.importer.import_destination(f"{data_dir}/destination.csv"),
        }

        return stats

    # ==== CRUD Helpers (nodos) ====

    def create_supplier(self, supplier: Dict) -> Dict:
        return self.crud.create_node_single_label(schema.LABEL_SUPPLIER, supplier)

    def get_supplier(self, supplier_id: int) -> Optional[Dict]:
        return self.crud.get_node_by_id(schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, supplier_id)

    def list_suppliers(self, limit: int = 100) -> List[Dict]:
        return self.crud.get_all_nodes(schema.LABEL_SUPPLIER)[:limit]

    def create_product(self, product: Dict) -> Dict:
        return self.crud.create_node_single_label(schema.LABEL_PRODUCT, product)

    def get_product(self, product_id: int) -> Optional[Dict]:
        return self.crud.get_node_by_id(schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, product_id)

    def list_products(self, limit: int = 100) -> List[Dict]:
        return self.crud.get_all_nodes(schema.LABEL_PRODUCT)[:limit]

    def list_orders(self, limit: int = 100) -> List[Dict]:
        return self.crud.get_all_nodes(schema.LABEL_ORDER)[:limit]

    def list_centers(self, limit: int = 100) -> List[Dict]:
        return self.crud.get_all_nodes(schema.LABEL_DISTRIBUTION_CENTER)[:limit]

    def list_inventories(self, limit: int = 100) -> List[Dict]:
        return self.crud.get_all_nodes(schema.LABEL_INVENTORY)[:limit]

    def list_transports(self, limit: int = 100) -> List[Dict]:
        return self.crud.get_all_nodes(schema.LABEL_TRANSPORT)[:limit]

    # ==== CRUD Generico - Nodos ====

    def create_multi_label_node(self, labels: List[str], properties: Dict) -> Dict:
        return self.crud.create_node_multi_label(labels, properties)

    def filter_nodes(self, label: str, filters: Dict) -> List[Dict]:
        return self.crud.get_nodes_by_filter(label, filters)

    def add_props_to_node(self, label: str, id_prop: str,
                         id_value: str, properties: Dict) -> Dict:
        return self.crud.add_properties_to_node(label, id_prop, id_value, properties)

    def add_props_to_multiple_nodes(self, label: str, filter_prop: str,
                                    filter_values: List, properties: Dict) -> int:
        return self.crud.add_properties_to_multiple_nodes(
            label, filter_prop, filter_values, properties)

    def update_props_in_multiple_nodes(self, label: str, filter_prop: str,
                                       filter_values: List, properties: Dict) -> int:
        return self.crud.update_properties_in_multiple_nodes(
            label, filter_prop, filter_values, properties)

    def remove_props_from_node(self, label: str, id_prop: str,
                               id_value: str, property_names: List[str]) -> Dict:
        return self.crud.remove_properties_from_node(
            label, id_prop, id_value, property_names)

    def remove_props_from_multiple_nodes(self, label: str, filter_prop: str,
                                         filter_values: List,
                                         property_names: List[str]) -> int:
        return self.crud.remove_properties_from_multiple_nodes(
            label, filter_prop, filter_values, property_names)

    def delete_node(self, label: str, id_prop: str, id_value: str) -> bool:
        return self.crud.delete_node(label, id_prop, id_value)

    def delete_multiple_nodes(self, label: str, filter_prop: str,
                              filter_values: List) -> int:
        return self.crud.delete_multiple_nodes(label, filter_prop, filter_values)

    def get_node_aggregation(self, label: str, agg_func: str, prop: str):
        return self.crud.get_node_aggregation(label, agg_func, prop)

    # ==== CRUD Generico - Relaciones ====

    def add_props_to_relationship(self, from_label: str, from_id_prop: str,
                                  from_id: str, to_label: str, to_id_prop: str,
                                  to_id: str, rel_type: str,
                                  properties: Dict) -> Dict:
        return self.crud.add_properties_to_relationship(
            from_label, from_id_prop, from_id,
            to_label, to_id_prop, to_id, rel_type, properties)

    def add_props_to_multiple_relationships(self, rel_type: str,
                                            filter_label: str, filter_prop: str,
                                            filter_values: List,
                                            properties: Dict) -> int:
        return self.crud.add_properties_to_multiple_relationships(
            rel_type, filter_label, filter_prop, filter_values, properties)

    def update_props_in_relationship(self, from_label: str, from_id_prop: str,
                                     from_id: str, to_label: str,
                                     to_id_prop: str, to_id: str,
                                     rel_type: str, properties: Dict) -> Dict:
        return self.crud.update_relationship_properties(
            from_label, from_id_prop, from_id,
            to_label, to_id_prop, to_id, rel_type, properties)

    def remove_props_from_relationship(self, from_label: str, from_id_prop: str,
                                       from_id: str, to_label: str,
                                       to_id_prop: str, to_id: str,
                                       rel_type: str,
                                       property_names: List[str]) -> Dict:
        return self.crud.remove_properties_from_relationship(
            from_label, from_id_prop, from_id,
            to_label, to_id_prop, to_id, rel_type, property_names)

    def remove_props_from_multiple_relationships(self, rel_type: str,
                                                  filter_label: str,
                                                  filter_prop: str,
                                                  filter_values: List,
                                                  property_names: List[str]) -> int:
        return self.crud.remove_properties_from_multiple_relationships(
            rel_type, filter_label, filter_prop, filter_values, property_names)

    def delete_relationship(self, from_label: str, from_id_prop: str,
                           from_id: str, to_label: str, to_id_prop: str,
                           to_id: str, rel_type: str) -> bool:
        return self.crud.delete_relationship(
            from_label, from_id_prop, from_id,
            to_label, to_id_prop, to_id, rel_type)

    def delete_multiple_relationships(self, rel_type: str, filter_label: str,
                                      filter_prop: str,
                                      filter_values: List) -> int:
        return self.crud.delete_multiple_relationships(
            rel_type, filter_label, filter_prop, filter_values)

    def get_graph_stats(self) -> Dict[str, Any]:
        return {
            "total_suppliers": self.crud.count_nodes(schema.LABEL_SUPPLIER),
            "total_products": self.crud.count_nodes(schema.LABEL_PRODUCT),
            "total_orders": self.crud.count_nodes(schema.LABEL_ORDER),
            "total_inventories": self.crud.count_nodes(schema.LABEL_INVENTORY),
            "total_centers": self.crud.count_nodes(schema.LABEL_DISTRIBUTION_CENTER),
            "total_transports": self.crud.count_nodes(schema.LABEL_TRANSPORT),
            "total_nodes": self.crud.count_all_nodes(),
            "total_relationships": self.crud.count_relationships(),
        }

    # ==== Queries y Analytics ====

    def products_by_category(self, category: str) -> List[Dict]:
        return self.queries.products_by_category(category)

    def top_suppliers_by_rating(self, limit: int = 10) -> List[Dict]:
        return self.queries.top_suppliers_by_rating(limit)

    def pending_orders(self, limit: int = 50) -> List[Dict]:
        return self.queries.pending_orders(limit)

    def transport_status(self, limit: int = 50) -> List[Dict]:
        return self.queries.transport_status(limit)

    def inventory_status_for_product(self, product_id: int) -> List[Dict]:
        return self.queries.inventory_status_for_product(product_id)

    def detect_stockouts(self, limit: int = 10) -> List[Dict]:
        return self.analytics.detect_stockouts(limit)

    def suggest_reorder(self, limit: int = 10) -> List[Dict]:
        return self.analytics.suggest_reorder(limit)

    def top_suppliers_by_volume(self, limit: int = 10) -> List[Dict]:
        return self.analytics.top_suppliers(limit)

    def transport_overview(self, limit: int = 10) -> List[Dict]:
        return self.analytics.transport_overview(limit)

    def close(self):
        self.conn.close()


def main():
    print("Aplicación Cadena de Suministros - Neo4j\n")
    app = SupplyChainApp()
    try:
        print("Inicializando base de datos de ejemplo (esto puede tardar)...")
        stats = app.initialize_database(clear=True)
        print("Importación completada. Estadísticas:")
        for k, v in stats.items():
            print(f"  {k}: {v}")

        print("\nEstadísticas del grafo:")
        gstats = app.get_graph_stats()
        for k, v in gstats.items():
            print(f"  {k}: {v}")

    except RuntimeError as exc:
        print(str(exc))
    finally:
        app.close()


if __name__ == "__main__":
    main()
