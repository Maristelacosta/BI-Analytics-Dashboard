import streamlit as st
import pandas as pd
import plotly.express as px

# ====================================
# CONFIGURAÇÃO DA PÁGINA
# ====================================

st.set_page_config(
    page_title="BI Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ====================================
# CARREGAMENTO DOS DADOS
# ====================================

@st.cache_data
def carregar_dados():
    return pd.read_csv(
        "dados/vendas.csv",
        parse_dates=["data"]
    )

df = carregar_dados()

# ====================================
# TÍTULO
# ====================================

st.title("📊 Painel de Análise de BI")
st.subheader("Painel Executivo de Vendas")

# ====================================
# FILTROS
# ====================================

st.sidebar.header("Filtros")

regioes = st.sidebar.multiselect(
    "Selecione a Região",
    options=sorted(df["regiao"].unique()),
    default=sorted(df["regiao"].unique())
)

produtos = st.sidebar.multiselect(
    "Selecione o Produto",
    options=sorted(df["produto"].unique()),
    default=sorted(df["produto"].unique())
)

# Aplicação dos filtros
df_filtrado = df[
    (df["regiao"].isin(regioes)) &
    (df["produto"].isin(produtos))
]

# ====================================
# KPIs
# ====================================

faturamento_total = df_filtrado["valor"].sum()

quantidade_vendida = df_filtrado["quantidade"].sum()

ticket_medio = (
    faturamento_total / quantidade_vendida
    if quantidade_vendida > 0 else 0
)

produto_top = (
    df_filtrado.groupby("produto")["valor"]
    .sum()
    .idxmax()
    if not df_filtrado.empty else "-"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Faturamento",
        f"R$ {faturamento_total:,.2f}"
    )

with col2:
    st.metric(
        "📦 Quantidade",
        f"{quantidade_vendida:,}"
    )

with col3:
    st.metric(
        "🧾 Ticket Médio",
        f"R$ {ticket_medio:,.2f}"
    )

with col4:
    st.metric(
        "🏆 Produto Líder",
        produto_top
    )

st.divider()

# ====================================
# GRÁFICOS
# ====================================

col_esq, col_dir = st.columns(2)

# Vendas por Produto
with col_esq:

    st.subheader("📈 Vendas por Produto")

    vendas_produto = (
        df_filtrado
        .groupby("produto")["valor"]
        .sum()
        .reset_index()
    
