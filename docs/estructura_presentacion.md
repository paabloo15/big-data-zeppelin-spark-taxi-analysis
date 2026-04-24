# Estructura propuesta de presentacion (15 minutos)

## Objetivo
Proponer una presentacion breve, tecnica y defendible para exponer el proyecto en 15 minutos.

## Configuracion sugerida
- Numero total de diapositivas: 12.
- Duracion total estimada: 15 minutos.
- Reparto por seccion: contexto, arquitectura, ETL, analisis, comparativa, conclusiones y demo.

## Guion por diapositiva

| # | Titulo | Tiempo aprox. | Contenido clave | Captura/grafico sugerido |
|---:|---|---:|---|---|
| 1 | Portada | 0:45 | Titulo, asignatura, equipo, alcance | Portada limpia |
| 2 | Problema y objetivos | 1:00 | Que se quiere resolver y por que | Diagrama simple de flujo |
| 3 | Stack tecnologico | 1:00 | Spark, Zeppelin, Docker, Parquet | Tabla de tecnologias |
| 4 | Dataset NYC TLC | 1:15 | Fuente, volumen, columnas clave | Tabla de columnas |
| 5 | Arquitectura del proyecto | 1:30 | Estructura repo y pipeline | Esquema de arquitectura |
| 6 | ETL y limpieza | 1:30 | Reglas de limpieza y columnas derivadas | Fragmento de script + resumen limpieza |
| 7 | Analisis temporal | 1:30 | Viajes por hora y dia, horas punta | Grafico viajes por hora |
| 8 | Analisis geografico/economico | 1:30 | Top zonas, propina por pago, coste medio | Top zonas y tabla propinas |
| 9 | Comparativa Parquet vs CSV | 1:15 | Metodologia didactica y resultados | Tabla/ barras de tiempos |
| 10 | Limitaciones y escalado | 1:00 | Limites local, como migrar a cluster real | Lista de mejoras futuras |
| 11 | Demo rapida en Zeppelin | 1:45 | Recorrido del dashboard final | Captura del notebook final |
| 12 | Conclusiones y preguntas | 1:00 | Aprendizajes, valor tecnico, cierre | Slide final con bullets |

Total aproximado: 15:00 min.

## Que decir durante la demo
- Mostrar primero KPI general (`total_viajes`).
- Enseñar patron temporal (horas punta).
- Enseñar un hallazgo geografico (zona top o par OD top).
- Cerrar con comparativa Parquet vs CSV y mensaje de valor tecnico.

## Capturas o graficos recomendados
- Pipeline completo (desde raw hasta resultados).
- Esquema de Spark DataFrame limpio.
- Viajes por hora.
- Top zonas de recogida.
- Tabla de benchmark.

## TODO
- TODO: sustituir capturas de ejemplo por capturas reales del entorno local del grupo.
- TODO: ajustar tiempos tras un ensayo completo cronometrado.
