# 04 - Analisis geografico y economico

## Objetivo
Cruzar los viajes con zonas TLC (si existe lookup), identificar hotspots de origen/destino y analizar componentes economicos como propina y coste medio.

## Explicacion breve
El enriquecimiento geografico aporta contexto de negocio: no solo cuantos viajes hay, sino en que zonas se concentra demanda, ingresos y comportamiento de propinas.

## Celdas sugeridas

### Celda 1 - Carga de datos limpios
```python
%pyspark
from pyspark.sql import functions as F
import os

clean_path = "/opt/project/data/processed/clean_taxi_trips.parquet"
lookup_path = "/opt/project/data/lookup/taxi_zone_lookup.csv"

trips = spark.read.parquet(clean_path)
trips.createOrReplaceTempView("trips_clean")
```

### Celda 2 - Carga de lookup de zonas (si existe)
```python
%pyspark
if os.path.exists(lookup_path):
    zones = spark.read.option("header", True).csv(lookup_path)
    zones = zones.select(
        F.col("LocationID").cast("int").alias("LocationID"),
        F.col("Borough").alias("borough"),
        F.col("Zone").alias("zone"),
        F.col("service_zone").alias("service_zone")
    )
    zones.createOrReplaceTempView("zones")
    print("Lookup cargado")
else:
    print("Lookup no encontrado. Ejecuta el TODO de descarga manual.")
```

### Celda 3 - Join de zonas de recogida y destino
```python
%pyspark
if "zones" in [t.name for t in spark.catalog.listTables()]:
    pu = zones.selectExpr("LocationID as PULocationID", "borough as pu_borough", "zone as pu_zone")
    do = zones.selectExpr("LocationID as DOLocationID", "borough as do_borough", "zone as do_zone")

    trips_geo = trips.join(pu, on="PULocationID", how="left").join(do, on="DOLocationID", how="left")
    trips_geo.createOrReplaceTempView("trips_geo")
    print("Join completado")
else:
    print("No se puede hacer join sin lookup")
```

### Celda 4 - Top zonas de recogida
```sql
%sql
SELECT pu_zone, COUNT(*) AS total_viajes
FROM trips_geo
GROUP BY pu_zone
ORDER BY total_viajes DESC
LIMIT 10
```

### Celda 5 - Top zonas de destino
```sql
%sql
SELECT do_zone, COUNT(*) AS total_viajes
FROM trips_geo
GROUP BY do_zone
ORDER BY total_viajes DESC
LIMIT 10
```

### Celda 6 - Top pares origen-destino
```sql
%sql
SELECT pu_zone, do_zone, COUNT(*) AS total_viajes
FROM trips_geo
GROUP BY pu_zone, do_zone
ORDER BY total_viajes DESC
LIMIT 10
```

### Celda 7 - Propina media por metodo de pago
```sql
%sql
SELECT payment_type, AVG(tip_amount) AS propina_media
FROM trips_clean
GROUP BY payment_type
ORDER BY payment_type
```

### Celda 8 - Coste medio por zona de recogida
```sql
%sql
SELECT pu_zone, AVG(total_amount) AS coste_medio
FROM trips_geo
GROUP BY pu_zone
ORDER BY coste_medio DESC
LIMIT 10
```

## Consultas principales
- Top zonas de recogida y destino.
- Top pares origen-destino.
- Propina media por metodo de pago.
- Coste medio por zona.

## Graficos recomendados
- Barras horizontales para top zonas.
- Tabla para top pares origen-destino.
- Barras para propina media por metodo de pago.

## Resultado a comentar
- Detectar concentraciones geografias de demanda.
- Comentar diferencias de coste/propina por zona y pago.
- Estado esperado: pendiente de ejecutar en entorno local.

## TODO
- TODO: descargar `taxi_zone_lookup.csv` y guardarlo en `data/lookup/`.
