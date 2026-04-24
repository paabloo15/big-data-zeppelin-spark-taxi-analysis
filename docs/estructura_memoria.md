# Estructura propuesta de memoria (aprox. 20 paginas)

## Objetivo de este documento
Proponer una guia de redaccion para la memoria academica sin escribir la memoria final completa.

## Distribucion sugerida

| Seccion | Paginas aprox. | Contenido recomendado |
|---|---:|---|
| 1. Introduccion | 1.5 | Contexto Big Data, problema, objetivos y alcance del trabajo |
| 2. Fundamentos teoricos | 2.0 | Spark, Zeppelin, DataFrames, Spark SQL, Parquet, procesamiento distribuido |
| 3. Dataset y contexto de datos | 1.5 | Fuente NYC TLC, columnas usadas, limites y supuestos |
| 4. Arquitectura tecnica | 2.0 | Docker Compose, flujo de datos, carpetas del repositorio, decisiones de diseno |
| 5. ETL y calidad del dato | 3.0 | Descarga, limpieza, transformaciones, reglas aplicadas, justificacion de umbrales |
| 6. Analisis temporal | 2.0 | Viajes por hora/dia, duracion media, tarifa media, interpretacion |
| 7. Analisis geografico y economico | 2.0 | Join con lookup, top zonas, pares OD, propinas y costes |
| 8. Comparativa de rendimiento | 1.5 | Metodologia didactica Parquet vs CSV, metricas y discusion de resultados |
| 9. Visualizacion y dashboard final | 1.0 | Seleccion de graficos y narrativa de defensa |
| 10. Manual de uso y despliegue | 1.0 | Como ejecutar el proyecto paso a paso |
| 11. Conclusiones y trabajo futuro | 1.0 | Logros, limitaciones en local, escalado a cluster real |
| 12. Referencias y uso de IA | 1.5 | Bibliografia, fuentes tecnicas, declaracion de uso de IA |

Total estimado: ~20 paginas.

## Detalle por seccion

### 1. Introduccion
- Problema que se aborda.
- Motivacion academica y tecnica.
- Objetivos generales y especificos.

### 2. Fundamentos teoricos
- Que es Big Data y por que Spark.
- Que aporta Zeppelin en analitica exploratoria.
- Diferencia entre CSV y Parquet para analitica.

### 3. Dataset
- Fuente oficial y licenciamiento.
- Columnas seleccionadas y razon.
- Riesgos de calidad de datos.

### 4. Arquitectura
- Diagrama de componentes local.
- Flujo desde `data/raw` hasta `results`.
- Decisiones de simplificacion para entorno docente.

### 5. ETL
- Script de descarga.
- Reglas de limpieza (fechas, duracion, distancia, importes, velocidad).
- Nuevas columnas derivadas.
- Resumen de limpieza.

### 6-7. Analisis
- Temporal: horas punta y comportamiento semanal.
- Geografico/economico: zonas top, coste, propina.

### 8. Comparativa
- Metodologia y limites del benchmark didactico.
- Tabla de tiempos y discusion critica.

### 9. Visualizacion
- Graficos elegidos y por que son relevantes.
- Dashboard final para defensa.

### 10. Manual
- Pasos de ejecucion reproducibles.
- Problemas comunes y soluciones.

### 11. Conclusiones
- Valor tecnico del enfoque.
- Limitaciones de entorno local.
- Propuesta de escalado a cluster real.

### 12. Referencias y uso IA
- Referencias formales (APA/IEEE segun norma docente).
- Declaracion transparente de apoyo con IA.

## TODO
- TODO: anadir capturas reales de Zeppelin en secciones 6, 7 y 9.
- TODO: completar tablas con resultados reales tras ejecucion local.
