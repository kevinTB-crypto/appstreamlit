import streamlit as st
import pandas as pd

st.set_page_config(page_title="Panadería Marcos", page_icon="🍞", layout="wide")

# Productos
productos = [
    {"nombre": "Bolillo", "precio": 3},
    {"nombre": "Concha", "precio": 8},
    {"nombre": "Cuernito", "precio": 10},
    {"nombre": "Pastel", "precio": 180},
    {"nombre": "Dona", "precio": 12},
]

# Carrito en memoria
if "carrito" not in st.session_state:
    st.session_state.carrito = []

st.title("🍞 Panadería Marcos")
st.subheader("Sistema de Ventas")

col1, col2 = st.columns([2,1])

# Productos
with col1:
    st.header("Productos")

    for p in productos:
        c1, c2, c3 = st.columns([3,2,1])

        c1.write(p["nombre"])
        c2.write(f"$ {p['precio']}")

        if c3.button("Agregar", key=p["nombre"]):
            st.session_state.carrito.append(p)

# Carrito
with col2:
    st.header("🛒 Carrito")

    total = 0

    for item in st.session_state.carrito:
        st.write(f"{item['nombre']} - $ {item['precio']}")
        total += item["precio"]

    st.subheader(f"Total: $ {total}")

    if st.button("Comprar"):
        st.success("Compra realizada con éxito")
        st.session_state.carrito = []