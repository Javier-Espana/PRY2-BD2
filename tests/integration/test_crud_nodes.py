"""Pruebas de CRUD completo de nodos via SupplyChainApp."""

import pytest
from src import schema


@pytest.mark.integration
class TestNodeCrudComplete:
    """Todas las operaciones CRUD de nodos exigidas por la rubrica."""

    def test_create_multi_label_node(self, app, clean_db):
        """Crear un nodo con 2+ labels."""
        node = app.create_multi_label_node(
            ["Product", "Supplier"],
            {"nombre": "Multi Label Test", "precio": 5.0}
        )
        assert node is not None

    def test_filter_nodes(self, app, clean_db, test_supplier_data):
        """Filtrar nodos por propiedad."""
        app.create_supplier(test_supplier_data)
        results = app.filter_nodes(
            schema.LABEL_SUPPLIER, {"pais": "Guatemala"}
        )
        assert len(results) >= 1

    def test_add_props_to_node(self, app, clean_db, test_supplier_data):
        """Agregar propiedades a un nodo."""
        app.create_supplier(test_supplier_data)
        result = app.add_props_to_node(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            {"contacto": "555-0001"}
        )
        assert result is not None

    def test_add_props_to_multiple_nodes(self, app, clean_db):
        """Agregar propiedades a multiples nodos."""
        app.create_supplier({
            "id_proveedor": 99901, "nombre": "S1", "pais": "XX",
            "rating": 3.0, "activo": "true", "categorias": "Bebidas"
        })
        app.create_supplier({
            "id_proveedor": 99902, "nombre": "S2", "pais": "XX",
            "rating": 4.0, "activo": "true", "categorias": "Alimentos"
        })
        updated = app.add_props_to_multiple_nodes(
            schema.LABEL_SUPPLIER, "pais", ["XX"], {"nivel": "premium"}
        )
        assert updated == 2

    def test_update_props_in_multiple_nodes(self, app, clean_db):
        """Actualizar propiedades en multiples nodos."""
        app.create_supplier({
            "id_proveedor": 99901, "nombre": "S1", "pais": "XX",
            "rating": 3.0, "activo": "true", "categorias": "Bebidas"
        })
        updated = app.update_props_in_multiple_nodes(
            schema.LABEL_SUPPLIER, "pais", ["XX"], {"pais": "Guatemala"}
        )
        assert updated == 1

    def test_remove_props_from_node(self, app, clean_db, test_supplier_data):
        """Eliminar propiedades de un nodo."""
        app.create_supplier(test_supplier_data)
        app.add_props_to_node(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            {"temporal": "borrar"}
        )
        result = app.remove_props_from_node(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            ["temporal"]
        )
        assert result is not None

    def test_remove_props_from_multiple_nodes(self, app, clean_db):
        """Eliminar propiedades de multiples nodos."""
        app.create_supplier({
            "id_proveedor": 99901, "nombre": "S1", "pais": "XX",
            "rating": 3.0, "activo": "true", "categorias": "Bebidas"
        })
        app.add_props_to_node(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901,
            {"temp": 1}
        )
        updated = app.remove_props_from_multiple_nodes(
            schema.LABEL_SUPPLIER, "pais", ["XX"], ["temp"]
        )
        assert updated >= 1

    def test_delete_node(self, app, clean_db, test_supplier_data):
        """Eliminar un nodo."""
        app.create_supplier(test_supplier_data)
        deleted = app.delete_node(
            schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, 99901
        )
        assert deleted is True
        s = app.get_supplier(99901)
        assert s is None

    def test_delete_multiple_nodes(self, app, clean_db):
        """Eliminar multiples nodos."""
        app.create_supplier({
            "id_proveedor": 99901, "nombre": "S1", "pais": "XX",
            "rating": 3.0, "activo": "true", "categorias": "Bebidas"
        })
        app.create_supplier({
            "id_proveedor": 99902, "nombre": "S2", "pais": "XX",
            "rating": 4.0, "activo": "true", "categorias": "Alimentos"
        })
        deleted = app.delete_multiple_nodes(
            schema.LABEL_SUPPLIER, "pais", ["XX"]
        )
        assert deleted == 2

    def test_get_node_aggregation(self, app, clean_db, test_supplier_data):
        """Agregacion sobre nodos."""
        app.create_supplier(test_supplier_data)
        result = app.get_node_aggregation(
            schema.LABEL_SUPPLIER, "COUNT", "id_proveedor"
        )
        assert result is not None
