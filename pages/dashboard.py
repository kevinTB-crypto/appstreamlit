import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# ---------------------------------
# CONFIGURACION PAGINA
# ---------------------------------
st.set_page_config(
    page_title="Dashboard Ventas",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------
# SESION LOGIN
# ---------------------------------
if "login_admin" not in st.session_state:
    st.session_state.login_admin = False

# ---------------------------------
# LOGIN ADMINISTRADOR
# ---------------------------------
if not st.session_state.login_admin:

    st.title("🔐 Acceso Administrador")
    st.caption("Panel privado - Panadería Marcos")

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):

        if usuario == "admin" and password == "1234":
            st.session_state.login_admin = True
            st.success("Acceso concedido")
            st.rerun()

        else:
            st.error("Usuario o contraseña incorrectos")

    st.stop()

# ---------------------------------
# BOTON CERRAR SESION
# ---------------------------------
col1, col2 = st.columns([6,1])

with col2:
    if st.button("🚪 Salir"):
        st.session_state.login_admin = False
        st.rerun()

# ---------------------------------
# CONEXION BASE DE DATOS
# ---------------------------------
conn = sqlite3.connect("panaderia.db")

# TABLA VENTAS
ventas = pd.read_sql_query(
    "SELECT * FROM ventas ORDER BY id DESC",
    conn
)

# TABLA DETALLE
detalle = pd.read_sql_query(
    "SELECT * FROM detalle_venta",
    conn
)

# ---------------------------------
# TITULO
# ---------------------------------
st.title("📊 Dashboard Administrativo")
st.caption("Bienvenido Administrador")

# ---------------------------------
# SI NO HAY DATOS
# ---------------------------------
if ventas.empty:
    st.warning("No hay ventas registradas todavía.")
    st.stop()

# ---------------------------------
# INDICADORES
# ---------------------------------
total_vendido = ventas["total"].sum()
cantidad_ventas = len(ventas)
ticket_promedio = ventas["total"].mean()

c1, c2, c3 = st.columns(3)

c1.metric("💰 Total Vendido", f"$ {total_vendido:,.2f}")
c2.metric("🧾 Ventas Realizadas", cantidad_ventas)
c3.metric("📈 Ticket Promedio", f"$ {ticket_promedio:,.2f}")

st.divider()

# ---------------------------------
# HISTORIAL
# ---------------------------------
st.subheader("📋 Historial de Ventas")

st.dataframe(
    ventas,
    use_container_width=True
)

st.divider()

# ---------------------------------
# GRAFICA BARRAS
# ---------------------------------
st.subheader("📈 Ventas por Operación")

fig = px.bar(
    ventas,
    x="id",
    y="total",
    title="Monto por Venta",
    text_auto=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ---------------------------------
# PRODUCTOS MAS VENDIDOS
# ---------------------------------
if not detalle.empty:

    top = (
        detalle.groupby("producto")["cantidad"]
        .sum()
        .reset_index()
        .sort_values("cantidad", ascending=False)
    )

    st.subheader("🥇 Productos Más Vendidos")

    fig2 = px.pie(
        top,
        names="producto",
        values="cantidad",
        hole=0.4
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ---------------------------------
# CERRAR CONEXION
# ---------------------------------
conn.close()