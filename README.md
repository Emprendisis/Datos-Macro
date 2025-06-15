# 🌍 Explorador de Indicadores Macroeconómicos

Esta aplicación permite consultar, visualizar y exportar datos macroeconómicos históricos desde diversas fuentes públicas como el **Banco Mundial (World Bank)**.

## 🚀 Características

- Selección dinámica de la fuente de datos (actualmente: World Bank)
- Consulta por país y por indicador macroeconómico
- Filtro de rango de años
- Visualización de la serie de tiempo en gráfico
- Exportación de los datos a archivo Excel

## 📊 Indicadores disponibles

Los indicadores disponibles incluyen (dependiendo de la fuente):

- PIB (USD)
- Inflación (%)
- Tasa de desempleo
- Deuda como porcentaje del PIB
- Déficit/superávit comercial
- PIB PPA (USD)
- Prima de riesgo, entre otros

## 🌐 Fuente de Datos

Actualmente habilitado:

- [World Bank Open Data](https://data.worldbank.org/)

## ▶️ Cómo ejecutar

1. Clona este repositorio.
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:

```bash
streamlit run app.py
```

## 📁 Archivos

- `app.py`: código principal de la aplicación
- `requirements.txt`: dependencias necesarias
- `README.md`: documentación del proyecto

## 📌 Notas

- Próximamente se integrarán nuevas fuentes como **FRED**, **IMF**, y **TradingEconomics**.
- Esta app es compatible con despliegue en [Streamlit Cloud](https://streamlit.io/cloud).

---
Desarrollado para facilitar el análisis económico comparado entre países.