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
# FUNÇÕES AUXILIARES
# =====================================
def formatar_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv("dados/vendas.csv", parse_dates=["Data"])
        return df
    except FileNotFoundError:
        st.error("Arquivo 'dados/vendas.csv' não encontrado. Verifique o caminho.")
        st.stop()

df = carregar_dados()

# =====================================
# TÍTULO
# =====================================
st.title("📊 BI Analytics Dashboard")
st.subheader("Painel Executivo de Vendas")

# =====================================
# FILTROS (BARRA LATERAL)
# =====================================
st.sidebar.header("🔎 Filtros")

# Filtro de Data
data_min = df["Data"].min().date()
data_max = df["Data"].max().date()

intervalo_datas = st.sidebar.date_input(
    "Período",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max
)

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

# Filtra produtos disponíveis com base nas categorias selecionadas
produtos_disponiveis = sorted(df[df["Categoria"].isin(categorias)]["Produto"].unique())
produtos = st.sidebar.multiselect(
    "Produto",
    options=produtos_disponiveis,
    default=produtos_disponiveis
)

# =====================================
# DADOS FILTRADOS
# =====================================
# Garante que o usuário selecionou data inicial e final
if len(intervalo_datas) == 2:
    data_inicio, data_fim = intervalo_datas
    filtro_data = (df["Data"].dt.date >= data_inicio) & (df["Data"].dt.date <= data_fim)
else:
    filtro_data = True

df_filtrado = df[
    filtro_data
    & (df["Regiao"].isin(regioes))
    & (df["Categoria"].isin(categorias))
    & (df["Produto"].isin(produtos))
]

if df_filtrado.empty:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados. Ajuste as opções na barra lateral.")
    st.stop()

# =====================================
# KPIs
# =====================================
faturamento = df_filtrado["Valor"].sum()
quantidade = df_filtrado["Quantidade"].sum()
ticket_medio = faturamento / quantidade if quantidade > 0 else 0
produto_lider = df_filtrado.groupby("Produto")["Valor"].sum().idxmax()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Faturamento", formatar_brl(faturamento))
col2.metric("📦 Quantidade", f"{quantidade:,}".replace(",", "."))
col3.metric("🧾 Ticket Médio", formatar_brl(ticket_medio))
col4.metric("🏆 Produto Líder", produto_lider)

st.divider()

# =====================================
# GRÁFICOS
# =====================================
col_esq, col_dir = st.columns(2)

with col_esq:
    st.subheader("📈 Vendas por Produto")
    vendas_produto = (
        df_filtrado.groupby("Produto")["Valor"]
        .sum()
        .reset_index()
        .sort_values(by="Valor", ascending=False)
    )
    fig_produto = px.bar(
        vendas_produto,
        x="Produto",
        y="Valor",
        color="Produto",
        text_auto=".2s"
    )
    fig_produto.update_layout(showlegend=False)
    st.plotly_chart(fig_produto, width="stretch")

with col_dir:
    st.subheader("🌎 Participação por Região")
    vendas_regiao = (
        df_filtrado.groupby("Regiao")["Valor"]
        .sum()
        .reset_index()
    )
    fig_regiao = px.pie(
        vendas_regiao,
        names="Regiao",
        values="Valor",
        hole=0.4
    )
    st.plotly_chart(fig_regiao, width="stretch")

# =====================================
# CATEGORIAS
# =====================================
st.subheader("📊 Faturamento por Categoria")
categoria_df = (
    df_filtrado.groupby("Categoria")["Valor"]
    .sum()
    .reset_index()
    .sort_values(by="Valor", ascending=False)
)
fig_categoria = px.bar(
    categoria_df,
    x="Categoria",
    y="Valor",
    color="Categoria",
    text_auto=".2s"
)
fig_categoria.update_layout(showlegend=False)
st.plotly_chart(fig_categoria, width="stretch")

# =====================================
# EVOLUÇÃO TEMPORAL
# =====================================
st.subheader("📅 Evolução das Vendas")
vendas_tempo = (
    df_filtrado.groupby("Data")["Valor"]
    .sum()
    .reset_index()
    .sort_values("Data")
)
fig_tempo = px.line(
    vendas_tempo,
    x="Data",
    y="Valor",
    markers=True
)
st.plotly_chart(fig_tempo, width="stretch")

# =====================================
# TABELA E DOWNLOAD
# =====================================
st.subheader("📋 Dados Detalhados")
st.dataframe(
    df_filtrado.sort_values("Data", ascending=False),
    width="stretch",
    hide_index=True
)

csv = df_filtrado.to_csv(index=False).encode("utf-8-sig")

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
