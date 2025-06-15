# Explorador de Indicadores del Banco Mundial

Esta aplicación permite consultar los indicadores disponibles para cualquier país usando el nombre o el código ISO de 3 letras, extraídos directamente desde el Banco Mundial.

## Cómo usar

1. Instala las dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecuta la app:
```bash
streamlit run app.py
```

3. Ingresa el nombre o código del país (por ejemplo, "Mexico" o "MEX") y explora los indicadores.

## Requisitos

- Python 3.8 o superior
- Conexión a internet

## Fuentes de datos

- World Bank Open Data API vía `wbdata`