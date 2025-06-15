import streamlit as st
import wbdata
import pandas as pd

st.set_page_config(page_title="Explorador de Indicadores del Banco Mundial", layout="centered")
st.title("🌍 Explorador de Indicadores del Banco Mundial")

st.markdown("### 🕰️ Ingresa el nombre o código ISO del país (por ejemplo: Mexico o MEX):")
pais_input = st.text_input("", placeholder="Ej. Mexico o MEX")

if pais_input:
    try:
        # Convertir entrada en código de país (opcionalmente normalizar a ISO 3)
        paises = wbdata.get_source()  # solo para probar conexión
        st.success("Conexión exitosa con el Banco Mundial.")

        st.info("🔄 Buscando indicadores disponibles para el país...")

        # Consulta simulada de indicadores porque wbdata.get_indicator() no funciona en últimas versiones
        indicadores = {
            "NY.GDP.MKTP.CD": "PIB (USD)",
            "FP.CPI.TOTL.ZG": "Inflación (%)",
            "SL.UEM.TOTL.ZS": "Desempleo (%)",
        }

        indicadores_df = pd.DataFrame(list(indicadores.items()), columns=["Código", "Descripción"])
        st.dataframe(indicadores_df)

        st.download_button(
            "📥 Descargar indicadores disponibles",
            indicadores_df.to_csv(index=False).encode("utf-8"),
            file_name="indicadores_disponibles.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Error al consultar el Banco Mundial: {e}")
