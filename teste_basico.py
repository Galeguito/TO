import streamlit as st
import datetime

# --- Interface Mínima ---

st.title("Olá! Este é o Streamlit Básico")

st.write("Se você está vendo esta mensagem, o Streamlit está funcionando!")

# Widget simples
nome = st.text_input("Digite seu nome aqui:", "Usuário")

if nome:
    st.success(f"Bem-vindo(a), {nome}!")

# Mostra a data atual para provar que o código Python está rodando
agora = datetime.datetime.now()
st.info(f"O script Python rodou em: {agora.strftime('%H:%M:%S')}")

# Um slider simples para testar a interatividade
valor_slider = st.slider("Teste de Slider", 0, 100, 50)
st.write(f"Valor selecionado: {valor_slider}")