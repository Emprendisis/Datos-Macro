import streamlit as st
import wbdata

st.set_page_config(page_title="Explorador de Indicadores del Banco Mundial", layout="centered")
st.title("🌍 Explorador de Indicadores del Banco Mundial")

# Entrada del usuario
codigo = st.text_input("🔎 Ingresa el nombre o código ISO del país (por ejemplo: Mexico o MEX):")

if codigo:
    try:
        # Cargar lista de países del Banco Mundial
        paises = wbdata.get_country()
        # Crear diccionario {nombre: código}
        pais_dict = {p["name"].lower(): p["id"] for p in paises}
        codigos_dict = {p["id"].lower(): p["id"] for p in paises}

        codigo = codigo.strip().lower()

        # Buscar el código ISO del país
        if codigo in pais_dict:
            pais_codigo = pais_dict[codigo]
        elif codigo in codigos_dict:
            pais_codigo = codigos_dict[codigo]
        else:
            st.error("❌ País no encontrado. Intenta con otro nombre o código ISO.")
            st.stop()

        st.success(f"✅ Código del país encontrado: {pais_codigo}")

        # Obtener los indicadores disponibles para ese país
        indicadores = wbdata.get_indicator(source=2)  # Fuente 2: Banco Mundial
        st.subheader("📊 Indicadores disponibles:")
        st.write(indicadores)

    except Exception as e:
        st.error(f"❌ Error al consultar el Banco Mundial: {e}")