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

fig1 = px.bar(
    graf_produto,
    x="Produto",
    y="Valor",
    color="Valor",
    title="Faturamento por Produto"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# Gráfico por região
st.subheader("🌎 Participação por Região")

graf_regiao = (
    df_filtrado
    .groupby("Regiao")["Valor"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    graf_regiao,
    names="Regiao",
    values="Valor",
    title="Distribuição das Vendas"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# Ranking
st.subheader("🏆 Ranking de Produtos")

ranking = (
    df_filtrado
    .groupby("Produto")["Valor"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

st.dataframe(
    ranking,
    use_container_width=True
)

# Base de dados
st.subheader("📋 Base de Dados")

st.dataframe(
    df_filtrado,
    use_container_width=True
)

# Rodapé
st.markdown("---")
st.markdown(
    "Projeto desenvolvido por Maristela Costa com Python, Pandas, Plotly e Streamlit."
)

# Gráfico de vendas por produto
st.subheader("📊 Vendas por Produto")

graf_produto = (
    df_filtrado
    .groupby("Produto")["Valor"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    graf_produto,
    x="Produto",
    y="Valor",
    color="Valor",
    title="Faturamento por Produto"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)
