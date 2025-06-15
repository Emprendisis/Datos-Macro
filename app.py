
import streamlit as st
import wbdata
import pandas as pd
import datetime

st.set_page_config(page_title="Explorador de Indicadores Macroeconómicos", layout="centered")

st.title("🌍 Explorador de Indicadores Macroeconómicos")

# Fuente de datos
fuente = st.selectbox("Selecciona la fuente de datos:", ["World Bank"])

# Función para obtener lista de países
def obtener_lista_paises():
    try:
        paises = wbdata.get_country()
        return {p['name']: p['id'] for p in paises}
    except Exception as e:
        st.error(f"No se pudo cargar la lista de países del World Bank: {e}")
        return {}

# Diccionario de indicadores
indicadores_disponibles = {
    "PIB (USD)": "NY.GDP.MKTP.CD",
    "PIB PPA (USD)": "NY.GDP.MKTP.PP.CD",
    "PIB Variación (%)": "NY.GDP.MKTP.KD.ZG",
    "Inflación (%)": "FP.CPI.TOTL.ZG",
    "Tasa de desempleo (%)": "SL.UEM.TOTL.ZS",
    "Deuda (% del PIB)": "GC.DOD.TOTL.GD.ZS",
    "Deuda total (USD)": "GC.DOD.TOTL.CN",
    "Balanza comercial (USD)": "NE.EXP.GNFS.CD",
    "Balanza comercial (% PIB)": "NE.EXP.GNFS.ZS",
    "Prima de riesgo (tasa de interés)": "FR.INR.RISK"
}

# Si es World Bank
if fuente == "World Bank":
    paises_dict = obtener_lista_paises()
    if paises_dict:
        pais = st.selectbox("🌐 Selecciona el país:", list(paises_dict.keys()))
        pais_codigo = paises_dict[pais]

        indicador_nombre = st.selectbox("📊 Selecciona el indicador:", list(indicadores_disponibles.keys()))
        indicador_codigo = indicadores_disponibles[indicador_nombre]

        # Fechas
        anio_inicio = st.slider("📅 Año de inicio", 2000, 2023, 2010)
        anio_fin = st.slider("📅 Año de fin", anio_inicio, 2024, 2023)

        if st.button("Consultar"):
            try:
                datos = wbdata.get_dataframe(
                    {indicador_nombre: indicador_codigo},
                    country=pais_codigo,
                    data_date=(datetime.datetime(anio_inicio, 1, 1), datetime.datetime(anio_fin, 12, 31)),
                    convert_date=True
                )
                if datos.empty:
                    st.warning("No se encontraron datos para los criterios seleccionados.")
                else:
                    datos = datos.reset_index()
                    st.line_chart(datos.set_index("date")[indicador_nombre])
                    st.dataframe(datos)

                    # Exportar a Excel
                    nombre_archivo = f"{pais}_{indicador_codigo}_{anio_inicio}_{anio_fin}.xlsx"
                    datos.to_excel(nombre_archivo, index=False)
                    with open(nombre_archivo, "rb") as f:
                        st.download_button("📥 Descargar Excel", f, file_name=nombre_archivo)
            except Exception as e:
                st.error(f"❌ Error al obtener los datos: {e}")
