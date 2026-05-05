"""API Flask para la Cadena de Suministros."""

import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from .app import SupplyChainApp
from . import schema

app = Flask(__name__)
CORS(app)

sc_app = SupplyChainApp()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_PATH = os.path.join(BASE_DIR, '..', 'app', 'code.html')

# ---------- LABEL / ID PROP MAP ----------
LABEL_ID_MAP = {
    "Supplier": schema.PROP_SUPPLIER_ID,
    "Product": schema.PROP_PRODUCT_ID,
    "OrderCompra": schema.PROP_ORDER_ID,
    "Inventory": schema.PROP_INVENTORY_ID,
    "CentroDistribucion": schema.PROP_CENTER_ID,
    "Transporte": schema.PROP_TRANSPORT_ID,
}


def _id_prop_for(label):
    return LABEL_ID_MAP.get(label, "id")


# ==================== DASHBOARD ====================

@app.route('/', methods=['GET'])
def dashboard():
    return send_file(FRONTEND_PATH)


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"success": True, "message": "API is running"}), 200


@app.route('/api/init', methods=['POST'])
def initialize():
    try:
        payload = request.get_json(silent=True) or {}
        stats = sc_app.initialize_database(clear=payload.get('clear', True))
        return jsonify({"success": True, "message": "Base de datos inicializada", "stats": stats}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        stats = sc_app.get_graph_stats()
        return jsonify({"success": True, "data": stats}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== NODOS GENÉRICOS ====================

@app.route('/api/nodes', methods=['POST'])
def create_node():
    """Crear nodo con 1 o 2+ labels y propiedades."""
    try:
        data = request.get_json(silent=True) or {}
        labels = data.get('labels', [])
        properties = data.get('properties', {})
        if not labels:
            return jsonify({"success": False, "error": "Se requiere al menos 1 label"}), 400
        if len(labels) == 1:
            node = sc_app.crud.create_node_single_label(labels[0], properties)
        else:
            node = sc_app.crud.create_node_multi_label(labels, properties)
        return jsonify({"success": True, "data": dict(node) if node else {}}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>', methods=['GET'])
def list_nodes_by_label(label):
    """Listar nodos por label con filtros opcionales."""
    try:
        limit = request.args.get('limit', 100, type=int)
        filter_key = request.args.get('filter_key')
        filter_val = request.args.get('filter_val')
        if filter_key and filter_val:
            nodes = sc_app.crud.get_nodes_by_filter(label, {filter_key: filter_val})
        else:
            nodes = sc_app.crud.get_all_nodes(label)[:limit]
        return jsonify({"success": True, "data": nodes}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>/<id_value>', methods=['GET'])
def get_node(label, id_value):
    """Obtener nodo por id (?id_prop=id_proveedor)."""
    try:
        id_prop = request.args.get('id_prop', _id_prop_for(label))
        node = sc_app.crud.get_node_by_id(label, id_prop, id_value)
        if node:
            return jsonify({"success": True, "data": node}), 200
        return jsonify({"success": False, "error": "Nodo no encontrado"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>/<id_value>', methods=['PATCH'])
def update_node_props(label, id_value):
    """Agregar o actualizar propiedades en un nodo."""
    try:
        data = request.get_json(silent=True) or {}
        id_prop = data.pop('id_prop', _id_prop_for(label))
        properties = data.get('properties', data)
        node = sc_app.crud.add_properties_to_node(label, id_prop, id_value, properties)
        return jsonify({"success": True, "data": dict(node) if node else {}}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>/<id_value>', methods=['DELETE'])
def delete_node(label, id_value):
    """Eliminar un nodo por id."""
    try:
        id_prop = request.args.get('id_prop', _id_prop_for(label))
        ok = sc_app.crud.delete_node(label, id_prop, id_value)
        return jsonify({"success": ok}), 200 if ok else 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>/<id_value>/remove-properties', methods=['POST'])
def remove_node_props(label, id_value):
    """Eliminar propiedades específicas de un nodo."""
    try:
        data = request.get_json(silent=True) or {}
        id_prop = data.get('id_prop', _id_prop_for(label))
        property_names = data.get('property_names', [])
        node = sc_app.crud.remove_properties_from_node(label, id_prop, id_value, property_names)
        return jsonify({"success": True, "data": dict(node) if node else {}}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>/bulk/update', methods=['POST'])
def bulk_update_nodes(label):
    """Agregar/actualizar propiedades en múltiples nodos."""
    try:
        data = request.get_json(silent=True) or {}
        filter_prop = data.get('filter_prop')
        filter_values = data.get('filter_values', [])
        properties = data.get('properties', {})
        count = sc_app.crud.add_properties_to_multiple_nodes(
            label, filter_prop, filter_values, properties)
        return jsonify({"success": True, "updated": count}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>/bulk/delete', methods=['POST'])
def bulk_delete_nodes(label):
    """Eliminar múltiples nodos por filtro."""
    try:
        data = request.get_json(silent=True) or {}
        filter_prop = data.get('filter_prop')
        filter_values = data.get('filter_values', [])
        count = sc_app.crud.delete_multiple_nodes(label, filter_prop, filter_values)
        return jsonify({"success": True, "deleted": count}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>/bulk/remove-properties', methods=['POST'])
def bulk_remove_node_props(label):
    """Eliminar propiedades de múltiples nodos."""
    try:
        data = request.get_json(silent=True) or {}
        filter_prop = data.get('filter_prop')
        filter_values = data.get('filter_values', [])
        property_names = data.get('property_names', [])
        count = sc_app.crud.remove_properties_from_multiple_nodes(
            label, filter_prop, filter_values, property_names)
        return jsonify({"success": True, "updated": count}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>/aggregations', methods=['GET'])
def node_aggregations(label):
    """Consultas agregadas: COUNT, AVG, MAX, MIN sobre una propiedad."""
    try:
        func = request.args.get('func', 'COUNT').upper()
        prop = request.args.get('prop', 'id')
        if func not in ('COUNT', 'AVG', 'MAX', 'MIN', 'SUM'):
            return jsonify({"success": False, "error": "func inválido"}), 400
        result = sc_app.crud.get_node_aggregation(label, func, prop)
        return jsonify({"success": True, "data": {"function": func, "property": prop, "result": result}}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== SUPPLIERS ====================

@app.route('/api/suppliers', methods=['GET'])
def list_suppliers():
    try:
        limit = request.args.get('limit', 100, type=int)
        return jsonify({"success": True, "data": sc_app.list_suppliers(limit)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/suppliers', methods=['POST'])
def create_supplier():
    try:
        data = request.get_json(silent=True) or {}
        supplier = sc_app.create_supplier(data)
        return jsonify({"success": True, "data": dict(supplier) if supplier else {}}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/suppliers/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    try:
        supplier = sc_app.get_supplier(supplier_id)
        if supplier:
            return jsonify({"success": True, "data": supplier}), 200
        return jsonify({"success": False, "error": "Proveedor no encontrado"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/suppliers/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    try:
        ok = sc_app.crud.delete_node(schema.LABEL_SUPPLIER, schema.PROP_SUPPLIER_ID, supplier_id)
        return jsonify({"success": ok}), 200 if ok else 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== PRODUCTS ====================

@app.route('/api/products', methods=['GET'])
def list_products():
    try:
        limit = request.args.get('limit', 100, type=int)
        return jsonify({"success": True, "data": sc_app.list_products(limit)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json(silent=True) or {}
        product = sc_app.create_product(data)
        return jsonify({"success": True, "data": dict(product) if product else {}}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = sc_app.get_product(product_id)
        if product:
            return jsonify({"success": True, "data": product}), 200
        return jsonify({"success": False, "error": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        ok = sc_app.crud.delete_node(schema.LABEL_PRODUCT, schema.PROP_PRODUCT_ID, product_id)
        return jsonify({"success": ok}), 200 if ok else 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== ORDERS ====================

@app.route('/api/orders', methods=['GET'])
def list_orders():
    try:
        limit = request.args.get('limit', 100, type=int)
        return jsonify({"success": True, "data": sc_app.list_orders(limit)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json(silent=True) or {}
        order = sc_app.crud.create_node_single_label(schema.LABEL_ORDER, data)
        return jsonify({"success": True, "data": dict(order) if order else {}}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== INVENTORIES ====================

@app.route('/api/inventories', methods=['GET'])
def list_inventories():
    try:
        limit = request.args.get('limit', 100, type=int)
        return jsonify({"success": True, "data": sc_app.list_inventories(limit)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/inventories', methods=['POST'])
def create_inventory():
    try:
        data = request.get_json(silent=True) or {}
        inv = sc_app.crud.create_node_single_label(schema.LABEL_INVENTORY, data)
        return jsonify({"success": True, "data": dict(inv) if inv else {}}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== CENTERS ====================

@app.route('/api/centers', methods=['GET'])
def list_centers():
    try:
        limit = request.args.get('limit', 100, type=int)
        return jsonify({"success": True, "data": sc_app.list_centers(limit)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/centers', methods=['POST'])
def create_center():
    try:
        data = request.get_json(silent=True) or {}
        center = sc_app.crud.create_node_single_label(schema.LABEL_DISTRIBUTION_CENTER, data)
        return jsonify({"success": True, "data": dict(center) if center else {}}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== TRANSPORTS ====================

@app.route('/api/transports', methods=['GET'])
def list_transports():
    try:
        limit = request.args.get('limit', 100, type=int)
        return jsonify({"success": True, "data": sc_app.list_transports(limit)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/transports', methods=['POST'])
def create_transport():
    try:
        data = request.get_json(silent=True) or {}
        transport = sc_app.crud.create_node_single_label(schema.LABEL_TRANSPORT, data)
        return jsonify({"success": True, "data": dict(transport) if transport else {}}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== RELACIONES ====================

@app.route('/api/relationships', methods=['POST'])
def create_relationship():
    """Crear una relación entre 2 nodos existentes con propiedades."""
    try:
        data = request.get_json(silent=True) or {}
        rel = sc_app.crud.create_relationship(
            from_label=data['from_label'],
            from_id_prop=data.get('from_id_prop', _id_prop_for(data['from_label'])),
            from_id=data['from_id'],
            to_label=data['to_label'],
            to_id_prop=data.get('to_id_prop', _id_prop_for(data['to_label'])),
            to_id=data['to_id'],
            rel_type=data['rel_type'],
            properties=data.get('properties', {}),
        )
        return jsonify({"success": True, "data": dict(rel) if rel else {}}), 201
    except KeyError as e:
        return jsonify({"success": False, "error": f"Campo requerido faltante: {e}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/relationships', methods=['PATCH'])
def update_relationship_props():
    """Agregar/actualizar propiedades en una relación."""
    try:
        data = request.get_json(silent=True) or {}
        rel = sc_app.crud.add_properties_to_relationship(
            from_label=data['from_label'],
            from_id_prop=data.get('from_id_prop', _id_prop_for(data['from_label'])),
            from_id=data['from_id'],
            to_label=data['to_label'],
            to_id_prop=data.get('to_id_prop', _id_prop_for(data['to_label'])),
            to_id=data['to_id'],
            rel_type=data['rel_type'],
            properties=data.get('properties', {}),
        )
        return jsonify({"success": True, "data": dict(rel) if rel else {}}), 200
    except KeyError as e:
        return jsonify({"success": False, "error": f"Campo requerido faltante: {e}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/relationships/remove-properties', methods=['POST'])
def remove_relationship_props():
    """Eliminar propiedades de una relación."""
    try:
        data = request.get_json(silent=True) or {}
        rel = sc_app.crud.remove_properties_from_relationship(
            from_label=data['from_label'],
            from_id_prop=data.get('from_id_prop', _id_prop_for(data['from_label'])),
            from_id=data['from_id'],
            to_label=data['to_label'],
            to_id_prop=data.get('to_id_prop', _id_prop_for(data['to_label'])),
            to_id=data['to_id'],
            rel_type=data['rel_type'],
            property_names=data.get('property_names', []),
        )
        return jsonify({"success": True, "data": dict(rel) if rel else {}}), 200
    except KeyError as e:
        return jsonify({"success": False, "error": f"Campo requerido faltante: {e}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/relationships', methods=['DELETE'])
def delete_relationship():
    """Eliminar una relación."""
    try:
        data = request.get_json(silent=True) or {}
        ok = sc_app.crud.delete_relationship(
            from_label=data['from_label'],
            from_id_prop=data.get('from_id_prop', _id_prop_for(data['from_label'])),
            from_id=data['from_id'],
            to_label=data['to_label'],
            to_id_prop=data.get('to_id_prop', _id_prop_for(data['to_label'])),
            to_id=data['to_id'],
            rel_type=data['rel_type'],
        )
        return jsonify({"success": ok}), 200 if ok else 404
    except KeyError as e:
        return jsonify({"success": False, "error": f"Campo requerido faltante: {e}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/relationships/bulk/update', methods=['POST'])
def bulk_update_relationships():
    """Agregar/actualizar propiedades en múltiples relaciones."""
    try:
        data = request.get_json(silent=True) or {}
        count = sc_app.crud.add_properties_to_multiple_relationships(
            rel_type=data['rel_type'],
            filter_label=data['filter_label'],
            filter_prop=data['filter_prop'],
            filter_values=data['filter_values'],
            properties=data.get('properties', {}),
        )
        return jsonify({"success": True, "updated": count}), 200
    except KeyError as e:
        return jsonify({"success": False, "error": f"Campo requerido faltante: {e}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/relationships/bulk/remove-properties', methods=['POST'])
def bulk_remove_relationship_props():
    """Eliminar propiedades de múltiples relaciones."""
    try:
        data = request.get_json(silent=True) or {}
        count = sc_app.crud.remove_properties_from_multiple_relationships(
            rel_type=data['rel_type'],
            filter_label=data['filter_label'],
            filter_prop=data['filter_prop'],
            filter_values=data['filter_values'],
            property_names=data.get('property_names', []),
        )
        return jsonify({"success": True, "updated": count}), 200
    except KeyError as e:
        return jsonify({"success": False, "error": f"Campo requerido faltante: {e}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/relationships/bulk/delete', methods=['POST'])
def bulk_delete_relationships():
    """Eliminar múltiples relaciones por filtro."""
    try:
        data = request.get_json(silent=True) or {}
        count = sc_app.crud.delete_multiple_relationships(
            rel_type=data['rel_type'],
            filter_label=data['filter_label'],
            filter_prop=data['filter_prop'],
            filter_values=data['filter_values'],
        )
        return jsonify({"success": True, "deleted": count}), 200
    except KeyError as e:
        return jsonify({"success": False, "error": f"Campo requerido faltante: {e}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== QUERIES ====================

@app.route('/api/queries/products-by-category/<category>', methods=['GET'])
def query_products_by_category(category):
    try:
        data = sc_app.products_by_category(category)
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/queries/top-suppliers', methods=['GET'])
def query_top_suppliers():
    try:
        limit = request.args.get('limit', 10, type=int)
        data = sc_app.top_suppliers_by_rating(limit)
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/queries/pending-orders', methods=['GET'])
def query_pending_orders():
    try:
        limit = request.args.get('limit', 50, type=int)
        data = sc_app.pending_orders(limit)
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/queries/transport-status', methods=['GET'])
def query_transport_status():
    try:
        limit = request.args.get('limit', 50, type=int)
        data = sc_app.transport_status(limit)
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/queries/inventory-for-product/<int:product_id>', methods=['GET'])
def query_inventory_for_product(product_id):
    try:
        data = sc_app.inventory_status_for_product(product_id)
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== ANALYTICS ====================

@app.route('/api/analytics/stockouts', methods=['GET'])
def analytics_stockouts():
    try:
        limit = request.args.get('limit', 10, type=int)
        data = sc_app.detect_stockouts(limit)
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/analytics/reorder', methods=['GET'])
def analytics_reorder():
    try:
        limit = request.args.get('limit', 10, type=int)
        data = sc_app.suggest_reorder(limit)
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/analytics/top-suppliers', methods=['GET'])
def analytics_top_suppliers():
    try:
        limit = request.args.get('limit', 10, type=int)
        data = sc_app.top_suppliers_by_volume(limit)
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/analytics/transport-overview', methods=['GET'])
def analytics_transport_overview():
    try:
        data = sc_app.transport_overview()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== RUNNER ====================

def run_api(host: str = "0.0.0.0", port: int = 5000, debug: bool = False) -> None:
    app.run(debug=debug, host=host, port=port)


if __name__ == '__main__':
    run_api(debug=True)
