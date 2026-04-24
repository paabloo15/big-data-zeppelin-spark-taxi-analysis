# 06 - Dashboard final para defensa

## Objetivo
Preparar un notebook final orientado a demo rapida (defensa oral y video de 1 minuto) con las consultas y graficos mas representativos.

## Explicacion breve
Este notebook no introduce transformaciones nuevas. Resume resultados clave y narrativa tecnica para justificar decisiones de arquitectura, limpieza y analitica.

## Estructura sugerida del dashboard

### Bloque 1 - Contexto y alcance
- Que datos se usan (Yellow Taxi, meses seleccionados).
- Que pipeline se ejecuto (descarga, limpieza, analisis, benchmark).
- Que limitaciones tiene el entorno local.

### Bloque 2 - KPIs base
```sql
%sql
SELECT COUNT(*) AS total_viajes
FROM trips_clean
```

```sql
%sql
SELECT AVG(total_amount) AS coste_medio, AVG(trip_duration_minutes) AS duracion_media
FROM trips_clean
```

### Bloque 3 - Patrones temporales clave
```sql
%sql
SELECT pickup_hour, COUNT(*) AS total_viajes
FROM trips_clean
GROUP BY pickup_hour
ORDER BY pickup_hour
```

```sql
%sql
SELECT pickup_day_of_week, COUNT(*) AS total_viajes
FROM trips_clean
GROUP BY pickup_day_of_week
ORDER BY pickup_day_of_week
```

### Bloque 4 - Hallazgos geograficos (si hay lookup)
```sql
%sql
SELECT pu_zone, COUNT(*) AS total_viajes
FROM trips_geo
GROUP BY pu_zone
ORDER BY total_viajes DESC
LIMIT 10
```

### Bloque 5 - Comparativa Parquet vs CSV
- Mostrar tabla de `results/metricas_consultas.csv` (pendiente de ejecutar).
- Explicar que es comparativa didactica, no benchmark cientifico.

## Graficos que conviene mostrar
- Viajes por hora (linea o barras).
- Top 10 zonas de recogida (barras horizontales).
- Tabla de tiempos Parquet vs CSV.

## Guion de demo de 1 minuto (orientativo)
1. 0:00-0:10: problema y dataset.
2. 0:10-0:20: arquitectura Spark + Zeppelin en local.
3. 0:20-0:35: limpieza y calidad del dato.
4. 0:35-0:50: hallazgos temporales/geograficos.
5. 0:50-1:00: comparativa Parquet vs CSV y cierre.

## Resultado a comentar
- El proyecto es reproducible en local y defendible tecnicamente.
- Queda listo para ampliar a cluster real si crece volumen o concurrencia.
- Estado esperado: pendiente de ejecutar y capturar para entrega.

## TODO
- TODO: anadir capturas reales de graficos para memoria y presentacion.
- TODO: validar tiempos del benchmark en el hardware final del grupo.
- TODO: ajustar orden narrativo segun quien presente cada bloque.
