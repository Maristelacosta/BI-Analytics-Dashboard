import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="BI Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Carregamento dos dados
df = pd.read_csv("vendas.csv")

# Título
st.title("📊 BI Analytics Dashboard")
st.subheader("Dashboard Executivo de Vendas")

# Barra lateral
st.sidebar.header("Filtros")

regiao = st.sidebar.multiselect(
    "Selecione a Região",
    options=df["Regiao"].unique(),
    default=df["Regiao"].unique()
)

produto = st.sidebar.multiselect(
    "Selecione o Produto",
    options=df["Produto"].unique(),
    default=df["Produto"].unique()
)

# Aplicação dos filtros
df_filtrado = df[
    (df["Regiao"].isin(regiao))
    &
    (df["Produto"].isin(produto))
]

# KPIs
faturamento = df_filtrado["Valor"].sum()
quantidade = df_filtrado["Quantidade"].sum()

if quantidade > 0:
    ticket_medio = faturamento / quantidade
else:
    ticket_medio = 0

col1, col2, col3 = st.columns(3)

col1.metric(
    "💰 Faturamento Total",
    f"R$ {faturamento:,.2f}"
)

col2.metric(
    "📦 Quantidade Vendida",
    quantidade
)

col3.metric(
    "📈 Ticket Médio",
    f"R$ {ticket_medio:,.2f}"
)

st.markdown("---")

# Gráfico de vendas por produto
st.subheader("📊 Vendas por Produto")

graf_produto = (
    df_filtrado
    .groupby("Produto")["Valor"]
    .sum()
    .reset_index()
)

fig1 
