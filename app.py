import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Vehicles Explorer", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("vehicles_us.csv")

df = load_data()

st.title(" Vehicles Explorer ")

st.markdown(
    "Explora anuncios de vehículos usados en Estados Unidos. "
    "Puedes filtrar por año, precio, kilometraje, tipo, condición y combustible."
)
st.sidebar.header("Filtros")

# rango de año del modelo
year_min = int(df["model_year"].min())
year_max = int(df["model_year"].max())
year_range = st.sidebar.slider(
    "Año del modelo",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max),
)

# rango de precio
price_min = int(df["price"].min())
price_max = int(df["price"].max())
price_range = st.sidebar.slider(
    "Rango de precio ($)",
    min_value=price_min,
    max_value=price_max,
    value=(price_min, price_max),
    step=1000,
)

# rango de kilometraje (odometer)
odo_min = int(df["odometer"].min())
odo_max = int(df["odometer"].max())
odo_range = st.sidebar.slider(
    "Rango de kilometraje",
    min_value=odo_min,
    max_value=odo_max,
    value=(odo_min, odo_max),
    step=10000,
)

# condición
conditions = sorted(df["condition"].dropna().unique())
cond_filter = st.sidebar.multiselect(
    "Condición",
    options=conditions,
    default=conditions,
)

# tipo de vehículo
types = sorted(df["type"].dropna().unique())
type_filter = st.sidebar.multiselect(
    "Tipo de vehículo",
    options=types,
    default=types,
)

# combustible
fuels = sorted(df["fuel"].dropna().unique())
fuel_filter = st.sidebar.multiselect(
    "Combustible",
    options=fuels,
    default=fuels,
)

filtered = df[
    (df["model_year"].between(year_range[0], year_range[1])) &
    (df["price"].between(price_range[0], price_range[1])) &
    (df["odometer"].between(odo_range[0], odo_range[1])) &
    (df["condition"].isin(cond_filter)) &
    (df["type"].isin(type_filter)) &
    (df["fuel"].isin(fuel_filter))
].copy()

st.caption(f"Resultados filtrados: **{len(filtered)}** vehículos.")

c1, c2 = st.columns(2)

# -------- Histograma de precios --------
with c1:
    st.subheader("Distribución de precios")
    fig_price = px.histogram(
        filtered,
        x="price",
        nbins=40,
        labels={"price": "Precio ($ USD)"},
    )
    fig_price.update_layout(
        xaxis_title="Precio ($ USD)",
        yaxis_title="Número de vehículos",
        xaxis_tickprefix="$",
    )
    st.plotly_chart(fig_price, use_container_width=True)

# -------- Histograma de kilometraje --------
with c2:
    st.subheader("Distribución de kilometraje")
    fig_odo = px.histogram(
        filtered,
        x="odometer",
        nbins=40,
        labels={"odometer": "Kilometraje (millas)"},
    )
    fig_odo.update_layout(
        xaxis_title="Kilometraje (millas)",
        yaxis_title="Número de vehículos",
    )
    st.plotly_chart(fig_odo, use_container_width=True)

# -------- Scatter: kilometraje vs precio --------
st.subheader("Relación kilometraje vs precio")

color_col = "condition" if "condition" in filtered.columns else None

fig_scatter = px.scatter(
    filtered,
    x="odometer",
    y="price",
    color=color_col,
    hover_data=["model", "model_year"],
    labels={"odometer": "Kilometraje (millas)", "price": "Precio ($ USD)"},
)
fig_scatter.update_layout(
    xaxis_title="Kilometraje (millas)",
    yaxis_title="Precio ($ USD)",
    yaxis_tickprefix="$",
)
st.plotly_chart(fig_scatter, use_container_width=True)


st.subheader("Vista de datos filtrados")

max_rows = st.slider(
    "Número de filas a mostrar",
    min_value=50,
    max_value=1000,
    value=200,
    step=50,
)

st.dataframe(filtered.head(max_rows))

st.header("🏆 Vehículos destacados (dataset completo)")

# usamos el df completo, no solo filtrado
top_expensive = df.nlargest(5, "price")
top_cheap = df.nsmallest(5, "price")
electric_cars = df[df["fuel"] == "electric"]

if not electric_cars.empty:
    top_electric = electric_cars.nlargest(5, "price")
else:
    top_electric = pd.DataFrame()  # vacío

cols_to_show = ["price", "model_year", "model", "condition", "odometer", "fuel"]

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.subheader("Top 5 más caros")
    st.dataframe(top_expensive[cols_to_show])

with col_b:
    st.subheader("Top 5 más económicos")
    st.dataframe(top_cheap[cols_to_show])

with col_c:
    st.subheader("Top 5 eléctricos")
    if top_electric.empty:
        st.write("No hay vehículos eléctricos en el conjunto de datos.")
    else:
        st.dataframe(top_electric[cols_to_show])
