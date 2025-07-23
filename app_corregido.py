import streamlit as st
import pandas as pd
import openai

# Inicializa el cliente con la clave desde secrets
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Función para cargar los datos
@st.cache_data
def cargar_datos():
    return pd.read_excel("propiedades_bogota_10.xlsx")

# Cargar el DataFrame
df = cargar_datos()

# Mostrar título
st.title("🏠 Agente Virtual Inmobiliario")

# Mostrar la base de datos opcionalmente
if st.checkbox("🔍 Ver base de datos"):
    st.dataframe(df)

# Preguntas predefinidas
preguntas = [
    "¿Qué propiedades hay en arriendo en Chapinero?",
    "¿Tienes casas con parqueadero en Suba?",
    "Propiedades en venta por menos de 400 millones",
    "Apartamentos de 2 baños en Engativá",
    "¿Qué propiedades hay disponibles en Teusaquillo?",
    "Casas de 3 habitaciones en venta"
]

# Selector de preguntas
pregunta = st.selectbox("🧠 Pregunta", preguntas)

# Botón para ejecutar
if st.button("🔍 Buscar propiedades"):

    columnas = ", ".join(df.columns)

    with st.spinner("🔍 Interpretando la pregunta..."):

        try:
            # Llamada a OpenAI con el modelo GPT
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Eres un asistente experto en filtrar inmuebles. Usa columnas como: {columnas}."},
                    {"role": "user", "content": pregunta},
                ]
            )

            codigo = response.choices[0].message.content.strip("`python").strip("`").strip()

            st.subheader("🧠 Código generado:")
            st.code(codigo, language='python')

            # Evaluar el código como filtro
            resultados = eval(codigo)

            if not resultados.empty:
                st.success("✅ Propiedades encontradas:")
                st.dataframe(resultados)
            else:
                st.warning("⚠️ No se encontraron propiedades para esta consulta.")

        except Exception as e:
            st.error("❌ Error procesando la consulta:")
            st.text(str(e))
