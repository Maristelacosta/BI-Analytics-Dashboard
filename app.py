import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard BI",
    page_icon="📊",
    layout="wide"
)

df = pd.read_csv("vendas.csv")

st.title("📊 BI Analytics Dashboard")

st.sidebar.header("Filtros")

regiao = st.sidebar.multiselect(
    "Região",
    df["Regiao"].unique(),
    default=df["Regiao"].unique()
)

df = df[df["Regiao"].isin(regiao)]

faturamento = df["Valor"].sum()

quantidade = df["Quantidade"].sum()

ticket = faturamento / quantidade

col1, col2, col3 = st.columns(3)

col1.metric("💰 Faturamento", f"R$ {faturamento:,.2f}")
col2.metric("📦 Quantidade", quantidade)
col3.metric("📈 Ticket Médio", f"R$ {ticket:,.2f}")

grafico = (
    df.groupby("Produto")["Valor"]
    .sum()
    .reset_index()
)

fig = px.bar(
    grafico,
    x="Produto",
    y="Valor",
    color="Valor",
    title="Vendas por Produto"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(df)
