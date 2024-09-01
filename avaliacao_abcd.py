import streamlit as st
from databricks import sql
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
DB_SERVER_HOSTNAME = os.getenv("DB_SERVER_HOSTNAME")
DB_HTTP_PATH = os.getenv("DB_HTTP_PATH")
DB_ACCESS_TOKEN = os.getenv("DB_ACCESS_TOKEN")

# Aplicando CSS para aumentar a largura da página e expandir elementos
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 1200px;  /* Aumenta a largura máxima da página */
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .stTextInput > div > div > input {
        width: 100% !important;  /* Expande a largura das caixas de texto */
    }
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Definindo as categorias, notas e suas pontuações com descrições para comportamental
categorias_comportamental = ["Colaboração", "Inteligência Emocional", "Responsabilidade", "Iniciativa / Pró atividade", "Flexibilidade"]
pontuacoes_comportamental = {
    "A": 16,
    "B+": 12,
    "B": 8,
    "C": 4,
    "D": 0
}
descricoes_comportamental = {
    "Colaboração": {
        "A": "Está sempre disponível para servir, tem opiniões próprias, está disposto a colaborar para o atingimento dos bons resultados, independentemente se as ideias são suas ou dos seus colegas. O interesse em colaborar deve ser nato.",
        "B+": "De modo geral tem disposição para colaborar, esforça-se para entregar bons resultados. É prestativo e coloca-se em posição de aprendiz sempre que necessário.",
        "B": "Colabora de forma aceitável, para que o time e a empresa tenham um bom fluxo nas suas atividades.",
        "C": "Tem dificuldade em colaborar com o time em prol de um resultado coletivo. Está deixando de atender as necessidades da equipe e da empresa.",
        "D": "Não se coloca mais como um colaborador. Não atende mais as expectativas do time e da empresa."
    },
    "Inteligência Emocional": {
        "A": "É sempre ponderado em situações de tensão e conflito. Transmite segurança e tranquilidade aos demais, mantendo o equilíbrio emocional de todos a sua volta.",
        "B+": "Habitualmente mantem o controle emocional em situações adversas. Nos momentos de crise e tensão sofre alterações mas volta ao equilíbrio com facilidade.",
        "B": "A perda de equilíbrio emocional é momentânea e aceitável para o seu nível de atuação e maturidade na empresa. Precisa ser desenvolvido para evoluir emocionalmente.",
        "C": "Tem muita dificuldade em manter o equilíbrio emocional. Por vezes deixa sua vida externa impactar em seus resultados na empresa.",
        "D": "Não tem equilíbrio emocional, suas ações são degradáveis e já não agrega ao time e a empresa."
    },
    "Responsabilidade": {
        "A": "Traz a responsabilidade para si, é altamente comprometido com a Empresa, líderes, pares e o time de uma forma geral. Assume seus atos e está a altura dos desafios propostos.",
        "B+": "É comprometido com a sua palavra, honra seus compromissos e entende que é exemplo para os demais do seu time e empresa.",
        "B": "Em algumas situações precisa se provocação do pelo líder, principalmente no que se refere a prazos. De maneira geral assume a responsabilidade e está aberto a mudança de comportamento.",
        "C": "Tem sempre uma justificativa para a perda de prazos. Terceiriza a responsabilidade, porém usa o discurso de que está disponível para mudar o comportamento.",
        "D": "Foge da responsabilidade, está sempre se esquivando dos seus compromissos e verbaliza a certeza de que suas atitudes são corretas e coerentes."
    },
    "Iniciativa / Pró atividade": {
        "A": "Tem alta iniciativa e determinação. Entrega sempre resultados a mais que o esperado, demonstrado a sua senioridade. Não se deixa abater diante das dificuldades, mostra-se comprometido com as suas tarefas e com o resultado dos demais.",
        "B+": "Tem iniciativa na maioria das situações. Vai além dos compromissos rotineiros na maioria das vezes. Assume com frequência os imprevistos e se coloca a disposição para ajudar o time de uma forma geral quando necessário.",
        "B": "Tem iniciativa de forma normal e pontual, dentro do esperado para um colaborador na média. Seus resultados atendem a empresa, mas não são brilhantes.",
        "C": "Não demonstra muita pro atividade e iniciativa diante das atividades propostas. Se mantem neutro nas situações evitando sempre o acúmulo de trabalho.",
        "D": "Não atende as expectativas, se esconde de novas responsabilidades e não é um bom exemplo para o time."
    },
    "Flexibilidade": {
        "A": "Adapta-se de forma veloz ao que está sendo lidado e não cria barreiras, pelo contrário- enxerga sempre uma possibilidade de crescimento.",
        "B+": "Convive na maioria das vezes muito bem com as adversidades que vão sendo impostas. Ainda precisa-se adaptar para “fazer sem reclamar”, porém traz o resultado esperado.",
        "B": "Reclama mas faz, não gosta de mudanças abruptas e resmunga para as novas diretrizes.",
        "C": "Reclama bastante e desestimula os colegas diante de novos desafios. Faz as demandas apenas sob supervisão.",
        "D": "Reclama o tempo todo e não cumpre com os prazos estipulados, pois não acredita mais nas diretrizes impostas."
    }
}

# Definindo a única categoria, notas e suas pontuações com descrições para técnico
categoria_tecnica = "Conhecimento Técnico"
pontuacoes_tecnico = {
    "A": 20,
    "B+": 15,
    "B": 10,
    "C": 5,
    "D": 0
}

