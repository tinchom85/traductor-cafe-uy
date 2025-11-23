import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Clarito: Sommelier AI 🇺🇾", page_icon="☕", layout="centered")

st.markdown("""
    <style>
    .stApp {background-color: #FAFAFA;}
    h1 {color: #2C3E50;}
    div.stButton > button {background-color: #A0522D; color: white; border-radius: 8px; width: 100%;}
    </style>
    """, unsafe_allow_html=True)

# --- API KEY ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.stop()

# --- INTERFAZ ---
st.title("☕ Clarito: Sommelier 360°")
st.write("Análisis sensorial completo. Sin límites.")

metodo_usuario = st.selectbox(
    "Seleccioná tu método:",
    ("✨ Sorprendeme", "AeroPress", "V60 / Origami", "Chemex", "Prensa Francesa", "Moka Italiana", "Espresso", "Cold Brew")
)

archivo = st.file_uploader("📸 Foto de la etiqueta", type=["jpg", "png", "jpeg"])

# --- EL CEREBRO LIBERADO ---
def analizar_experto(imagen, metodo):
    model = genai.GenerativeModel('gemini-2.5-flash') 
    
    prompt = f"""
    Eres un Sommelier de Café de Clase Mundial y Crítico Gastronómico en Uruguay.
    
    Analiza esta etiqueta. El usuario usará: {metodo}.

    --- 1. ANÁLISIS DE TERROIR ---
    Identifica Variedad, Proceso y Altura.
    Explica qué esperar en taza (Acidez, Cuerpo, Dulzura) basándote en esos datos técnicos.

    --- 2. LA RECETA MAESTRA ---
    Diseña la receta técnica para: {metodo}.
    Define Ratio, Temperatura y Molienda exacta. Explica el porqué de tus decisiones.

    --- 3. MARIDAJE DE AUTOR (SIN LÍMITES) ---
    Accede a tu conocimiento completo sobre la gastronomía de cafetería y panadería en Uruguay (Clásica y Moderna/Tendencia).
    
    NO te limites a una lista. Piensa fuera de la caja.
    Analiza las notas del café (ej. si es cítrico, terroso, chocolatoso, especiado) y busca el "Match Perfecto" en el repertorio uruguayo.

    Puedes sugerir desde clásicos (ej. Martín Fierro, Yo-Yo, Bizcochos de grasa) hasta tendencias modernas de especialidad (ej. Avocado Toast, Babka, Cardamom Bun, Tostados de Focaccia).

    TU MISIÓN:
    1. Define si el café pide algo DULCE (para acompañar) o SALADO (para contrastar).
    2. Elige UN plato específico.
    3. Justifica la elección sensorialmente (ej. "La grasa del queso de cabra limpiará la astringencia de este tueste oscuro...").

    --- FORMATO ---
    Usa tono profesional, rioplatense neutro y elegante.
    """
    
    try:
        with st.spinner('Catando el café y revisando el menú de todo Montevideo... 🧐'):
            response = model.generate_content([prompt, imagen])
            return response.text
    except Exception as e:
        return f"Error: {e}"

if archivo is not None:
    image = Image.open(archivo)
    st.image(image, use_column_width=True)
    if st.button('🔍 Iniciar Cata'):
        resultado = analizar_experto(image, metodo_usuario)
        st.markdown(resultado)
