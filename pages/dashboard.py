import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Ventas",
    page_icon="📊",
    layout="wide"
)

# Conexion
conn = sqlite3.connect("panaderia.db")

# Leer ventas
ventas = pd.read_sql_query(
    "SELECT * FROM ventas ORDER BY id DESC",
    conn
)

# Leer detalle
detalle = pd.read_sql_query(
    "SELECT * FROM detalle_venta",
    conn
)   

st.title("📊 Dashboard Administrativo")
st.caption("Panadería Marcos")

# Si no hay datos
if ventas.empty:
    st.warning("No hay ventas registradas")
    st.stop()

# KPIs
total_vendido = ventas["total"].sum()
num_ventas = len(ventas)
ticket_promedio = ventas["total"].mean()

c1, c2, c3 = st.columns(3)

c1.metric("💰 Total Vendido", f"$ {total_vendido:,.2f}")
c2.metric("🧾 Ventas", num_ventas)
c3.metric("📈 Ticket Promedio", f"$ {ticket_promedio:,.2f}")

st.divider()

# Tabla historial
st.subheader("📋 Historial de Ventas")
st.dataframe(ventas, use_container_width=True)

st.divider()

# Gráfica ventas
st.subheader("📈 Ventas por operación")

fig = px.bar(
    ventas,
    x="id",
    y="total",
    title="Ventas registradas"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Producto más vendido
if not detalle.empty:

    top = (
        detalle.groupby("producto")["cantidad"]
        .sum()
        .reset_index()
        .sort_values("cantidad", ascending=False)
    )

    st.subheader("🥇 Productos más vendidos")

    fig2 = px.pie(
        top,
        names="producto",
        values="cantidad"
    )

    st.plotly_chart(fig2, use_container_width=True)