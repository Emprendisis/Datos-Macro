import streamlit as st
import requests
import pandas as pd
import wbdata
import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Indicadores Macroeconómicos Mundiales", layout="centered")
st.title("📊 Consulta de Indicadores Macroeconómicos Mundiales")
st.markdown("Consulta indicadores macroeconómicos oficiales del Banco Mundial y expórtalos a Excel.")

# --- OBTENER LISTA DE PAÍSES DESDE API DEL WORLD BANK ---
@st.cache_data
def obtener_paises_wb():
    url = "http://api.worldbank.org/v2/country?format=json&per_page=300"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()[1]
        return {item['name']: item['id'] for item in data if item['region']['value'] != 'Aggregates'}
    else:
        return {}

paises_dict = obtener_paises_wb()
pais_nombre = st.selectbox("🌍 Selecciona un país", list(paises_dict.keys()))
pais_codigo = paises_dict[pais_nombre]

# --- SELECCIÓN DE RANGO DE AÑOS ---
anio_inicio, anio_fin = st.select_slider(
    "📅 Selecciona el rango de años",
    options=list(range(2000, datetime.datetime.now().year + 1)),
    value=(2010, 2024)
)

# --- INDICADORES DISPONIBLES Y SUS CÓDIGOS WB ---
indicadores = {
    "Deuda total (USD)": "DT.DOD.DECT.CD",
    "Deuda total (% del PIB)": "GC.DOD.TOTL.GD.ZS",
    "PIB (USD)": "NY.GDP.MKTP.CD",
    "Balanza comercial (USD)": "NE.RSB.GNFS.CD",
    "Balanza comercial (% del PIB)": "NE.RSB.GNFS.ZS",
    "Tasa de desempleo": "SL.UEM.TOTL.ZS",
    "Inflación (anual %)": "FP.CPI.TOTL.ZG",
    "PIB PPA (USD)": "NY.GDP.MKTP.PP.CD",
    "Crecimiento PIB (%)": "NY.GDP.MKTP.KD.ZG",
    "Prima de riesgo": "FR.INR.RISK"
}

indicador_nombre = st.selectbox("📈 Indicador", list(indicadores.keys()))
codigo_indicador = indicadores[indicador_nombre]

# --- CONSULTAR DATOS ---
if st.button("🔎 Consultar datos"):
    try:
        data = wbdata.get_dataframe({codigo_indicador: indicador_nombre}, country=pais_codigo,
                                     data_date=(datetime.datetime(anio_inicio, 1, 1), datetime.datetime(anio_fin, 12, 31)))
        if data.empty:
            st.warning("No se encontraron datos disponibles para el criterio seleccionado.")
        else:
            data = data.reset_index()
            data["date"] = pd.to_datetime(data["date"])
            data = data.sort_values("date")

            st.success(f"Datos obtenidos para {pais_nombre}: {indicador_nombre}")
            st.line_chart(data.set_index("date")[indicador_nombre])

            # Exportar a Excel
            excel_file = f"{pais_codigo}_{codigo_indicador}_{anio_inicio}_{anio_fin}.xlsx"
            data['date'] = data['date'].dt.strftime('%d/%m/%Y')
            data.to_excel(excel_file, index=False)
            with open(excel_file, "rb") as f:
                st.download_button("📥 Descargar Excel", f, file_name=excel_file)

    except Exception as e:
        st.error(f"Error: {e}")
