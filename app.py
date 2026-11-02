import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="BI Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Carregar dados
df = pd.read_csv("vendas.csv")

# Título
st.title("📊 BI Analytics Dashboard")
st.subheader("Dashboard Executivo de Vendas")

# Filtro lateral
st.sidebar.header("Filtros")

regiao = st.sidebar.multiselect(
    "Selecione a Região",
    options=df["Regiao"].unique(),
    default=df["Regiao"].unique()
)

df_filtrado = df[df["Regiao"].isin(regiao)]

# KPIs
faturamento = df_filtrado["Valor"].sum()
quantidade = df_filtrado["Quantidade"].sum()
ticket_medio = faturamento / quantidade

col1, col2, col3 = st.columns(3)

col1.metric("💰 Faturamento Total", f"R$ {faturamento:,.2f}")
col2.metric("📦 Quantidade Vendida", quantidade)
col3.metric("📈 Ticket Médio", f"R$ {ticket_medio:,.2f}")

st.markdown("---")

# Gráfico de vendas por produto
graf_produto = (
    df_filtrado.groupby("Produto")["Valor"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    graf_produto,
    x="Produto",
    y="Valor",
    color="Valor",
    title="Vendas por Produto"
)

st.plotly_chart(fig1, use_container_width=True)

# Gráfico por região
graf_regiao = (
    df_filtrado.groupby("Regiao")["Valor"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    graf_regiao,
    names="Regiao",
    values="Valor",
    title="Participação por Região"
)

st.plotly_chart(fig2, use_container_width=True)

# Ranking de produtos
st.subheader("🏆 Ranking de Produtos")

ranking = (
    df_filtrado.groupby("Produto")["Valor"]
    .sum()
    .sort_values(ascending=False)
)

st.dataframe(ranking)

# Dados completos
st.subheader("📋 Base de Dados")

st.dataframe(df_filtrado)
