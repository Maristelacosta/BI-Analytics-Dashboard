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

# Converter data
df["Data"] = pd.to_datetime(df["Data"])

# Título
st.title("📊 Painel de Análise de BI")
st.subheader("Painel Executivo de Vendas")

# Sidebar
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

# Aplicar filtros
df_filtrado = df[
    (df["Regiao"].isin(regiao)) &
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

with col1:
    st.metric(
        "💰 Faturamento Total",
        f"R$ {faturamento:,.2f}"
    )

with col2:
    st.metric(
        "📦 Quantidade Vendida",
        quantidade
    )

with col3:
    st.metric(
        "📈 Ticket Médio",
        f"R$ {ticket_medio:,.2f}"
    )

st.markdown("---")

# Vendas por Produto
st.subheader("📊 Vendas por Produto")

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
    title="Faturamento por Produto"
)

st.plotly_chart(fig1, use_container_width=True)

# Participação por Região
st.subheader("🌎 Participação por Região")

graf_regiao = (
    df_filtrado.groupby("Regiao")["Valor"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    graf_regiao,
    names="Regiao",
    values="Valor",
    title="Distribuição das Vendas"
)

st.plotly_chart(fig2, use_container_width=True)

# Evolução das Vendas
st.subheader("📅 Evolução das Vendas")

vendas_tempo = (
    df_filtrado.groupby("Data")["Valor"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    vendas_tempo,
    x="Data",
    y="Valor",
    title="Evolução das Vendas",
    markers=True
)

st.plotly_chart(fig3, use_container_width=True)

# Ranking
st.subheader("🏆 Ranking de Produtos")

ranking = (
    df_filtrado.groupby("Produto")["Valor"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

st.dataframe(
    ranking,
    use_container_width=True
)

# Base completa
st.subheader("📋 Base de Dados")

st.dataframe(
    df_filtrado,
    use_container_width=True
)

# Rodapé
st.markdown("---")

st.markdown(
    "🚀 Projeto desenvolvido por Maristela Costa utilizando Python, Pandas, Plotly e Streamlit."
)
