import streamlit as st
from login import login_page
from avaliacao_abcd import abcd_page
from func_data import func_data_page  # Importar a nova página
from alter_nota import func_data_nota

# Cria um seletor de páginas na barra lateral
st.sidebar.title("Navegação")
pagina_selecionada = st.sidebar.selectbox("Escolha a página", ["Login", "Avaliação ABCD", "Funcionários Data","Lista de Avaliados"])  # Adicionar nova opção

# Carrega a página selecionada
if pagina_selecionada == "Login":
    login_page()
elif pagina_selecionada == "Avaliação ABCD":
    abcd_page()
elif pagina_selecionada == "Funcionários Data":  # Nova página
    func_data_page()  # Chama a função da nova página
elif pagina_selecionada == "Lista de Avaliados":  # Nova página
    func_data_nota()  # Chama a função da nova página