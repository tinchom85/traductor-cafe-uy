import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. CONFIGURACIÓN DE LUJO ---
st.set_page_config(
    page_title="Clarito: Sommelier AI 🇺🇾",
    page_icon="☕",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {background-color: #FAFAFA;}
    h1 {color: #2C3E50; font-family: 'Helvetica', sans-serif;}
    div.stButton > button {
        background-color: #A0522D; 
        color: white; 
        border-radius: 8px; 
        padding: 12px;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #8B4513;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXIÓN API ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ Error de Configuración: Falta la API Key en Secrets.")
    st.stop()

# --- 3. INTERFAZ PRO ---
st.title("☕ Clarito: Expert Sommelier")
st.write("Análisis 'De la Finca a la Taza'. Subí tu etiqueta para una experiencia sensorial completa.")

# Lista ampliada para entusiastas
metodo_usuario = st.selectbox(
    "Seleccioná tu método de extracción:",
    (
        "✨ Sorprendeme (Recomendación del Sommelier)",
        "AeroPress (Invertida/Tradicional)",
        "V60 / Origami / Kalita (Pour-over)",
        "Chemex",
        "Prensa Francesa",
        "Moka Italiana (Volturno)",
        "Máquina de Espresso (Comercial/Hogareña)",
        "Cold Brew",
        "Syphon / Vacío"
    )
)

archivo = st.file_uploader("📸 Foto de la etiqueta (Frente o Dorso)", type=["jpg", "png", "jpeg"])

# --- 4. EL CEREBRO 360° (PROMPT AVANZADO) ---
def analizar_experto(imagen, metodo):
    model = genai.GenerativeModel('gemini-2.5-flash') 
    
    prompt = f"""
    Eres un Sommelier de Café de Clase Mundial y experto en la escena de café de especialidad de Uruguay.
    Tu conocimiento abarca desde la agronomía (varietales, terruño, procesos) hasta la física de la extracción y la gastronomía molecular.

    Analiza la imagen de esta etiqueta con profundidad.
    El usuario dispone de: {metodo}.

    --- 1. ANÁLISIS DE ORIGEN (TERROIR) ---
    Identifica Variedad (ej. Geisha, Pacamara, Borbón), Proceso (Anaeróbico, Lavado, Natural) y Altura.
    Explica cómo estas variables definen lo que el usuario va a sentir.
    *Ejemplo: "Al ser un proceso Natural de 1800m, esperamos una fermentación frutal intensa y mucho cuerpo..."*

    --- 2. LA RECETA MAESTRA ---
    Diseña la receta exacta para el método: {metodo}.
    Si eligió "Sorprendeme", selecciona el método que MEJOR exprese las cualidades de este grano específico.
    Detalla:
    - **Ratio:** (ej. 1:16 para resaltar elegancia o 1:14 para fuerza).
    - **Molienda:** Sé visual (ej. "Sal Kosher", "Azúcar talco").
    - **Temperatura:** Precisa (ej. "93°C para abrir la acidez").
    - **Técnica:** (ej. "En AeroPress usa método invertido para retener aceites" o "En V60 haz un bloom largo de 45s").

    --- 3. MARIDAJE DE ALTO NIVEL (URUGUAY) ---
    Olvida las recomendaciones básicas. Piensa como un chef que diseña una carta en una cafetería de especialidad de Montevideo (Pocitos/Carrasco/Cordón).
    Busca elevar la experiencia mediante:
    A) **Complemento:** Sabores similares que se potencian.
    B) **Contraste:** Sabores opuestos que crean equilibrio.
    
    Sugiere UNA opción de pastelería/salado de alta calidad disponible en Uruguay.
    *Opciones sugeridas (pero elige la mejor):*
    - Scones de Queso Parmesano (Contraste salado).
    - Carrot Cake con frosting de lima (Para cafés especiados).
    - Tostada de Masa Madre con Palta y Huevo (Para cafés complejos).
    - Alfajor de Pistacho o Almendras (Tendencia actual).
    - Financier o Magdalena de Limón.
    - Cinnamon Roll (Para cafés dulces).

    --- FORMATO ---
    Usa un tono sofisticado, educado y apasionado (Neutro Rioplatense). Usa Markdown.
    """
    
    try:
        with st.spinner('Calibrando molino, analizando terroir y buscando maridaje... 🧐'):
            response = model.generate_content([prompt, imagen])
            return response.text
    except Exception as e:
        return f"Error de lectura: {e}. Intenta con una foto más clara."

# --- 5. VISUALIZACIÓN ---
if archivo is not None:
    image = Image.open(archivo)
    st.image(image, use_column_width=True)
    
    if st.button('🔍 Iniciar Cata Virtual'):
        resultado = analizar_experto(image, metodo_usuario)
        st.markdown(resultado)
        st.info("💡 Tip: Guarda esta receta para replicarla siempre igual.")
