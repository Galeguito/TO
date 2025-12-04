import streamlit as st
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import os

# --- CONSTANTES ---
IMAGE_WIDTH = 200
IMAGE_HEIGHT = 50
MODEL_FILENAME = "modelo_topologia.keras"
OUTPUT_DIM = IMAGE_WIDTH * IMAGE_HEIGHT

# --- FUNÇÕES ESSENCIAIS ---

# @st.cache_resource: Cacheia o carregamento do modelo para não recarregar a cada interação
@st.cache_resource 
def load_model(filename=MODEL_FILENAME):
    """Carrega o modelo salvo do disco. O caminho é relativo ao app.py."""
    
    # Adicionando um print de depuração para verificar se o arquivo existe
    # Isso aparecerá nos logs do Streamlit Cloud
    print(f"Tentando carregar o modelo em: {os.path.abspath(filename)}")
    
    if not os.path.exists(filename):
        # Em ambiente web, a localização do modelo pode ser diferente.
        # Se o modelo não estiver no GitHub, esta mensagem é exibida.
        st.error(f"Erro: Arquivo de modelo não encontrado em: {filename}.")
        st.caption("Verifique se 'modelo_topologia.keras' foi incluído e commitado no seu repositório GitHub.")
        return None
    try:
        # Apenas um aviso: Modelos grandes podem falhar no carregamento sem Git LFS.
        loaded_model = tf.keras.models.load_model(filename)
        return loaded_model
    except Exception as e:
        st.error(f"Erro ao carregar o modelo: {e}")
        return None

def predict_topologia(model, vr, vf, vyl):
    """
    Faz a predição da densidade binária a partir dos 3 parâmetros.
    """
    input_data = np.array([[vr, vf, vyl]], dtype=np.float32)
    
    # 1. Predição
    prediction = model.predict(input_data, verbose=0)
    
    # 2. Reshape para a matriz 50x200 (Top-Down)
    image_array = prediction.reshape((IMAGE_HEIGHT, IMAGE_WIDTH))

    # 3. Inverte (flipud) para visualização Bottom-Up (Y=0 na base)
    return np.flipud(image_array)


# --- INTERFACE PRINCIPAL DO STREAMLIT ---

# 1. Carrega o Modelo (usando cache)
ml_model = load_model()

# Se o modelo não carregar, interrompe a execução e exibe o erro
if ml_model is None:
    st.stop() 

st.title("⚙️ Otimização Topológica Interativa (MLP)")
st.write("Ajuste os parâmetros abaixo para gerar uma nova topologia predita pelo modelo.")

# 2. Coluna Lateral para Sliders (Widgets)
st.sidebar.header("Parâmetros de Entrada")

# Criação dos Sliders do Streamlit
# Parâmetros: (label, min, max, valor_inicial, passo)
vr = st.sidebar.slider("Parâmetro VR (Razão de Volume)", min_value=0.5, max_value=2.0, value=1.0, step=0.01)
vf = st.sidebar.slider("Parâmetro VF (Volume Fracional)", min_value=0.1, max_value=0.9, value=0.5, step=0.01)
vyl = st.sidebar.slider("Parâmetro VYL (Posição Y da Força)", min_value=-1.0, max_value=1.0, value=0.0, step=0.01)

# 3. Geração da Predição (Chamado automaticamente a cada interação)
predicted_image = predict_topologia(ml_model, vr, vf, vyl)

# 4. Criação da Figura Matplotlib (para renderizar no Streamlit)
fig, ax = plt.subplots(figsize=(10, 2.5))

# Plota a imagem
ax.imshow(predicted_image, 
          cmap='gray_r', 
          interpolation='nearest', 
          origin='lower', 
          vmin=0, 
          vmax=1)
ax.set_title(f"VR:{vr:.2f}, VF:{vf:.2f}, VYL:{vyl:.2f}")
ax.set_xticks(np.linspace(0, IMAGE_WIDTH, 5))
ax.set_yticks(np.linspace(0, IMAGE_HEIGHT, 3))
ax.set_xlabel("Largura da Malha (X)")
ax.set_ylabel("Altura da Malha (Y)")

# 5. Renderiza a figura no navegador
st.pyplot(fig)


st.caption("A topologia é binarizada (0 ou 1) pela função sigmoid de saída do modelo.")
