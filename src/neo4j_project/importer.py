"""Esqueleto para importar datos a Neo4j.

Este módulo debe adaptarse según el formato de origen (CSV, JSON, SQL, etc.).
Contiene funciones ejemplo para añadir nodos y relaciones.
"""
from typing import Iterable, Dict
from .neo4j_conn import get_connection


def create_person(tx, person: Dict):
    query = (
        "MERGE (p:Person {id: $id})\n"
        "SET p.name = $name, p.attrs = $attrs\n"
        "RETURN p"
    )
    return tx.run(query, id=person["id"], name=person.get("name"), attrs=person.get("attrs", {})).single()


def import_people(people: Iterable[Dict]):
    conn = get_connection()
    try:
        for person in people:
            conn.execute_write(create_person, person)
    finally:
        conn.close()


def example_usage():
    sample = [
        {"id": "p1", "name": "Alice", "attrs": {"age": 30}},
        {"id": "p2", "name": "Bob", "attrs": {"age": 28}},
    ]
    import_people(sample)


if __name__ == "__main__":
    example_usage()
