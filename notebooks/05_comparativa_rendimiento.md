# 05 - Comparativa de rendimiento (Parquet vs CSV)

## Objetivo
Comparar de forma didactica tiempos de lectura y consultas agregadas entre Parquet y CSV.

## Explicacion breve
No se busca un benchmark cientifico perfecto, sino evidenciar con rigor academico por que Parquet suele rendir mejor en analitica distribuida.

## Celdas sugeridas

### Celda 1 - Carga de librerias y rutas
```python
%pyspark
import time
from pyspark.sql import functions as F

parquet_path = "/opt/project/data/processed/clean_taxi_trips.parquet"
csv_path = "/opt/project/data/processed/sample_taxi_trips.csv"
```

### Celda 2 - Medir tiempo de lectura
```python
%pyspark
start = time.perf_counter()
parquet_df = spark.read.parquet(parquet_path)
parquet_df.count()
parquet_read_time = time.perf_counter() - start

start = time.perf_counter()
csv_df = spark.read.option("header", True).option("inferSchema", True).csv(csv_path)
csv_df.count()
csv_read_time = time.perf_counter() - start

print(f"Lectura Parquet (s): {parquet_read_time:.4f}")
print(f"Lectura CSV (s): {csv_read_time:.4f}")
```

### Celda 3 - Preparar DataFrames comparables
```python
%pyspark
parquet_base = parquet_df.select("pickup_hour", "fare_amount", "trip_duration_minutes")
csv_base = csv_df.select("pickup_hour", "fare_amount", "trip_duration_minutes")

base_rows = min(parquet_base.count(), csv_base.count())
parquet_base = parquet_base.limit(base_rows).cache()
csv_base = csv_base.limit(base_rows).cache()

parquet_base.count()
csv_base.count()
print(f"Filas usadas en comparativa: {base_rows}")
```

### Celda 4 - Medir consultas agregadas
```python
%pyspark
def measure_query(df, name):
    t0 = time.perf_counter()
    if name == "numero_total_viajes":
        out = df.agg(F.count("*").alias("total"))
    elif name == "viajes_por_hora":
        out = df.groupBy("pickup_hour").count().orderBy("pickup_hour")
    elif name == "tarifa_media_por_hora":
        out = df.groupBy("pickup_hour").agg(F.avg("fare_amount").alias("fare_media")).orderBy("pickup_hour")
    elif name == "duracion_media_por_hora":
        out = df.groupBy("pickup_hour").agg(F.avg("trip_duration_minutes").alias("duracion_media")).orderBy("pickup_hour")
    else:
        raise ValueError("Consulta no soportada")

    out.count()
    return time.perf_counter() - t0

queries = [
    "numero_total_viajes",
    "viajes_por_hora",
    "tarifa_media_por_hora",
    "duracion_media_por_hora",
]

for q in queries:
    p_time = measure_query(parquet_base, q)
    c_time = measure_query(csv_base, q)
    print(f"{q} | parquet={p_time:.4f}s | csv={c_time:.4f}s")
```

## Consultas principales
- Numero total de viajes.
- Viajes por hora.
- Tarifa media por hora.
- Duracion media por hora.

## Grafico recomendado
- Tabla comparativa final de tiempos por consulta y formato.
- Barras agrupadas `parquet vs csv` por consulta.

## Resultado a comentar
- Explicar por que Parquet suele reducir tiempo de I/O en analitica.
- Mencionar sesgos: cache, tamano de muestra, hardware local.
- Estado esperado: pendiente de ejecutar en entorno local.

## TODO
- TODO: repetir consultas al menos 3 veces y comentar variabilidad de tiempos.
