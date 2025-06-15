
import streamlit as st
import wbdata
import pandas as pd
import datetime

# Título
st.title("🌍 Explorador de Indicadores Macroeconómicos")

# Selección de la fuente de datos (solo World Bank habilitado)
fuente = st.selectbox("Selecciona la fuente de datos:", ["World Bank"])

# Carga dinámica de países desde el World Bank
paises = wbdata.get_country()
paises_dict = {pais['name']: pais['id'] for pais in paises}
pais_nombre = st.selectbox("🌐 Selecciona el país:", list(paises_dict.keys()))
pais_codigo = paises_dict[pais_nombre]

# Diccionario de indicadores (puedes expandirlo)
indicadores = {
    "PIB (USD)": "NY.GDP.MKTP.CD",
    "PIB PPA (USD)": "NY.GDP.MKTP.PP.CD",
    "Inflación (%)": "FP.CPI.TOTL.ZG",
    "Desempleo (%)": "SL.UEM.TOTL.ZS",
    "Deuda externa total (USD)": "DT.DOD.DECT.CD",
    "Deuda (% PIB)": "GC.DOD.TOTL.GD.ZS",
    "Balanza comercial (USD)": "NE.EXP.GNFS.CD",
    "Balanza comercial (% PIB)": "NE.EXP.GNFS.ZS",
    "Crecimiento del PIB (%)": "NY.GDP.MKTP.KD.ZG",
    "Prima de riesgo país": "FR.INR.RISK"
}
indicador_nombre = st.selectbox("📊 Selecciona el indicador:", list(indicadores.keys()))
indicador_codigo = indicadores[indicador_nombre]

# Selección de rango de años
año_inicio = st.slider("Año de inicio", 2000, 2023, 2010)
año_fin = st.slider("Año de fin", año_inicio + 1, 2024, 2023)

# Botón de consulta
if st.button("🔍 Consultar"):
    try:
        fecha_inicio = datetime.datetime(año_inicio, 1, 1)
        fecha_fin = datetime.datetime(año_fin, 1, 1)
        df = wbdata.get_dataframe({indicador_codigo: indicador_nombre}, country=pais_codigo,
                                  data_date=(fecha_inicio, fecha_fin), convert_date=True)
        df = df.reset_index().sort_values(by="date")
        st.line_chart(df.set_index("date")[indicador_nombre])
        st.dataframe(df)

        # Exportar a Excel
        archivo = f"{pais_codigo}_{indicador_codigo}_{año_inicio}_{año_fin}.xlsx"
        df.to_excel(archivo, index=False)
        with open(archivo, "rb") as f:
            st.download_button("📥 Descargar Excel", f, file_name=archivo)

    except Exception as e:
        st.error(f"❌ Error al obtener los datos: {e}")
