"""Operaciones CRUD para nodos y relaciones.

Implementa todas las operaciones requeridas por la rúbrica de evaluación.
"""
from datetime import datetime
from typing import Dict, List, Any, Optional
from .neo4j_conn import Neo4jConnection
from . import schema


class CrudOperations:
    """Maneja todas las operaciones CRUD en el grafo."""
    
    def __init__(self, conn: Neo4jConnection):
        self.conn = conn
    
    # ============ NODOS - CREACIÓN ============
    
    def create_node_single_label(self, label: str, properties: Dict) -> Dict:
        """Crear un nodo con una sola etiqueta."""
        def _create(tx):
            prop_string = ", ".join([f"{k}: ${k}" for k in properties.keys()])
            query = f"CREATE (n:{label} {{{prop_string}}}) RETURN n"
            result = tx.run(query, **properties)
            return result.single()[0] if result else None
        
        return self.conn.execute_write(_create)
    
    def create_node_multi_label(self, labels: List[str], properties: Dict) -> Dict:
        """Crear un nodo con 2+ etiquetas."""
        def _create(tx):
            labels_str = ":".join(labels)
            prop_string = ", ".join([f"{k}: ${k}" for k in properties.keys()])
            query = f"CREATE (n:{labels_str} {{{prop_string}}}) RETURN n"
            result = tx.run(query, **properties)
            return result.single()[0] if result else None
        
        return self.conn.execute_write(_create)
    
    def create_user(self, user_data: Dict) -> Dict:
        """Crear un usuario."""
        return self.create_node_single_label(schema.LABEL_USER, user_data)
    
    def create_movie(self, movie_data: Dict) -> Dict:
        """Crear una película."""
        return self.create_node_single_label(schema.LABEL_MOVIE, movie_data)
    
    def create_genre(self, genre_data: Dict) -> Dict:
        """Crear un género."""
        return self.create_node_single_label(schema.LABEL_GENRE, genre_data)
    
    def create_actor(self, actor_data: Dict) -> Dict:
        """Crear un actor."""
        return self.create_node_single_label(schema.LABEL_ACTOR, actor_data)
    
    def create_director(self, director_data: Dict) -> Dict:
        """Crear un director."""
        return self.create_node_single_label(schema.LABEL_DIRECTOR, director_data)
    
    # ============ NODOS - LECTURA ============
    
    def get_node_by_id(self, label: str, id_prop: str, id_value: str) -> Optional[Dict]:
        """Obtener un nodo por su ID."""
        def _get(tx):
            query = f"MATCH (n:{label} {{{id_prop}: ${id_prop}}}) RETURN n"
            result = tx.run(query, **{id_prop: id_value})
            return result.single()
        
        result = self.conn.execute_read(_get)
        return dict(result[0]) if result else None
    
    def get_nodes_by_filter(self, label: str, filters: Dict) -> List[Dict]:
        """Obtener múltiples nodos con filtros."""
        def _get(tx):
            filter_string = " AND ".join([f"n.{k} = ${k}" for k in filters.keys()])
            query = f"MATCH (n:{label}) WHERE {filter_string} RETURN n"
            result = tx.run(query, **filters)
            return result
        
        records = self.conn.execute_read(_get)
        return [dict(record[0]) for record in records] if records else []
    
    def get_all_nodes(self, label: str) -> List[Dict]:
        """Obtener todos los nodos de un tipo."""
        def _get(tx):
            query = f"MATCH (n:{label}) RETURN n LIMIT 1000"
            result = tx.run(query)
            return result
        
        records = self.conn.execute_read(_get)
        return [dict(record[0]) for record in records] if records else []
    
    def get_node_aggregation(self, label: str, agg_func: str, prop: str) -> Any:
        """Realizar agregaciones sobre propiedades de nodos."""
        def _get(tx):
            query = f"MATCH (n:{label}) RETURN {agg_func}(n.{prop}) as result"
            result = tx.run(query)
            record = result.single()
            return record["result"] if record else None
        
        return self.conn.execute_read(_get)
    
    # ============ NODOS - ACTUALIZACIÓN ============
    
    def add_properties_to_node(self, label: str, id_prop: str, 
                              id_value: str, properties: Dict) -> Dict:
        """Agregar una o más propiedades a un nodo."""
        def _update(tx):
            set_string = ", ".join([f"n.{k} = ${k}" for k in properties.keys()])
            query = f"MATCH (n:{label} {{{id_prop}: ${id_prop}}}) SET {set_string} RETURN n"
            params = {id_prop: id_value, **properties}
            result = tx.run(query, **params)
            return result.single()[0] if result else None
        
        return self.conn.execute_write(_update)
    
    def add_properties_to_multiple_nodes(self, label: str, filter_prop: str, 
                                        filter_values: List, properties: Dict) -> int:
        """Agregar propiedades a múltiples nodos."""
        def _update(tx):
            set_string = ", ".join([f"n.{k} = ${k}" for k in properties.keys()])
            query = f"""MATCH (n:{label}) 
                       WHERE n.{filter_prop} IN $filter_values 
                       SET {set_string} 
                       RETURN count(n) as updated"""
            params = {**properties, "filter_values": filter_values}
            result = tx.run(query, **params)
            return result.single()["updated"] if result else 0
        
        return self.conn.execute_write(_update)
    
    def update_properties_in_node(self, label: str, id_prop: str,
                                 id_value: str, properties: Dict) -> Dict:
        """Actualizar propiedades de un nodo."""
        return self.add_properties_to_node(label, id_prop, id_value, properties)
    
    def update_properties_in_multiple_nodes(self, label: str, filter_prop: str,
                                           filter_values: List, properties: Dict) -> int:
        """Actualizar propiedades en múltiples nodos."""
        return self.add_properties_to_multiple_nodes(label, filter_prop, filter_values, properties)
    
    # ============ NODOS - ELIMINACIÓN ============
    
    def remove_properties_from_node(self, label: str, id_prop: str,
                                   id_value: str, property_names: List[str]) -> Dict:
        """Eliminar una o más propiedades de un nodo."""
        def _delete(tx):
            remove_string = ", ".join([f"n.{prop}" for prop in property_names])
            query = f"MATCH (n:{label} {{{id_prop}: ${id_prop}}}) REMOVE {remove_string} RETURN n"
            result = tx.run(query, **{id_prop: id_value})
            return result.single()[0] if result else None
        
        return self.conn.execute_write(_delete)
    
    def remove_properties_from_multiple_nodes(self, label: str, filter_prop: str,
                                             filter_values: List, property_names: List[str]) -> int:
        """Eliminar propiedades de múltiples nodos."""
        def _delete(tx):
            remove_string = ", ".join([f"n.{prop}" for prop in property_names])
            query = f"""MATCH (n:{label}) 
                       WHERE n.{filter_prop} IN $filter_values 
                       REMOVE {remove_string} 
                       RETURN count(n) as updated"""
            result = tx.run(query, filter_values=filter_values)
            return result.single()["updated"] if result else 0
        
        return self.conn.execute_write(_delete)
    
    def delete_node(self, label: str, id_prop: str, id_value: str) -> bool:
        """Eliminar un nodo y sus relaciones."""
        def _delete(tx):
            query = f"MATCH (n:{label} {{{id_prop}: ${id_prop}}}) DETACH DELETE n RETURN 1"
            result = tx.run(query, **{id_prop: id_value})
            return result.single() is not None
        
        return self.conn.execute_write(_delete)
    
    def delete_multiple_nodes(self, label: str, filter_prop: str,
                             filter_values: List) -> int:
        """Eliminar múltiples nodos."""
        def _delete(tx):
            query = f"""MATCH (n:{label}) 
                       WHERE n.{filter_prop} IN $filter_values 
                       DETACH DELETE n 
                       RETURN count(n) as deleted"""
            result = tx.run(query, filter_values=filter_values)
            return result.single()["deleted"] if result else 0
        
        return self.conn.execute_write(_delete)
    
    # ============ RELACIONES - CREACIÓN ============
    
    def create_relationship(self, from_label: str, from_id_prop: str, from_id: str,
                          to_label: str, to_id_prop: str, to_id: str,
                          rel_type: str, properties: Dict = None) -> Dict:
        """Crear una relación entre dos nodos existentes con propiedades."""
        def _create(tx):
            properties = properties or {}
            prop_string = ""
            if properties:
                prop_string = "{" + ", ".join([f"{k}: ${k}" for k in properties.keys()]) + "}"
            
            query = f"""MATCH (a:{from_label} {{{from_id_prop}: ${from_id_prop}}}),
                             (b:{to_label} {{{to_id_prop}: ${to_id_prop}}})
                       CREATE (a)-[r:{rel_type} {prop_string}]->(b)
                       RETURN r"""
            
            params = {
                from_id_prop: from_id,
                to_id_prop: to_id,
                **properties
            }
            result = tx.run(query, **params)
            return result.single()[0] if result else None
        
        return self.conn.execute_write(_create)
    
    # ============ RELACIONES - ACTUALIZACIÓN ============
    
    def add_properties_to_relationship(self, from_label: str, from_id_prop: str, from_id: str,
                                      to_label: str, to_id_prop: str, to_id: str,
                                      rel_type: str, properties: Dict) -> Dict:
        """Agregar propiedades a una relación."""
        def _update(tx):
            set_string = ", ".join([f"r.{k} = ${k}" for k in properties.keys()])
            query = f"""MATCH (a:{from_label} {{{from_id_prop}: ${from_id_prop}}})-[r:{rel_type}]->(b:{to_label} {{{to_id_prop}: ${to_id_prop}}})
                       SET {set_string}
                       RETURN r"""
            
            params = {
                from_id_prop: from_id,
                to_id_prop: to_id,
                **properties
            }
            result = tx.run(query, **params)
            return result.single()[0] if result else None
        
        return self.conn.execute_write(_update)
    
    def add_properties_to_multiple_relationships(self, rel_type: str,
                                               filter_label: str, filter_prop: str, filter_values: List,
                                               properties: Dict) -> int:
        """Agregar propiedades a múltiples relaciones."""
        def _update(tx):
            set_string = ", ".join([f"r.{k} = ${k}" for k in properties.keys()])
            query = f"""MATCH (n:{filter_label})-[r:{rel_type}]-()
                       WHERE n.{filter_prop} IN $filter_values
                       SET {set_string}
                       RETURN count(r) as updated"""
            params = {**properties, "filter_values": filter_values}
            result = tx.run(query, **params)
            return result.single()["updated"] if result else 0
        
        return self.conn.execute_write(_update)
    
    def update_relationship_properties(self, from_label: str, from_id_prop: str, from_id: str,
                                      to_label: str, to_id_prop: str, to_id: str,
                                      rel_type: str, properties: Dict) -> Dict:
        """Actualizar propiedades de una relación."""
        return self.add_properties_to_relationship(from_label, from_id_prop, from_id,
                                                   to_label, to_id_prop, to_id,
                                                   rel_type, properties)
    
    # ============ RELACIONES - ELIMINACIÓN ============
    
    def remove_properties_from_relationship(self, from_label: str, from_id_prop: str, from_id: str,
                                           to_label: str, to_id_prop: str, to_id: str,
                                           rel_type: str, property_names: List[str]) -> Dict:
        """Eliminar propiedades de una relación."""
        def _delete(tx):
            remove_string = ", ".join([f"r.{prop}" for prop in property_names])
            query = f"""MATCH (a:{from_label} {{{from_id_prop}: ${from_id_prop}}})-[r:{rel_type}]->(b:{to_label} {{{to_id_prop}: ${to_id_prop}}})
                       REMOVE {remove_string}
                       RETURN r"""
            
            params = {
                from_id_prop: from_id,
                to_id_prop: to_id
            }
            result = tx.run(query, **params)
            return result.single()[0] if result else None
        
        return self.conn.execute_write(_delete)
    
    def remove_properties_from_multiple_relationships(self, rel_type: str,
                                                     filter_label: str, filter_prop: str, filter_values: List,
                                                     property_names: List[str]) -> int:
        """Eliminar propiedades de múltiples relaciones."""
        def _delete(tx):
            remove_string = ", ".join([f"r.{prop}" for prop in property_names])
            query = f"""MATCH (n:{filter_label})-[r:{rel_type}]-()
                       WHERE n.{filter_prop} IN $filter_values
                       REMOVE {remove_string}
                       RETURN count(r) as updated"""
            result = tx.run(query, filter_values=filter_values)
            return result.single()["updated"] if result else 0
        
        return self.conn.execute_write(_delete)
    
    def delete_relationship(self, from_label: str, from_id_prop: str, from_id: str,
                           to_label: str, to_id_prop: str, to_id: str,
                           rel_type: str) -> bool:
        """Eliminar una relación."""
        def _delete(tx):
            query = f"""MATCH (a:{from_label} {{{from_id_prop}: ${from_id_prop}}})-[r:{rel_type}]->(b:{to_label} {{{to_id_prop}: ${to_id_prop}}})
                       DELETE r
                       RETURN 1"""
            
            params = {
                from_id_prop: from_id,
                to_id_prop: to_id
            }
            result = tx.run(query, **params)
            return result.single() is not None
        
        return self.conn.execute_write(_delete)
    
    def delete_multiple_relationships(self, rel_type: str,
                                     filter_label: str, filter_prop: str, filter_values: List) -> int:
        """Eliminar múltiples relaciones."""
        def _delete(tx):
            query = f"""MATCH (n:{filter_label})-[r:{rel_type}]-()
                       WHERE n.{filter_prop} IN $filter_values
                       DELETE r
                       RETURN count(r) as deleted"""
            result = tx.run(query, filter_values=filter_values)
            return result.single()["deleted"] if result else 0
        
        return self.conn.execute_write(_delete)
    
    # ============ UTILIDADES ============
    
    def count_nodes(self, label: str) -> int:
        """Contar nodos de un tipo."""
        def _count(tx):
            query = f"MATCH (n:{label}) RETURN count(n) as count"
            result = tx.run(query)
            return result.single()["count"] if result else 0
        
        return self.conn.execute_read(_count)
    
    def count_all_nodes(self) -> int:
        """Contar todos los nodos en el grafo."""
        def _count(tx):
            query = "MATCH (n) RETURN count(n) as count"
            result = tx.run(query)
            return result.single()["count"] if result else 0
        
        return self.conn.execute_read(_count)
    
    def count_relationships(self, rel_type: str = None) -> int:
        """Contar relaciones."""
        def _count(tx):
            if rel_type:
                query = f"MATCH ()-[r:{rel_type}]-() RETURN count(r) as count"
            else:
                query = "MATCH ()-[r]-() RETURN count(r) as count"
            result = tx.run(query)
            return result.single()["count"] if result else 0
        
        return self.conn.execute_read(_count)
    
    def is_graph_connected(self) -> bool:
        """Verificar si el grafo es conexo."""
        def _check(tx):
            query = """
            MATCH (n)
            WITH n LIMIT 1
            MATCH (n)-[*0..]-(m)
            RETURN count(DISTINCT m) as reachable
            """
            result = tx.run(query)
            reachable = result.single()["reachable"] if result else 0

            total_result = tx.run("MATCH (n) RETURN count(n) as count")
            total = total_result.single()["count"] if total_result else 0
            return reachable == total
        
        return self.conn.execute_read(_check)
