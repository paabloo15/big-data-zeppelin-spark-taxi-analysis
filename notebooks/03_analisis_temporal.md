# 03 - Analisis temporal

## Objetivo
Analizar patrones de movilidad por hora y dia de la semana, asi como variaciones en tarifa y duracion media.

## Explicacion breve
El analisis temporal permite detectar horas punta, comportamiento semanal y cambios de coste/duracion que pueden relacionarse con congestion urbana.

## Celdas sugeridas

### Celda 1 - Carga de dataset limpio
```python
%pyspark
clean_path = "/opt/project/data/processed/clean_taxi_trips.parquet"
df = spark.read.parquet(clean_path)
df.createOrReplaceTempView("trips_clean")
```

### Celda 2 - Viajes por hora
```sql
%sql
SELECT pickup_hour, COUNT(*) AS total_viajes
FROM trips_clean
GROUP BY pickup_hour
ORDER BY pickup_hour
```

### Celda 3 - Viajes por dia de la semana
```sql
%sql
SELECT pickup_day_of_week, COUNT(*) AS total_viajes
FROM trips_clean
GROUP BY pickup_day_of_week
ORDER BY pickup_day_of_week
```

### Celda 4 - Duracion media por hora
```sql
%sql
SELECT pickup_hour, AVG(trip_duration_minutes) AS duracion_media_min
FROM trips_clean
GROUP BY pickup_hour
ORDER BY pickup_hour
```

### Celda 5 - Tarifa media por hora
```sql
%sql
SELECT pickup_hour, AVG(fare_amount) AS tarifa_media
FROM trips_clean
GROUP BY pickup_hour
ORDER BY pickup_hour
```

## Consultas principales
- Conteo de viajes por hora.
- Conteo de viajes por dia de semana.
- Duracion media por hora.
- Tarifa media por hora.

## Graficos recomendados
- Linea o barras para viajes por hora.
- Barras para viajes por dia de semana.
- Linea para duracion media por hora.
- Linea para tarifa media por hora.

## Resultado a comentar
- Identificar horas punta y horas valle.
- Comentar posibles relaciones entre pico de demanda, duracion y coste.
- Estado esperado: pendiente de ejecutar en entorno local.

## TODO
- TODO: revisar si el huso horario de procesamiento coincide con el criterio del dataset.
