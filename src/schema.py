"""Esquema del grafo para la Cadena de Suministros.

Este módulo define etiquetas (labels), tipos de relaciones y propiedades
consistentes con el documento de planteamiento (Proveedor, Producto,
OrdenCompra, Inventario, CentroDistribucion, Transporte).
"""

# Etiquetas de nodos
LABEL_SUPPLIER = "Supplier"
LABEL_PRODUCT = "Product"
LABEL_ORDER = "OrderCompra"
LABEL_INVENTORY = "Inventory"
LABEL_DISTRIBUTION_CENTER = "CentroDistribucion"
LABEL_TRANSPORT = "Transporte"

# Tipos de relaciones
REL_SUPPLIES = "SUMINISTRA"
REL_RECEIVES_ORDER = "RECIBE_ORDEN"
REL_INCLUDES = "INCLUYE"
REL_SENT_BY = "SE_ENVIA_POR"
REL_STORED_IN = "ALMACENADO_EN"
REL_LOCATED_IN = "UBICADO_EN"
REL_ARRIVES_AT = "LLEGA_A"
REL_DEPARTS_FROM = "SALE_DE"
REL_MANAGES = "GESTIONA"
REL_REQUIRES = "REQUIERE"
REL_DESTINATION = "DESTINO"

# Propiedades de Supplier
PROP_SUPPLIER_ID = "id_proveedor"
PROP_SUPPLIER_NOMBRE = "nombre"
PROP_SUPPLIER_PAIS = "pais"
PROP_SUPPLIER_RATING = "rating"
PROP_SUPPLIER_ACTIVO = "activo"
PROP_SUPPLIER_CATEGORIAS = "categorias"

# Propiedades de Product
PROP_PRODUCT_ID = "id_producto"
PROP_PRODUCT_NOMBRE = "nombre"
PROP_PRODUCT_CATEGORIA = "categoria"
PROP_PRODUCT_PRECIO = "precio"
PROP_PRODUCT_PERECEDERO = "perecedero"
PROP_PRODUCT_FECHA_EXPIRACION = "fecha_expiracion"

# Propiedades de OrderCompra
PROP_ORDER_ID = "id_orden"
PROP_ORDER_FECHA = "fecha_orden"
PROP_ORDER_ESTADO = "estado"
PROP_ORDER_TOTAL = "total"
PROP_ORDER_URGENTE = "urgente"
PROP_ORDER_METODO_PAGO = "metodo_pago"

# Propiedades de Inventory
PROP_INVENTORY_ID = "id_inventario"
PROP_INVENTORY_CANTIDAD = "cantidad"
PROP_INVENTORY_UBICACION = "ubicacion"
PROP_INVENTORY_CAPACIDAD_MAX = "capacidad_max"
PROP_INVENTORY_TEMPERATURA_CONTROLADA = "temperatura_controlada"
PROP_INVENTORY_FECHA_ACTUALIZACION = "fecha_actualizacion"

# Propiedades de Transporte
PROP_TRANSPORT_ID = "id_transporte"
PROP_TRANSPORT_TIPO = "tipo"
PROP_TRANSPORT_COSTO = "costo"
PROP_TRANSPORT_DURACION_DIAS = "duracion_dias"
PROP_TRANSPORT_ESTADO = "estado"
PROP_TRANSPORT_FECHA_SALIDA = "fecha_salida"

# Propiedades de Centro de Distribucion
PROP_CENTER_ID = "id_centro"
PROP_CENTER_NOMBRE = "nombre"
PROP_CENTER_CIUDAD = "ciudad"
PROP_CENTER_CAPACIDAD = "capacidad"
PROP_CENTER_ACTIVO = "activo"
PROP_CENTER_TIPO = "tipo"

# Propiedades usadas en relaciones
PROP_REL_FECHA = "fecha"
PROP_REL_COSTO = "costo"
PROP_REL_CANTIDAD = "cantidad"
PROP_REL_PRIORIDAD = "prioridad"
PROP_REL_ESTADO = "estado"
PROP_REL_FECHA_LLEGADA = "fecha_llegada"
PROP_REL_TIEMPO_REAL = "tiempo_real"
PROP_REL_TIEMPO_ESTIMADO = "tiempo_estimado"
PROP_REL_RESPONSABLE = "responsable"
PROP_REL_TIPO_REQUERIDO = "tipo_requerido"
PROP_REL_TEMPERATURA = "temperatura"

# Índices recomendados
INDEXES = [
    (LABEL_SUPPLIER, PROP_SUPPLIER_ID),
    (LABEL_PRODUCT, PROP_PRODUCT_ID),
    (LABEL_ORDER, PROP_ORDER_ID),
    (LABEL_INVENTORY, PROP_INVENTORY_ID),
    (LABEL_DISTRIBUTION_CENTER, PROP_CENTER_ID),
]
