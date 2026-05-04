"""API Flask para la Cadena de Suministros.

Proporciona endpoints REST para inicializar datos e interactuar con
proveedores, productos, órdenes, inventarios, centros y transportes.
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from .app import SupplyChainApp

app = Flask(__name__)
CORS(app)

# Instancia global de la aplicacion
sc_app = SupplyChainApp()


@app.route('/', methods=['GET'])
def dashboard():
    """Dashboard HTML simple."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Supply Chain Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
            h1 { color: #333; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 20px 0; }
            .stat-box { background: #007bff; color: white; padding: 15px; border-radius: 5px; text-align: center; }
            .stat-label { font-size: 12px; opacity: 0.9; }
            .stat-value { font-size: 24px; font-weight: bold; }
            .endpoints { margin-top: 20px; }
            .endpoint { background: #f9f9f9; padding: 10px; margin: 5px 0; border-left: 3px solid #007bff; }
            .endpoint code { background: #f0f0f0; padding: 2px 5px; border-radius: 3px; }
            .success { color: #28a745; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Supply Chain Management Dashboard</h1>
            <p>Sistema de Cadena de Suministros - Neo4j Graph Database</p>
            
            <div id="stats" class="stats">
                <div class="stat-box"><div class="stat-label">Total Nodos</div><div class="stat-value">-</div></div>
                <div class="stat-box"><div class="stat-label">Total Relaciones</div><div class="stat-value">-</div></div>
                <div class="stat-box"><div class="stat-label">Proveedores</div><div class="stat-value">-</div></div>
                <div class="stat-box"><div class="stat-label">Productos</div><div class="stat-value">-</div></div>
                <div class="stat-box"><div class="stat-label">Órdenes</div><div class="stat-value">-</div></div>
                <div class="stat-box"><div class="stat-label">Centros</div><div class="stat-value">-</div></div>
            </div>

            <div class="endpoints">
                <h2>API Endpoints</h2>
                <div class="endpoint"><code>GET /api/stats</code> - Obtener estadísticas del grafo</div>
                <div class="endpoint"><code>GET /api/suppliers</code> - Listar proveedores</div>
                <div class="endpoint"><code>GET /api/products</code> - Listar productos</div>
                <div class="endpoint"><code>GET /api/orders</code> - Listar órdenes</div>
                <div class="endpoint"><code>GET /api/inventories</code> - Listar inventarios</div>
                <div class="endpoint"><code>GET /api/centers</code> - Listar centros de distribución</div>
                <div class="endpoint"><code>GET /api/transports</code> - Listar transportes</div>
                <div class="endpoint"><code>POST /api/init</code> - Inicializar base de datos</div>
            </div>

            <p style="margin-top: 30px; font-size: 12px; color: #666;">
                <span class="success">✓</span> API Running | 
                Proyecto: PRY2-BD2 | 
                Database: Neo4j
            </p>
        </div>

        <script>
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    if (data.success && data.data) {
                        const s = data.data;
                        const statBoxes = document.querySelectorAll('.stat-box');
                        statBoxes[0].innerHTML = `<div class="stat-label">Total Nodos</div><div class="stat-value">${s.total_nodes}</div>`;
                        statBoxes[1].innerHTML = `<div class="stat-label">Total Relaciones</div><div class="stat-value">${s.total_relationships}</div>`;
                        statBoxes[2].innerHTML = `<div class="stat-label">Proveedores</div><div class="stat-value">${s.total_suppliers}</div>`;
                        statBoxes[3].innerHTML = `<div class="stat-label">Productos</div><div class="stat-value">${s.total_products}</div>`;
                        statBoxes[4].innerHTML = `<div class="stat-label">Órdenes</div><div class="stat-value">${s.total_orders}</div>`;
                        statBoxes[5].innerHTML = `<div class="stat-label">Centros</div><div class="stat-value">${s.total_centers}</div>`;
                    }
                })
                .catch(e => console.error('Error:', e));
        </script>
    </body>
    </html>
    """
    return render_template_string(html)


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
