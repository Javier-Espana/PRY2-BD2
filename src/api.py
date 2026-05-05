"""API Flask para la Cadena de Suministros."""

import os
import csv
import io
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from .app import SupplyChainApp
from . import schema

app = Flask(__name__)
CORS(app)

sc_app = SupplyChainApp()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_PATH = os.path.join(BASE_DIR, '..', 'app', 'code.html')

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


def _s(obj):
    """Convierte tipos Neo4j (Date, DateTime, etc.) a tipos JSON-serializables."""
    if isinstance(obj, dict):
        return {k: _s(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_s(v) for v in obj]
    if hasattr(obj, 'isoformat'):   # neo4j.time.Date / DateTime
        return obj.isoformat()
    return obj


def _coerce(v):
    """Coerce a string value to int/float/bool as appropriate."""
    if not isinstance(v, str):
        return v
    if v.lower() == 'true':
        return True
    if v.lower() == 'false':
        return False
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    return v


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
        return jsonify({"success": True, "data": _s(sc_app.get_graph_stats())}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== NODOS GENÉRICOS ====================

@app.route('/api/nodes', methods=['POST'])
def create_node():
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
        return jsonify({"success": True, "data": _s(dict(node)) if node else {}}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>', methods=['GET'])
def list_nodes_by_label(label):
    try:
        limit = request.args.get('limit', 100, type=int)
        filter_key = request.args.get('filter_key')
        filter_val = request.args.get('filter_val')
        if filter_key and filter_val:
            nodes = sc_app.crud.get_nodes_by_filter(label, {filter_key: filter_val})
        else:
            nodes = sc_app.crud.get_all_nodes(label)[:limit]
        return jsonify({"success": True, "data": _s(nodes)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>/<id_value>', methods=['GET'])
def get_node(label, id_value):
    try:
        id_prop = request.args.get('id_prop', _id_prop_for(label))
        node = sc_app.crud.get_node_by_id(label, id_prop, id_value)
        if node:
            return jsonify({"success": True, "data": _s(node)}), 200
        return jsonify({"success": False, "error": "Nodo no encontrado"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>/<id_value>', methods=['PATCH'])
def update_node_props(label, id_value):
    try:
        data = request.get_json(silent=True) or {}
        id_prop = data.pop('id_prop', _id_prop_for(label))
        properties = data.get('properties', data)
        node = sc_app.crud.add_properties_to_node(label, id_prop, id_value, properties)
        return jsonify({"success": True, "data": _s(dict(node)) if node else {}}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>/<id_value>', methods=['DELETE'])
def delete_node(label, id_value):
    try:
        id_prop = request.args.get('id_prop', _id_prop_for(label))
        ok = sc_app.crud.delete_node(label, id_prop, id_value)
        return jsonify({"success": ok}), 200 if ok else 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>/<id_value>/remove-properties', methods=['POST'])
def remove_node_props(label, id_value):
    try:
        data = request.get_json(silent=True) or {}
        id_prop = data.get('id_prop', _id_prop_for(label))
        property_names = data.get('property_names', [])
        node = sc_app.crud.remove_properties_from_node(label, id_prop, id_value, property_names)
        return jsonify({"success": True, "data": _s(dict(node)) if node else {}}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>/bulk/update', methods=['POST'])
def bulk_update_nodes(label):
    try:
        data = request.get_json(silent=True) or {}
        count = sc_app.crud.add_properties_to_multiple_nodes(
            label, data.get('filter_prop'), data.get('filter_values', []),
            data.get('properties', {}))
        return jsonify({"success": True, "updated": count}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>/bulk/delete', methods=['POST'])
def bulk_delete_nodes(label):
    try:
        data = request.get_json(silent=True) or {}
        count = sc_app.crud.delete_multiple_nodes(
            label, data.get('filter_prop'), data.get('filter_values', []))
        return jsonify({"success": True, "deleted": count}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>/bulk/remove-properties', methods=['POST'])
def bulk_remove_node_props(label):
    try:
        data = request.get_json(silent=True) or {}
        count = sc_app.crud.remove_properties_from_multiple_nodes(
            label, data.get('filter_prop'), data.get('filter_values', []),
            data.get('property_names', []))
        return jsonify({"success": True, "updated": count}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/nodes/<label>/aggregations', methods=['GET'])
def node_aggregations(label):
    try:
        func = request.args.get('func', 'COUNT').upper()
        prop = request.args.get('prop', 'id')
        if func not in ('COUNT', 'AVG', 'MAX', 'MIN', 'SUM'):
            return jsonify({"success": False, "error": "func inválido"}), 400
        result = sc_app.crud.get_node_aggregation(label, func, prop)
        return jsonify({"success": True, "data": {"function": func, "property": prop, "result": _s(result)}}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== SUPPLIERS ====================

@app.route('/api/suppliers', methods=['GET'])
def list_suppliers():
    try:
        limit = request.args.get('limit', 100, type=int)
        return jsonify({"success": True, "data": _s(sc_app.list_suppliers(limit))}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/suppliers', methods=['POST'])
def create_supplier():
    try:
        data = request.get_json(silent=True) or {}
        supplier = sc_app.create_supplier(data)
        return jsonify({"success": True, "data": _s(dict(supplier)) if supplier else {}}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/suppliers/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    try:
        supplier = sc_app.get_supplier(supplier_id)
        if supplier:
            return jsonify({"success": True, "data": _s(supplier)}), 200
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
        return jsonify({"success": True, "data": _s(sc_app.list_products(limit))}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json(silent=True) or {}
        product = sc_app.create_product(data)
        return jsonify({"success": True, "data": _s(dict(product)) if product else {}}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = sc_app.get_product(product_id)
        if product:
            return jsonify({"success": True, "data": _s(product)}), 200
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
        return jsonify({"success": True, "data": _s(sc_app.list_orders(limit))}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json(silent=True) or {}
        order = sc_app.crud.create_node_single_label(schema.LABEL_ORDER, data)
        return jsonify({"success": True, "data": _s(dict(order)) if order else {}}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== INVENTORIES ====================

@app.route('/api/inventories', methods=['GET'])
def list_inventories():
    try:
        limit = request.args.get('limit', 100, type=int)
        return jsonify({"success": True, "data": _s(sc_app.list_inventories(limit))}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/inventories', methods=['POST'])
def create_inventory():
    try:
        data = request.get_json(silent=True) or {}
        inv = sc_app.crud.create_node_single_label(schema.LABEL_INVENTORY, data)
        return jsonify({"success": True, "data": _s(dict(inv)) if inv else {}}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== CENTERS ====================

@app.route('/api/centers', methods=['GET'])
def list_centers():
    try:
        limit = request.args.get('limit', 100, type=int)
        return jsonify({"success": True, "data": _s(sc_app.list_centers(limit))}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/centers', methods=['POST'])
def create_center():
    try:
        data = request.get_json(silent=True) or {}
        center = sc_app.crud.create_node_single_label(schema.LABEL_DISTRIBUTION_CENTER, data)
        return jsonify({"success": True, "data": _s(dict(center)) if center else {}}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== TRANSPORTS ====================

@app.route('/api/transports', methods=['GET'])
def list_transports():
    try:
        limit = request.args.get('limit', 100, type=int)
        return jsonify({"success": True, "data": _s(sc_app.list_transports(limit))}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/transports', methods=['POST'])
def create_transport():
    try:
        data = request.get_json(silent=True) or {}
        transport = sc_app.crud.create_node_single_label(schema.LABEL_TRANSPORT, data)
        return jsonify({"success": True, "data": _s(dict(transport)) if transport else {}}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== RELACIONES ====================

@app.route('/api/relationships', methods=['POST'])
def create_relationship():
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
        return jsonify({"success": True, "data": _s(dict(rel)) if rel else {}}), 201
    except KeyError as e:
        return jsonify({"success": False, "error": f"Campo requerido: {e}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/relationships', methods=['PATCH'])
def update_relationship_props():
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
        return jsonify({"success": True, "data": _s(dict(rel)) if rel else {}}), 200
    except KeyError as e:
        return jsonify({"success": False, "error": f"Campo requerido: {e}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/relationships/remove-properties', methods=['POST'])
def remove_relationship_props():
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
        return jsonify({"success": True, "data": _s(dict(rel)) if rel else {}}), 200
    except KeyError as e:
        return jsonify({"success": False, "error": f"Campo requerido: {e}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/relationships', methods=['DELETE'])
def delete_relationship():
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
        return jsonify({"success": False, "error": f"Campo requerido: {e}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/relationships/bulk/update', methods=['POST'])
def bulk_update_relationships():
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
        return jsonify({"success": False, "error": f"Campo requerido: {e}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/relationships/bulk/remove-properties', methods=['POST'])
def bulk_remove_relationship_props():
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
        return jsonify({"success": False, "error": f"Campo requerido: {e}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/relationships/bulk/delete', methods=['POST'])
def bulk_delete_relationships():
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
        return jsonify({"success": False, "error": f"Campo requerido: {e}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== QUERIES ====================

@app.route('/api/queries/products-by-category/<category>', methods=['GET'])
def query_products_by_category(category):
    try:
        return jsonify({"success": True, "data": _s(sc_app.products_by_category(category))}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/queries/top-suppliers', methods=['GET'])
def query_top_suppliers():
    try:
        limit = request.args.get('limit', 10, type=int)
        return jsonify({"success": True, "data": _s(sc_app.top_suppliers_by_rating(limit))}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/queries/pending-orders', methods=['GET'])
def query_pending_orders():
    try:
        limit = request.args.get('limit', 50, type=int)
        return jsonify({"success": True, "data": _s(sc_app.pending_orders(limit))}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/queries/transport-status', methods=['GET'])
def query_transport_status():
    try:
        limit = request.args.get('limit', 50, type=int)
        return jsonify({"success": True, "data": _s(sc_app.transport_status(limit))}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/queries/inventory-for-product/<int:product_id>', methods=['GET'])
def query_inventory_for_product(product_id):
    try:
        return jsonify({"success": True, "data": _s(sc_app.inventory_status_for_product(product_id))}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== ANALYTICS ====================

@app.route('/api/analytics/stockouts', methods=['GET'])
def analytics_stockouts():
    try:
        limit = request.args.get('limit', 10, type=int)
        return jsonify({"success": True, "data": _s(sc_app.detect_stockouts(limit))}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/analytics/reorder', methods=['GET'])
def analytics_reorder():
    try:
        limit = request.args.get('limit', 10, type=int)
        return jsonify({"success": True, "data": _s(sc_app.suggest_reorder(limit))}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/analytics/top-suppliers', methods=['GET'])
def analytics_top_suppliers():
    try:
        limit = request.args.get('limit', 10, type=int)
        return jsonify({"success": True, "data": _s(sc_app.top_suppliers_by_volume(limit))}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/analytics/transport-overview', methods=['GET'])
def analytics_transport_overview():
    try:
        return jsonify({"success": True, "data": _s(sc_app.transport_overview())}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== GRAPH VISUALIZATION ====================

@app.route('/api/graph-sample', methods=['GET'])
def graph_sample():
    """Devuelve una muestra del grafo para visualización (nodos + relaciones)."""
    limit = request.args.get('limit', 200, type=int)
    label_filter = request.args.get('label', None)
    try:
        def _get(tx):
            if label_filter:
                q = f"""
                MATCH (n:{label_filter})-[r]->(m)
                WITH n, r, m LIMIT {limit}
                RETURN id(n) AS fid, labels(n) AS fl, properties(n) AS fp,
                       id(m) AS tid, labels(m) AS tl, properties(m) AS tp,
                       type(r) AS rt
                """
            else:
                q = f"""
                MATCH (n)-[r]->(m)
                WITH n, r, m LIMIT {limit}
                RETURN id(n) AS fid, labels(n) AS fl, properties(n) AS fp,
                       id(m) AS tid, labels(m) AS tl, properties(m) AS tp,
                       type(r) AS rt
                """
            result = tx.run(q)
            nodes = {}
            edges = []
            for rec in result:
                fid, tid = rec['fid'], rec['tid']
                for nid, lbls, props in [(fid, list(rec['fl']), dict(rec['fp'])),
                                          (tid, list(rec['tl']), dict(rec['tp']))]:
                    if nid not in nodes:
                        lbl = lbls[0] if lbls else 'Node'
                        name = (props.get('nombre') or props.get('id_proveedor') or
                                props.get('id_producto') or props.get('id_orden') or
                                props.get('id_inventario') or props.get('id_centro') or
                                props.get('id_transporte') or str(nid))
                        nodes[nid] = {
                            'id': nid,
                            'label': str(name)[:18],
                            'group': lbl,
                            'title': f"<b>{lbl}</b><br/>" + "<br/>".join(
                                f"{k}: {v}" for k, v in list(props.items())[:6]
                            )
                        }
                edges.append({'from': fid, 'to': tid, 'label': rec['rt'],
                               'arrows': 'to', 'font': {'size': 8}})
            return list(nodes.values()), edges

        nodes, edges = sc_app.conn.execute_read(_get)
        return jsonify({'success': True, 'data': {'nodes': nodes, 'edges': edges}}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== CSV IMPORT ====================

@app.route('/api/import/csv', methods=['POST'])
def import_csv():
    """Importa nodos desde un archivo CSV."""
    try:
        entity_type = request.form.get('entity_type', 'Supplier')
        f = request.files.get('file')
        if not f:
            return jsonify({'success': False, 'error': 'No se proporcionó archivo CSV'}), 400
        content = f.read().decode('utf-8-sig')
        reader = csv.DictReader(io.StringIO(content))
        created, errors = 0, []
        for i, row in enumerate(reader):
            props = {}
            for k, v in row.items():
                k = (k or '').strip()
                v = (v or '').strip()
                if k and v:
                    props[k] = _coerce(v)
            if not props:
                continue
            try:
                sc_app.crud.create_node_single_label(entity_type, props)
                created += 1
            except Exception as e:
                errors.append(f"Fila {i + 2}: {str(e)[:100]}")
        return jsonify({'success': True, 'created': created, 'errors': errors[:5]}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== RUNNER ====================

def run_api(host: str = "0.0.0.0", port: int = 5000, debug: bool = False) -> None:
    app.run(debug=debug, host=host, port=port)


if __name__ == '__main__':
    run_api(debug=True)
