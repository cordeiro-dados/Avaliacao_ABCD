import streamlit as st
from databricks import sql
from dotenv import load_dotenv
import os

load_dotenv()
DB_SERVER_HOSTNAME = os.getenv("DB_SERVER_HOSTNAME")
DB_HTTP_PATH = os.getenv("DB_HTTP_PATH")
DB_ACCESS_TOKEN = os.getenv("DB_ACCESS_TOKEN")

# Função para conectar ao banco de dados
def conectar_banco():
    return sql.connect(
        server_hostname=DB_SERVER_HOSTNAME,
        http_path=DB_HTTP_PATH,
        access_token=DB_ACCESS_TOKEN
    )

# Função para verificar o login
def verificar_login(username, password):
    connection = conectar_banco()
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT id_emp
        FROM datalake.avaliacao_abcd.login
        WHERE username = '{username}' AND password = '{password}'
    """)
    resultado = cursor.fetchone()
    cursor.close()
    connection.close()
    return resultado is not None

# Função para a página de login
def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if verificar_login(username, password):
            st.session_state['logged_in'] = True
            st.success("Login bem-sucedido! Vá para a aplicação principal.")
        else:
            st.error("Usuário ou senha incorretos.")
