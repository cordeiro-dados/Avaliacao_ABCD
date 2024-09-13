import streamlit as st
from login import login_page
from avaliacao_abcd import abcd_page

# Cria um seletor de páginas na barra lateral
st.sidebar.title("Navegação")
pagina_selecionada = st.sidebar.selectbox("Escolha a página", ["Login", "Aplicação ABCD"])

# Carrega a página selecionada
if pagina_selecionada == "Login":
    login_page()
elif pagina_selecionada == "Aplicação ABCD":
    abcd_page()