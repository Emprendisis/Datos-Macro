
import streamlit as st
import wbdata
import pandas as pd
import requests
import datetime

st.set_page_config(page_title="Explorador de Indicadores del Banco Mundial", layout="centered")
st.title("🌍 Explorador de Indicadores del Banco Mundial")

st.markdown("### 🧭 Ingresa el nombre o código ISO del país (por ejemplo: Mexico o MEX):")
pais_input = st.text_input("", "Mexico")

def obtener_codigos_paises():
    url = "http://api.worldbank.org/v2/country?format=json&per_page=500"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("No se pudo obtener la lista de países.")
    data = response.json()[1]
    return {pais["name"]: pais["id"] for pais in data}

try:
    paises = obtener_codigos_paises()
    if pais_input.upper() in paises.values():
        codigo_pais = pais_input.upper()
    else:
        codigo_pais = paises.get(pais_input.capitalize(), None)

    if codigo_pais:
        indicadores = wbdata.get_indicator(source=2)  # Banco Mundial data source
        st.subheader(f"📈 Indicadores disponibles para {pais_input.title()}")
        for k, v in indicadores.items():
            st.markdown(f"- **{v}** (`{k}`)")
    else:
        st.error("❌ No se encontró el país en la base del Banco Mundial.")
except Exception as e:
    st.error(f"❌ Error al consultar el Banco Mundial: {e}")
