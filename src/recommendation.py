"""Analytics Engine para Supply Chain basado en grafos y algoritmos de data science.

Implementa análisis de supply chain usando:
- Detección de stockouts
- Sugerencias de reorden
- Análisis de proveedores
- Visión general de transporte
"""
from typing import List, Dict, Any
from .neo4j_conn import Neo4jConnection
from . import schema


class AnalyticsEngine:
    """Motor de análisis para supply chain."""
    
    def __init__(self, conn: Neo4jConnection):
        self.conn = conn
    
    def detect_stockouts(self, limit: int = 10) -> List[Dict]:
        """
        Detectar productos con stockout.
        
        Identifica productos con inventario en cero o por debajo del nivel mínimo.
        """
        def _detect(tx):
            cypher = """
            MATCH (p:Product)-[:STORED_IN]->(w:Warehouse)
            WHERE p.cantidad_disponible <= p.stock_minimo
            
            OPTIONAL MATCH (p)-[:BELONGS_TO]->(c:Category)
            OPTIONAL MATCH (p)-[:SUPPLIED_BY]->(s:Supplier)
            
            WITH p, w, c.nombre as categoria,
                 s.nombre as proveedor,
                 p.stock_minimo - p.cantidad_disponible as deficit
            
            RETURN p.id as producto_id,
                   p.nombre as nombre_producto,
                   p.cantidad_disponible as inventario_actual,
                   p.stock_minimo as stock_minimo,
                   deficit as deficit_inventario,
                   categoria as categoría,
                   proveedor as proveedor_principal,
                   w.nombre as almacén,
                   CASE 
                       WHEN p.cantidad_disponible = 0 THEN 'CRITICO'
                       WHEN deficit > 0 THEN 'BAJO'
                       ELSE 'NORMAL'
                   END as estado
            
            ORDER BY deficit DESC
            LIMIT $limit
            """
            result = tx.run(cypher, limit=limit)
            return result
        
        records = self.conn.execute_read(_detect)
        return [dict(record) for record in records] if records else []
    
    def suggest_reorder(self, product_id: str = None, limit: int = 10) -> List[Dict]:
        """
        Sugerir cantidad de reorden para productos.
        
        Calcula la cantidad óptima basada en demanda histórica y tiempos de entrega.
        """
        def _suggest(tx):
            if product_id:
                cypher = """
                MATCH (p:Product {id: $product_id})
                MATCH (p)-[:HAS_ORDER]->(o:Order)
                WHERE o.fecha >= date() - duration('P90D')
                
                WITH p,
                     COUNT(o) as total_orders,
                     AVG(o.cantidad) as avg_demand,
                     MAX(o.fecha) as last_order_date,
                     p.dias_entrega as lead_time
                
                WITH p, total_orders, avg_demand, last_order_date, lead_time,
                     CEIL(avg_demand * (lead_time / 30.0)) as rop,
                     CEIL(avg_demand * 1.5) as quantity
                
                RETURN p.id as producto_id,
                       p.nombre as nombre_producto,
                       p.cantidad_disponible as inventario_actual,
                       avg_demand as demanda_promedio_diaria,
                       lead_time as dias_entrega,
                       rop as punto_reorden,
                       quantity as cantidad_sugerida,
                       total_orders as ordenes_ultimos_90_dias
                """
                result = tx.run(cypher, product_id=product_id)
            else:
                cypher = """
                MATCH (p:Product)
                MATCH (p)-[:HAS_ORDER]->(o:Order)
                WHERE o.fecha >= date() - duration('P90D')
                
                WITH p,
                     COUNT(o) as total_orders,
                     AVG(o.cantidad) as avg_demand,
                     MAX(o.fecha) as last_order_date,
                     p.dias_entrega as lead_time
                
                WHERE avg_demand > 0
                WITH p, total_orders, avg_demand, last_order_date, lead_time,
                     CEIL(avg_demand * (lead_time / 30.0)) as rop,
                     CEIL(avg_demand * 1.5) as quantity
                
                RETURN p.id as producto_id,
                       p.nombre as nombre_producto,
                       p.cantidad_disponible as inventario_actual,
                       avg_demand as demanda_promedio_diaria,
                       lead_time as dias_entrega,
                       rop as punto_reorden,
                       quantity as cantidad_sugerida,
                       total_orders as ordenes_ultimos_90_dias
                
                ORDER BY cantidad_sugerida DESC
                LIMIT $limit
                """
                result = tx.run(cypher, limit=limit)
            
            return result
        
        records = self.conn.execute_read(_suggest)
        return [dict(record) for record in records] if records else []
    
    def top_suppliers(self, limit: int = 10) -> List[Dict]:
        """
        Obtener proveedores principales.
        
        Ranquea proveedores por rendimiento: puntualidad, calidad y volumen.
        """
        def _get_top(tx):
            cypher = """
            MATCH (s:Supplier)-[:SUPPLIES]->(p:Product)<-[:ORDERED]->(shipment:Shipment)
            
            WITH s,
                 COUNT(DISTINCT shipment) as total_shipments,
                 COUNT(CASE WHEN shipment.estado = 'ENTREGADO' THEN 1 END) as delivered,
                 AVG(CASE WHEN shipment.fecha_entrega <= shipment.fecha_entrega_esperada 
                     THEN 1 ELSE 0 END) as on_time_rate,
                 SUM(CASE WHEN shipment.estado = 'ENTREGADO' THEN shipment.cantidad ELSE 0 END) as total_cantidad
            
            WITH s, total_shipments, delivered, on_time_rate, total_cantidad,
                 ROUND(toFloat(delivered) / total_shipments * 100) as delivery_rate,
                 CASE 
                     WHEN on_time_rate >= 0.95 THEN 'EXCELENTE'
                     WHEN on_time_rate >= 0.85 THEN 'BUENO'
                     WHEN on_time_rate >= 0.70 THEN 'REGULAR'
                     ELSE 'POBRE'
                 END as performance
            
            OPTIONAL MATCH (s)-[:LOCATED_IN]->(loc:Location)
            OPTIONAL MATCH (s)-[:DELIVERS_TO]->(w:Warehouse)
            
            WITH s, total_shipments, delivery_rate, on_time_rate, total_cantidad, performance,
                 loc.ciudad as ciudad,
                 COUNT(DISTINCT w) as almacenes_servidos,
                 ROUND(on_time_rate * 100) as puntualidad_porcentaje
            
            RETURN s.id as proveedor_id,
                   s.nombre as nombre_proveedor,
                   ciudad as ubicación,
                   total_shipments as total_envíos,
                   delivery_rate as tasa_entrega_porcentaje,
                   puntualidad_porcentaje as puntualidad_porcentaje,
                   total_cantidad as cantidad_total_suministrada,
                   almacenes_servidos as almacenes_servidos,
                   performance as desempeño,
                   total_shipments * puntualidad_porcentaje / 100.0 as score
            
            ORDER BY score DESC
            LIMIT $limit
            """
            result = tx.run(cypher, limit=limit)
            return result
        
        records = self.conn.execute_read(_get_top)
        return [dict(record) for record in records] if records else []
    
    def transport_overview(self, limit: int = 10) -> List[Dict]:
        """
        Obtener visión general del transporte.
        
        Analiza rutas, vehículos y entregas activas.
        """
        def _overview(tx):
            cypher = """
            MATCH (v:Vehicle)-[:ASSIGNED_TO]->(r:Route)
            OPTIONAL MATCH (v)-[:CARRYING]->(shipment:Shipment)
            
            WITH v, r,
                 COUNT(DISTINCT shipment) as shipments_count,
                 SUM(CASE WHEN shipment.estado = 'EN_TRANSITO' THEN 1 ELSE 0 END) as active_shipments,
                 SUM(shipment.cantidad) as total_weight,
                 MAX(shipment.fecha_entrega_esperada) as next_delivery
            
            WITH v, r, shipments_count, active_shipments, total_weight, next_delivery,
                 CASE 
                     WHEN v.estado = 'EN_RUTA' THEN 'ACTIVO'
                     WHEN v.estado = 'EN_DEPOSITO' THEN 'DISPONIBLE'
                     ELSE 'INACTIVO'
                 END as estado_vehículo
            
            OPTIONAL MATCH (r)-[:CONNECTS]->(w1:Warehouse)
            OPTIONAL MATCH (r)-[:CONNECTS]->(w2:Warehouse)
            
            WITH v, r, shipments_count, active_shipments, total_weight, next_delivery,
                 estado_vehículo,
                 COUNT(DISTINCT w1) + COUNT(DISTINCT w2) as ubicaciones_ruta
            
            OPTIONAL MATCH (v)-[:BELONGS_TO]->(fleet:Fleet)
            
            RETURN v.id as vehículo_id,
                   v.placa as placa,
                   fleet.nombre as flota,
                   r.nombre as ruta,
                   v.capacidad as capacidad_total,
                   total_weight as peso_transportado,
                   ROUND(toFloat(total_weight) / v.capacidad * 100) as utilización_porcentaje,
                   shipments_count as envíos_asignados,
                   active_shipments as envíos_activos,
                   ubicaciones_ruta as ubicaciones_en_ruta,
                   estado_vehículo as estado,
                   next_delivery as próxima_entrega_estimada,
                   active_shipments * 10 + ROUND(toFloat(total_weight) / v.capacidad * 100) as score
            
            ORDER BY score DESC
            LIMIT $limit
            """
            result = tx.run(cypher, limit=limit)
            return result
        
        records = self.conn.execute_read(_overview)
        return [dict(record) for record in records] if records else []
