# Manual de despliegue

## 1. Alcance
Este documento describe el despliegue local del entorno Spark + Zeppelin para el proyecto.

## 2. Requisitos previos
- Docker Desktop instalado y activo.
- Docker Compose v2.
- Puertos libres: `8080` (Zeppelin) y `4040` (Spark UI).
- Espacio en disco suficiente para datos Parquet descargados.

Opcional (si se ejecuta sin Docker):
- Python 3.10+.
- Java 11 o 17.
- Dependencias de `requirements.txt`.

## 3. Arranque con Docker Compose (opcion principal)
Desde la raiz del proyecto:
```bash
docker compose up -d
```

Verificar estado:
```bash
docker compose ps
```

Acceder a Zeppelin:
- `http://localhost:8080`

## 4. Comandos operativos utiles
Parar servicios:
```bash
docker compose down
```

Ver logs de Zeppelin:
```bash
docker compose logs -f zeppelin
```

Ejecutar scripts dentro del contenedor:
```bash
docker compose exec zeppelin python /opt/project/scripts/download_data.py --year 2023 --months 1 2 3

docker compose exec zeppelin spark-submit /opt/project/scripts/prepare_data.py

docker compose exec zeppelin spark-submit /opt/project/scripts/convert_sample_to_csv.py

docker compose exec zeppelin spark-submit /opt/project/scripts/benchmark_queries.py
```

## 5. Problemas frecuentes y solucion
1. Puerto 8080 ocupado.
- Cambiar mapeo en `docker-compose.yml`, por ejemplo `18080:8080`.

2. Error de memoria al limpiar datos.
- Reducir cantidad de meses.
- Aumentar memoria asignada a Docker Desktop.

3. Benchmark falla por falta de CSV.
- Ejecutar primero `convert_sample_to_csv.py`.

4. Analisis geografico incompleto.
- Falta `taxi_zone_lookup.csv`.
- Descargarlo manualmente en `data/lookup/`.

## 6. Alternativa sin Docker (viable pero secundaria)
Pasos:
1. Crear entorno virtual Python.
2. Instalar dependencias con `pip install -r requirements.txt`.
3. Verificar Java y Spark local.
4. Ejecutar scripts desde terminal local.
5. Usar Zeppelin local o Jupyter como alternativa de exploracion.

Limitacion:
- Mayor variabilidad de entorno entre miembros del equipo.

## 7. TODOs de despliegue
- TODO: acordar configuracion minima de RAM para todos los equipos del grupo.
- TODO: validar comandos en el hardware final antes de grabar demo.
