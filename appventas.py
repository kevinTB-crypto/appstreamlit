import streamlit as st
from database import crear_tablas, guardar_venta
from datetime import datetime

crear_tablas()

st.set_page_config(
    page_title="Panadería Marcos",
    page_icon="🍞",
    layout="wide"
)

# CSS visual
st.markdown("""
<style>
.main {
    background-color: #fffaf4;
}
.card {
    padding: 15px;
    border-radius: 15px;
    background: white;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 12px;
}
.total {
    padding: 12px;
    border-radius: 12px;
    background: #f0f8ff;
    font-size: 22px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Productos
productos = [
    {"nombre": "Bolillo", "precio": 3},
    {"nombre": "Concha", "precio": 8},
    {"nombre": "Cuernito", "precio": 10},
    {"nombre": "Dona", "precio": 12},
    {"nombre": "Pastel", "precio": 180},
]

# Memoria carrito
if "carrito" not in st.session_state:
    st.session_state.carrito = []

st.title("🍞 Panadería Marcos")
st.caption("Sistema de ventas profesional")

col1, col2 = st.columns([2,1])

# PRODUCTOS
with col1:
    st.subheader("🥖 Productos")

    for i, p in enumerate(productos):
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)

            c1, c2, c3 = st.columns([3,2,2])

            c1.write(f"**{p['nombre']}**")
            c2.write(f"$ {p['precio']}")

            cantidad = c3.number_input(
                "Cant.",
                min_value=1,
                max_value=20,
                value=1,
                key=f"cant{i}"
            )

            if st.button("Agregar", key=f"btn{i}"):
                st.session_state.carrito.append({
                    "nombre": p["nombre"],
                    "precio": p["precio"],
                    "cantidad": cantidad
                })

            st.markdown("</div>", unsafe_allow_html=True)

# CARRITO
with col2:
    st.subheader("🛒 Carrito")

    total = 0

    for idx, item in enumerate(st.session_state.carrito):
        subtotal = item["precio"] * item["cantidad"]
        total += subtotal

        c1, c2 = st.columns([4,1])

        c1.write(
            f"{item['nombre']} x{item['cantidad']} = $ {subtotal}"
        )

        if c2.button("❌", key=f"del{idx}"):
            st.session_state.carrito.pop(idx)
            st.rerun()

    st.markdown(
        f'<div class="total">Total: $ {total}</div>',
        unsafe_allow_html=True
    )

    if st.button("Comprar"):

     if len(st.session_state.carrito) > 0:

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        guardar_venta(
            fecha,
            total,
            st.session_state.carrito
        )

        st.success("✅ Venta guardada correctamente")

        st.session_state.carrito = []
        st.rerun()

    else:
        st.warning("Carrito vacío")