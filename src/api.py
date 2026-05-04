"""API Flask para la Cadena de Suministros.

Proporciona endpoints REST para inicializar datos e interactuar con
proveedores, productos, órdenes, inventarios, centros y transportes.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from .app import SupplyChainApp

app = Flask(__name__)
CORS(app)

# Instancia global de la aplicacion
sc_app = SupplyChainApp()


@app.route('/api/init', methods=['POST'])
def initialize():
    """Inicializar base de datos con datos de ejemplo."""
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


# Suppliers
@app.route('/api/suppliers', methods=['GET'])
def list_suppliers():
    try:
        limit = request.args.get('limit', 100, type=int)
        suppliers = sc_app.list_suppliers(limit)
        return jsonify({"success": True, "data": suppliers}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/suppliers', methods=['POST'])
def create_supplier():
    try:
        data = request.get_json(silent=True) or {}
        supplier = sc_app.create_supplier(data)
        return jsonify({"success": True, "data": supplier}), 201
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


# Products
@app.route('/api/products', methods=['GET'])
def list_products():
    try:
        limit = request.args.get('limit', 100, type=int)
        products = sc_app.list_products(limit)
        return jsonify({"success": True, "data": products}), 200
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


# Orders / Inventories / Centers / Transports (basic listing)
@app.route('/api/orders', methods=['GET'])
def list_orders():
    try:
        limit = request.args.get('limit', 100, type=int)
        orders = sc_app.list_orders(limit)
        return jsonify({"success": True, "data": orders}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/inventories', methods=['GET'])
def list_inventories():
    try:
        limit = request.args.get('limit', 100, type=int)
        inventories = sc_app.list_inventories(limit)
        return jsonify({"success": True, "data": inventories}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/centers', methods=['GET'])
def list_centers():
    try:
        limit = request.args.get('limit', 100, type=int)
        centers = sc_app.list_centers(limit)
        return jsonify({"success": True, "data": centers}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/transports', methods=['GET'])
def list_transports():
    try:
        limit = request.args.get('limit', 100, type=int)
        transports = sc_app.list_transports(limit)
        return jsonify({"success": True, "data": transports}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"success": True, "message": "API is running"}), 200


def run_api(host: str = "0.0.0.0", port: int = 5000, debug: bool = False) -> None:
    app.run(debug=debug, host=host, port=port)


if __name__ == '__main__':
    run_api(debug=True)
