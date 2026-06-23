# Vehicles Explorer

Este proyecto es una aplicación web hecha con **Streamlit** que explora un conjunto de datos de anuncios de vehículos usados en Estados Unidos (`vehicles_us.csv`).

### ¿Qué hace la app?

- Permite filtrar los vehículos por:
  - Año del modelo  
  - Rango de precio  
  - Rango de kilometraje  
  - Condición  
  - Tipo de vehículo  
  - Tipo de combustible  

- Muestra:
  - Histograma de la **distribución de precios**  
  - Histograma de la **distribución de kilometraje**  
  - Gráfico de dispersión **kilometraje vs precio**, coloreado por condición  
  - Tabla interactiva con los datos filtrados  
  - Tablas con:
    - Top 5 vehículos más caros  
    - Top 5 vehículos más económicos  
    - Top 5 vehículos eléctricos (si existen en el dataset)

### Cómo correr la app localmente

```bash
conda activate vehicles_env
streamlit run app.py
