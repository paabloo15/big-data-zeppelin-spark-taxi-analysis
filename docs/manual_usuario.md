# Manual de usuario

## 1. Proposito
Este manual describe como usar el proyecto desde el punto de vista de una persona usuaria del sistema analitico (sin entrar en implementacion profunda).

## 2. Flujo de uso recomendado
1. Levantar Zeppelin con Docker.
2. Descargar datos NYC TLC (meses seleccionados).
3. Ejecutar limpieza y transformacion.
4. Generar muestra CSV para comparativa.
5. Ejecutar benchmark didactico.
6. Abrir Zeppelin y ejecutar notebooks en orden.

## 3. Arranque rapido
Desde la raiz del proyecto:
```bash
docker compose up -d
```

Abrir Zeppelin en navegador:
- `http://localhost:8080`

## 4. Descarga de datos
Ejemplo para 2023 meses 1, 2 y 3:
```bash
docker compose exec zeppelin python /opt/project/scripts/download_data.py --year 2023 --months 1 2 3
```

Salida esperada:
- Ficheros `yellow_tripdata_YYYY-MM.parquet` en `data/raw/`.

## 5. Preparacion de datos
```bash
docker compose exec zeppelin spark-submit /opt/project/scripts/prepare_data.py
```

Salida esperada:
- `data/processed/clean_taxi_trips.parquet`
- `results/resumen_limpieza.csv`

## 6. Conversion de muestra a CSV
```bash
docker compose exec zeppelin spark-submit /opt/project/scripts/convert_sample_to_csv.py --sample-ratio 0.05 --sample-size 200000
```

Salida esperada:
- `data/processed/sample_taxi_trips.csv`

## 7. Benchmark de consultas
```bash
docker compose exec zeppelin spark-submit /opt/project/scripts/benchmark_queries.py
```

Salida esperada:
- `results/metricas_consultas.csv`

## 8. Ejecucion de notebooks en Zeppelin
Orden recomendado:
1. `notebooks/01_carga_datos.md`
2. `notebooks/02_limpieza_transformacion.md`
3. `notebooks/03_analisis_temporal.md`
4. `notebooks/04_analisis_geografico_economico.md`
5. `notebooks/05_comparativa_rendimiento.md`
6. `notebooks/06_dashboard_final.md`

Nota:
- Estos `.md` son guiones. Se deben copiar/adaptar en notebooks reales de Zeppelin.

## 9. Interpretacion basica de resultados
- `resumen_limpieza.csv`: cuantifica impacto de limpieza (filas iniciales/finales).
- `metricas_consultas.csv`: tiempos de consultas para comparativa Parquet vs CSV.
- Graficos Zeppelin: patrones de movilidad por hora/dia y concentracion por zona.

## 10. TODOs de usuario
- TODO: descargar `taxi_zone_lookup.csv` en `data/lookup/` para analisis geografico completo.
- TODO: validar en equipo si los meses elegidos representan bien el periodo de estudio.
- TODO: revisar y comentar resultados reales antes de la defensa.