# Simulação de descrições para a categoria técnica
descricoes_tecnico = {
    "A": "Descrição A para Conhecimento Técnico",
    "B+": "Descrição B+ para Conhecimento Técnico",
    "B": "Descrição B para Conhecimento Técnico",
    "C": "Descrição C para Conhecimento Técnico",
    "D": "Descrição D para Conhecimento Técnico"
}

# Função para conectar ao banco de dados
def conectar_banco():
    return sql.connect(
        server_hostname=DB_SERVER_HOSTNAME,
        http_path=DB_HTTP_PATH,
        access_token=DB_ACCESS_TOKEN
    )

# Função para calcular a nota final
def calcular_nota_final(selecoes_comportamental, selecao_tecnico):
    nota_comportamental = sum(pontuacoes_comportamental[nota] for nota in selecoes_comportamental if nota)
    nota_tecnico = pontuacoes_tecnico[selecao_tecnico] if selecao_tecnico else 0
    return nota_comportamental, nota_tecnico, nota_comportamental + nota_tecnico

# Função para determinar a nota com base na soma final
def determinar_nota_final(soma_final):
    if soma_final <= 24:
        return "D"
    elif 25 <= soma_final <= 49:
        return "C"
    elif 50 <= soma_final <= 74:
        return "B"
    elif 75 <= soma_final <= 89:
        return "B+"
    else:
        return "A"

# Função para atualizar o banco de dados
def atualizar_banco_dados(nome_colaborador, nome_gestor, setor, diretoria, data_resposta, nota_final):
    try:
        connection = conectar_banco()
        cursor = connection.cursor()
        cursor.execute(f"""
            INSERT INTO datalake.avaliacao_abcd.avaliacao_abcd (nome_colaborador, nome_gestor, setor, diretoria, data_resposta, nota)
            VALUES ('{nome_colaborador}', '{nome_gestor}', '{setor}', '{diretoria}', '{data_resposta}', '{nota_final}')
        """)
        connection.commit()
        cursor.close()
        connection.close()
        st.success("Avaliação salva com sucesso no banco de dados!")
    except Exception as e:
        st.error(f"Erro ao salvar no banco de dados: {str(e)}")

# Interface em Streamlit
st.title("Avaliação ABCD")
st.header("Preencha as informações abaixo:")

# Inputs de informações do colaborador em grid de 2 colunas
cols_inputs = st.columns(2)

with cols_inputs[0]:
    nome_colaborador = st.text_input("Nome do Colaborador")
    setor = st.text_input("Setor")

with cols_inputs[1]:
    nome_gestor = st.text_input("Nome do Gestor")
    diretoria = st.text_input("Diretoria")

# Data de resposta com formato dd-mm-yyyy
cols_date = st.columns([1, 3])  # Reduzir a largura do campo de data
with cols_date[0]:
    data_resposta = st.date_input("Data da Resposta", value=datetime.today(), format="DD-MM-YYYY")

# Avaliação Comportamental
st.subheader("Comportamental")
for categoria in categorias_comportamental:
    st.subheader(categoria)
    cols = st.columns([5, 5, 5, 5, 5])  # Ajuste para deixar as caixas mais largas
    
    selected_nota = st.session_state.get(categoria)  # Recupera a seleção atual para essa categoria

    for i, (nota, desc) in enumerate(descricoes_comportamental[categoria].items()):
        with cols[i]:
            if st.button(f"{nota}\n\n{desc}", key=f"{categoria}_{nota}"):
                st.session_state[categoria] = nota  # Armazena a seleção da nota para a categoria
                st.success(f"Selecionado: {nota} para {categoria}")  # Mensagem de confirmação da seleção

    # Botão para cancelar a seleção de uma categoria
    if selected_nota:
        if st.button(f"Cancelar seleção de {categoria}"):
            del st.session_state[categoria]
            st.warning(f"Seleção de {categoria} foi cancelada.")  # Mensagem de cancelamento

# Avaliação Técnica
st.subheader("Conhecimento Técnico")
cols = st.columns([5, 5, 5, 5, 5])  # Ajuste para deixar as caixas mais largas

selecao_tecnico = st.session_state.get(categoria_tecnica)  # Recupera a seleção atual para a categoria técnica

for i, (nota, desc) in enumerate(descricoes_tecnico.items()):
    with cols[i]:
        if st.button(f"{nota}\n\n{desc}", key=f"{categoria_tecnica}_{nota}"):
            st.session_state[categoria_tecnica] = nota  # Armazena a seleção da nota para a categoria técnica
            st.success(f"Selecionado: {nota} para {categoria_tecnica}")  # Mensagem de confirmação da seleção

# Botão para calcular a nota e salvar no banco de dados
if st.button("Calcular Nota e Salvar"):
    selecoes_comportamental = [st.session_state.get(categoria) for categoria in categorias_comportamental]
    selecao_tecnico = st.session_state.get(categoria_tecnica)
    
    if None in selecoes_comportamental or not selecao_tecnico:
        st.error("Você deve selecionar uma nota para todas as categorias antes de salvar.")
    else:
        nota_comportamental, nota_tecnico, soma_final = calcular_nota_final(selecoes_comportamental, selecao_tecnico)
        nota_final = determinar_nota_final(soma_final)
        
        st.write(f"Nota Comportamental: {nota_comportamental}")
        st.write(f"Nota Técnica: {nota_tecnico}")
        st.write(f"Soma Final: {soma_final}")
        st.write(f"Nota Final: {nota_final}")
        
        atualizar_banco_dados(nome_colaborador, nome_gestor, setor, diretoria, data_resposta, nota_final)
