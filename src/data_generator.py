"""Generador de datos de prueba para la Cadena de Suministros.

Genera CSVs compatibles con `src/importer.py` (suppliers, products, orders,
inventories, centers, transports y relaciones principales).
"""

import csv
import random
from datetime import datetime, timedelta
import os


class DataGenerator:
    CATEGORIES = [
        "Bebidas", "Alimentos", "Lácteos", "Bebidas Energéticas", "Aguas",
        "Jugos", "Cerveza", "Vinos", "Gaseosas", "Snacks"
    ]

    COUNTRIES = [
        "Guatemala", "México", "Estados Unidos", "Colombia", "Chile",
        "Perú", "Argentina", "España", "Brasil"
    ]

    @staticmethod
    def rand_date(days_back=365*2):
        return (datetime.now() - timedelta(days=random.randint(0, days_back))).strftime("%Y-%m-%d")

    @staticmethod
    def generate_suppliers(count: int = 200) -> list:
        suppliers = []
        for i in range(count):
            suppliers.append({
                "id_proveedor": i + 1,
                "nombre": f"Proveedor_{i+1:04d}",
                "pais": random.choice(DataGenerator.COUNTRIES),
                "rating": round(random.uniform(2.5, 5.0), 2),
                "activo": "true" if random.random() > 0.1 else "false",
                "categorias": "|".join(random.sample(DataGenerator.CATEGORIES, k=random.randint(1, 3)))
            })
        return suppliers

    @staticmethod
    def generate_products(count: int = 1500) -> list:
        products = []
        for i in range(count):
            perecedero = random.random() > 0.6
            fecha_exp = DataGenerator.rand_date(365) if perecedero else ""
            products.append({
                "id_producto": i + 1,
                "nombre": f"Producto_{i+1:05d}",
                "categoria": random.choice(DataGenerator.CATEGORIES),
                "precio": round(random.uniform(0.5, 50.0), 2),
                "perecedero": "true" if perecedero else "false",
                "fecha_expiracion": fecha_exp
            })
        return products

    @staticmethod
    def generate_centers(count: int = 50) -> list:
        centers = []
        for i in range(count):
            centers.append({
                "id_centro": i + 1,
                "nombre": f"Centro_{i+1:03d}",
                "ciudad": f"Ciudad_{random.randint(1,200)}",
                "capacidad": random.randint(1000, 100000),
                "activo": "true" if random.random() > 0.05 else "false",
                "tipo": random.choice(["Regional", "Local", "Nacional"])
            })
        return centers

    @staticmethod
    def generate_inventories(count: int = 500) -> list:
        inventories = []
        for i in range(count):
            inventories.append({
                "id_inventario": i + 1,
                "cantidad": random.randint(0, 2000),
                "ubicacion": f"Estante_{random.randint(1,500)}",
                "capacidad_max": random.randint(500, 5000),
                "temperatura_controlada": "true" if random.random() > 0.8 else "false",
                "fecha_actualizacion": DataGenerator.rand_date(30)
            })
        return inventories

    @staticmethod
    def generate_transports(count: int = 300) -> list:
        transports = []
        for i in range(count):
            transports.append({
                "id_transporte": i + 1,
                "tipo": random.choice(["Camión", "Barco", "Avión", "Tren"]),
                "costo": round(random.uniform(50, 5000), 2),
                "duracion_dias": random.randint(1, 15),
                "estado": random.choice(["En Ruta", "En Bodega", "Entregado"]),
                "fecha_salida": DataGenerator.rand_date(30)
            })
        return transports

    @staticmethod
    def generate_orders(count: int = 2000, products=None) -> list:
        orders = []
        for i in range(count):
            total = 0.0
            urgente = random.random() > 0.9
            orders.append({
                "id_orden": i + 1,
                "fecha_orden": DataGenerator.rand_date(90),
                "estado": random.choice(["PENDIENTE", "COMPLETADA", "CANCELADA"]),
                "total": round(total, 2),
                "urgente": "true" if urgente else "false",
                "metodo_pago": random.choice(["Transferencia", "Crédito", "Contado"]) 
            })
        return orders

    @staticmethod
    def generate_relations(suppliers, products, orders, inventories, centers, transports) -> dict:
        supplies = []
        includes = []
        stored_in = []
        sent_by = []
        arrives = []
        manages = []
        destination = []

        # SUPPLIES: each supplier supplies several products
        for s in suppliers:
            for p in random.sample(products, k=random.randint(5, 30)):
                supplies.append({
                    "id_proveedor": s["id_proveedor"],
                    "id_producto": p["id_producto"],
                    "fecha": DataGenerator.rand_date(365),
                    "costo": round(random.uniform(0.1, p["precio"] * 0.8), 2)
                })

        # INCLUDES: orders include 1-10 products
        for o in orders:
            for p in random.sample(products, k=random.randint(1, 6)):
                cantidad = random.randint(1, 100)
                precio_unitario = p["precio"]
                includes.append({
                    "id_orden": o["id_orden"],
                    "id_producto": p["id_producto"],
                    "cantidad": cantidad,
                    "precio_unitario": precio_unitario,
                    "subtotal": round(cantidad * precio_unitario, 2)
                })

        # STORED_IN: map some products to inventories
        for p in random.sample(products, k=min(len(products), len(inventories) * 3)):
            inv = random.choice(inventories)
            stored_in.append({
                "id_producto": p["id_producto"],
                "id_inventario": inv["id_inventario"],
                "fecha_ingreso": DataGenerator.rand_date(30),
                "cantidad": random.randint(1, inv["capacidad_max"]),
                "estado": random.choice(["Bueno", "Dañado", "Por Revisar"]) 
            })

        # SENT_BY: some orders assigned to transports
        for o in random.sample(orders, k=int(len(orders) * 0.7)):
            t = random.choice(transports)
            sent_by.append({
                "id_orden": o["id_orden"],
                "id_transporte": t["id_transporte"],
                "fecha_envio": DataGenerator.rand_date(30),
                "costo_envio": round(random.uniform(20, 1000), 2),
                "estado": random.choice(["En Ruta", "Entregado", "Programado"]) 
            })

        # ARRIVES/DEPARTS: transport events with centers
        for t in transports:
            c = random.choice(centers)
            arrives.append({
                "id_transporte": t["id_transporte"],
                "id_centro": c["id_centro"],
                "fecha_llegada": DataGenerator.rand_date(30),
                "tiempo_real": random.randint(1, 72),
                "fecha_salida": DataGenerator.rand_date(30),
                "tiempo_estimado": random.randint(1, 72),
                "estado": random.choice(["En Ruta", "En Bodega", "Entregado"]) 
            })

        # MANAGES: centers manage inventories
        for inv in inventories:
            c = random.choice(centers)
            manages.append({
                "id_centro": c["id_centro"],
                "id_inventario": inv["id_inventario"],
                "fecha": DataGenerator.rand_date(30),
                "responsable": f"Encargado_{random.randint(1,100)}",
                "estado": random.choice(["Activo", "Reubicado"]) 
            })

        # DESTINATION: orders get assigned to distribution centers
        for o in orders:
            c = random.choice(centers)
            destination.append({
                "id_orden": o["id_orden"],
                "id_centro": c["id_centro"],
                "fecha_entrega": DataGenerator.rand_date(30),
                "prioridad": random.randint(1, 5),
                "estado": random.choice(["Programado", "Entregado", "Retrasado"]) 
            })

        return {
            "supplies": supplies,
            "includes": includes,
            "stored_in": stored_in,
            "sent_by": sent_by,
            "arrives": arrives,
            "manages": manages,
            "destination": destination
        }

    @staticmethod
    def save_to_csv(data: list, filename: str, data_dir: str = "data"):
        os.makedirs(data_dir, exist_ok=True)
        filepath = os.path.join(data_dir, filename)

        if not data:
            # create an empty file with headerless content if necessary
            open(filepath, 'w', encoding='utf-8').close()
            return filepath

        keys = list(data[0].keys())
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

        print(f"Generado: {filepath} ({len(data)} registros)")
        return filepath

    @staticmethod
    def generate_all(data_dir: str = "data"):
        print("Generando datos de cadena de suministros...")

        # Ajuste de tamaños para superar 5.000 nodos totales
        suppliers = DataGenerator.generate_suppliers(250)
        products = DataGenerator.generate_products(2000)
        centers = DataGenerator.generate_centers(60)
        inventories = DataGenerator.generate_inventories(800)
        transports = DataGenerator.generate_transports(300)
        orders = DataGenerator.generate_orders(2000, products)

        DataGenerator.save_to_csv(suppliers, "suppliers.csv", data_dir)
        DataGenerator.save_to_csv(products, "products.csv", data_dir)
        DataGenerator.save_to_csv(centers, "centers.csv", data_dir)
        DataGenerator.save_to_csv(inventories, "inventories.csv", data_dir)
        DataGenerator.save_to_csv(transports, "transports.csv", data_dir)
        DataGenerator.save_to_csv(orders, "orders.csv", data_dir)

        rels = DataGenerator.generate_relations(suppliers, products, orders, inventories, centers, transports)
        for name, rows in rels.items():
            DataGenerator.save_to_csv(rows, f"{name}.csv", data_dir)

        total_nodes = len(suppliers) + len(products) + len(centers) + len(inventories) + len(transports) + len(orders)
        total_rels = sum(len(v) for v in rels.values())

        print(f"\n Generación completada!")
        print(f"   Total de nodos: {total_nodes:,}")
        print(f"   Total de relaciones: {total_rels:,}")

        return data_dir


if __name__ == "__main__":
    DataGenerator.generate_all()
