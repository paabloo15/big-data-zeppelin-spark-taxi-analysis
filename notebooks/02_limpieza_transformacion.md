# 02 - Limpieza y transformacion

## Objetivo
Aplicar reglas de calidad de datos, eliminar registros invalidos y crear variables derivadas para analisis temporal y economico.

## Explicacion breve
Esta fase convierte datos crudos en datos analiticos confiables. Las reglas usadas deben ser explicitadas en defensa para justificar por que se eliminan ciertos viajes.

## Celdas sugeridas

### Celda 1 - Carga de datos crudos
```python
%pyspark
from pyspark.sql import functions as F

raw_path = "/opt/project/data/raw/yellow_tripdata_*.parquet"
df = spark.read.parquet(raw_path)
print(f"Registros iniciales: {df.count()}")
```

### Celda 2 - Deteccion de nulos en columnas criticas
```python
%pyspark
nulls = df.select(
    F.sum(F.col("tpep_pickup_datetime").isNull().cast("int")).alias("pickup_nulls"),
    F.sum(F.col("tpep_dropoff_datetime").isNull().cast("int")).alias("dropoff_nulls"),
    F.sum(F.col("trip_distance").isNull().cast("int")).alias("distance_nulls"),
    F.sum(F.col("total_amount").isNull().cast("int")).alias("total_amount_nulls")
)
nulls.show()
```

### Celda 3 - Columnas derivadas (duracion y velocidad)
```python
%pyspark
df2 = (
    df.withColumn(
        "trip_duration_minutes",
        (F.unix_timestamp("tpep_dropoff_datetime") - F.unix_timestamp("tpep_pickup_datetime")) / 60.0
    )
    .withColumn("average_speed_mph", F.col("trip_distance") / (F.col("trip_duration_minutes") / 60.0))
)
```

### Celda 4 - Limpieza de registros invalidos
```python
%pyspark
max_duration_minutes = 240
max_speed_mph = 80

clean = (
    df2.where(F.col("tpep_pickup_datetime").isNotNull())
       .where(F.col("tpep_dropoff_datetime").isNotNull())
       .where(F.col("trip_duration_minutes") > 0)
       .where(F.col("trip_duration_minutes") <= max_duration_minutes)
       .where(F.col("trip_distance") > 0)
       .where(F.col("fare_amount") >= 0)
       .where(F.col("tip_amount") >= 0)
       .where(F.col("total_amount") >= 0)
       .where(F.col("average_speed_mph") > 0)
       .where(F.col("average_speed_mph") <= max_speed_mph)
       .withColumn("pickup_date", F.to_date("tpep_pickup_datetime"))
       .withColumn("pickup_hour", F.hour("tpep_pickup_datetime"))
       .withColumn("pickup_day_of_week", F.dayofweek("tpep_pickup_datetime"))
)

print(f"Registros finales: {clean.count()}")
```

### Celda 5 - Guardado del dataset limpio
```python
%pyspark
output_path = "/opt/project/data/processed/clean_taxi_trips.parquet"
clean.write.mode("overwrite").parquet(output_path)
print(f"Dataset limpio guardado en: {output_path}")
```

## Consultas principales
- Numero de nulos por columna critica.
- Registros iniciales vs finales tras limpieza.
- Distribucion basica de duracion y velocidad tras filtros.

## Grafico recomendado
- Barras: antes vs despues de limpieza.
- Histograma: `trip_duration_minutes` y `average_speed_mph` tras limpieza.

## Resultado a comentar
- Justificar reglas de limpieza y su impacto porcentual.
- Explicar que limpiar no es "perder datos", sino controlar calidad analitica.
- Estado esperado: pendiente de ejecutar en entorno local.

## TODO
- TODO: validar umbrales (`max_duration_minutes`, `max_speed_mph`) con el profesor si se requiere otro criterio.
