# 01 - Carga de datos

## Objetivo
Cargar los ficheros Parquet de Yellow Taxi, inspeccionar el esquema, contar registros y obtener una muestra de filas para validar que la ingesta es correcta.

## Explicacion breve
Parquet es un formato columnar optimizado para analitica. En Spark permite leer solo columnas necesarias, aplicar compresion eficiente y reducir I/O frente a CSV.

## Celdas sugeridas

### Celda 1 - Configuracion inicial
```python
%pyspark
raw_path = "/opt/project/data/raw/yellow_tripdata_*.parquet"
print(f"Ruta de entrada: {raw_path}")
```

### Celda 2 - Carga de datos
```python
%pyspark
df_raw = spark.read.parquet(raw_path)
print("Carga completada")
```

### Celda 3 - Esquema
```python
%pyspark
df_raw.printSchema()
```

### Celda 4 - Conteo de registros
```python
%pyspark
rows = df_raw.count()
print(f"Total de registros: {rows}")
```

### Celda 5 - Muestra de filas
```python
%pyspark
df_raw.select(
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount",
    "PULocationID",
    "DOLocationID"
).show(20, truncate=False)
```

### Celda 6 - Vista SQL opcional
```python
%pyspark
df_raw.createOrReplaceTempView("yellow_raw")
```

```sql
%sql
SELECT COUNT(*) AS total_registros FROM yellow_raw
```

## Consultas principales
- Conteo total de registros.
- Revision de tipos de datos en columnas clave.
- Muestreo de filas para detectar datos atipicos iniciales.

## Grafico recomendado
- Barras: registros por mes si se cargan varios ficheros.
- Si no se extrae mes en esta fase, dejarlo para notebook 03.

## Resultado a comentar
- Confirmar que el dataset se carga sin errores.
- Explicar por que se trabaja en Parquet y no directamente en CSV.
- Estado esperado: pendiente de ejecutar en entorno local.

## TODO
- TODO: ajustar anios y meses reales que se van a analizar en la entrega.
