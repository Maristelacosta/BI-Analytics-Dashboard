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
@st.cache_data
def carregar_dados():
    return pd.read_csv(
        "dados/vendas.csv",
        parse_dates=["data"]
    )

df = carregar_dados()

# Título
st.title("📊 Painel de Análise de BI")
st.subheader("Painel Executivo de Vendas")

# Sidebar
st.sidebar.header("Filtros")

regioes = st.sidebar.multiselect(
    "Selecione a Região",
    options=df["regiao"].unique(),
    default=df["regiao"].unique()
)

produtos = st.sidebar.multiselect(
    "Selecione o Produto",
    options=df["produto"].unique(),
    default=df["produto"].unique()
)

# Aplicando filtros
df_filtrado = df[
    (df["regiao"].isin(regioes)) &
    (df["produto"].isin(produtos))
]

# KPIs
faturamento_total = df_filtrado["valor"].sum()
total_vendas = df_filtrado["quantidade"].sum()
ticket_medio = faturamento_total / len(df_filtrado)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💰 Faturamento Total",
        f"R$ {faturamento_total:,.2f}"
    )

with col2:
    st.metric(
        "📦 Quantidade Vendida",
        f"{total_vendas}"
    )

with col3:
    st.metric(
        "🧾 Ticket Médio",
        f"R$ {ticket_medio:,.2f}"
    )

st.divider()

# Vendas por Produto
st.subheader("📈 Vendas por Produto")

vendas_produto = (
    df_filtrado
    .groupby("produto")["valor"]
    .sum()
    .reset_index()
)

fig_bar = px.bar(
    vendas_produto,
    x="produto",
    y="valor",
    color="produto",
    title="Faturamento por Produto"
)

st.plotly_chart(fig_bar, use_container_width=True)

# Participação por Região
st.subheader("🌎 Participação por Região")

vendas_regiao = (
    df_filtrado
    .groupby("regiao")["valor"]
    .sum()
    .reset_index()
)

fig_pie = px.pie(
    vendas_regiao,
    names="regiao",
    values="valor",
    hole=0.4
)

st.plotly_chart(fig_pie, use_container_width=True)

# Evolução Temporal
st.subheader("📅 Evolução das Vendas")

vendas_tempo = (
    df_filtrado
    .groupby("data")["valor"]
    .sum()
    .reset_index()
)

fig_line = px.line(
    vendas_tempo,
    x="data",
    y="valor",
    markers=True,
    title="Evolução do Faturamento"
)

st.plotly_chart(fig_line, use_container_width=True)

# Tabela
st.subheader("📋 Dados Detalhados")

st.dataframe(
    df_filtrado,
    use_container_width=True
)

# Download CSV
csv = df_filtrado.to_csv(index=False)

st.download_button(
    label="⬇️ Baixar Dados",
    data=csv,
    file_name="relatorio_vendas.csv",
    mime="text/csv"
)
