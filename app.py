import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================

st.set_page_config(
    page_title="BI Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================
# CARREGAR DADOS
# =====================================

@st.cache_data
def carregar_dados():
    df = pd.read_csv(
        "dados/vendas.csv",
        parse_dates=["Data"]
    )
    return df

df = carregar_dados()

# =====================================
# TÍTULO
# =====================================

st.title("📊 BI Analytics Dashboard")
st.subheader("Painel Executivo de Vendas")

# =====================================
# FILTROS
# =====================================

st.sidebar.header("🔎 Filtros")

regioes = st.sidebar.multiselect(
    "Região",
    options=sorted(df["Regiao"].unique()),
    default=sorted(df["Regiao"].unique())
)

categorias = st.sidebar.multiselect(
    "Categoria",
    options=sorted(df["Categoria"].unique()),
    default=sorted(df["Categoria"].unique())
)

produtos = st.sidebar.multiselect(
    "Produto",
    options=sorted(df["Produto"].unique()),
    default=sorted(df["Produto"].unique())
)

# =====================================
# DADOS FILTRADOS
# =====================================

df_filtrado = df[
    (df["Regiao"].isin(regioes))
    & (df["Categoria"].isin(categorias))
    & (df["Produto"].isin(produtos))
]

# =====================================
# KPIs
# =====================================

faturamento = df_filtrado["Valor"].sum()

quantidade = df_filtrado["Quantidade"].sum()

ticket_medio = (
    faturamento / quantidade
    if quantidade > 0 else 0
)

produto_lider = "-"

if not df_filtrado.empty:
    produto_lider = (
        df_filtrado.groupby("Produto")["Valor"]
        .sum()
        .idxmax()
    )

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Faturamento",
    f"R$ {faturamento:,.2f}"
)

col2.metric(
    "📦 Quantidade",
    quantidade
)

col3.metric(
    "🧾 Ticket Médio",
    f"R$ {ticket_medio:,.2f}"
)

col4.metric(
    "🏆 Produto Líder",
    produto_lider
)

st.divider()

# =====================================
# GRÁFICOS
# =====================================

col_esq, col_dir = st.columns(2)

with col_esq:

    st.subheader("📈 Vendas por Produto")

    vendas_produto = (
        df_filtrado
        .groupby("Produto")["Valor"]
        .sum()
        .reset_index()
        .sort_values(
            by="Valor",
            ascending=False
        )
    )

    fig_produto = px.bar(
        vendas_produto,
        x="Produto",
        y="Valor",
        color="Produto",
        text_auto=True
    )

    st.plotly_chart(
        fig_produto,
        use_container_width=True
    )

with col_dir:

    st.subheader("🌎 Participação por Região")

    vendas_regiao = (
        df_filtrado
        .groupby("Regiao")["Valor"]
        .sum()
        .reset_index()
    )

    fig_regiao = px.pie(
        vendas_regiao,
        names="Regiao",
        values="Valor",
        hole=0.4
    )

    st.plotly_chart(
        fig_regiao,
        use_container_width=True
    )

# =====================================
# CATEGORIAS
# =====================================

st.subheader("📊 Faturamento por Categoria")

categoria_df = (
    df_filtrado
    .groupby("Categoria")["Valor"]
    .sum()
    .reset_index()
)

fig_categoria = px.bar(
    categoria_df,
    x="Categoria",
    y="Valor",
    color="Categoria",
    text_auto=True
)

st.plotly_chart(
    fig_categoria,
    use_container_width=True
)

# =====================================
# EVOLUÇÃO TEMPORAL
# =====================================

st.subheader("📅 Evolução das Vendas")

vendas_tempo = (
    df_filtrado
    .groupby("Data")["Valor"]
    .sum()
    .reset_index()
)

fig_tempo = px.line(
    vendas_tempo,
    x="Data",
    y="Valor",
    markers=True
)

st.plotly_chart(
    fig_tempo,
    use_container_width=True
)

# =====================================
# TABELA
# =====================================

st.subheader("📋 Dados Detalhados")

st.dataframe(
    df_filtrado.sort_values("Data"),
    use_container_width=True,
    hide_index=True
)

# =====================================
# DOWNLOAD CSV
# =====================================

csv = df_filtrado.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "⬇️ Baixar Relatório CSV",
    data=csv,
    file_name="relatorio_vendas.csv",
    mime="text/csv"
)

# =====================================
# RODAPÉ
# =====================================

st.markdown("---")

st.caption(
    "Desenvolvido por Maristela Costa • BI Analytics Dashboard • Python • Streamlit • Pandas • Plotly"
)
