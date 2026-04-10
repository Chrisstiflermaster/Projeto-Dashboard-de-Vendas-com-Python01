# PROJETO: Análise Exploratória de Vendas com Pandas
# autor: Claudio dos santos
# dataset : Superstore Sales Dataset (Kaggle)
# link : https://www.kaggle.com/datasets/rohitsinghvi/superstore-sales-dataset
# objetivo: responder perguntas de negócios reais usando
#    apenas Python + Pandas — sem ferramentas complexas

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Dashboard de Vendas")

arquivo = st.file_uploader("Suba seu Excel", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)
    st.dataframe(df)

    fig = px.bar(df, x="Mês", y="Faturamento")
    st.plotly_chart(fig)

# 1. Carregar o dataset

df = pd.read_csv('superstore_sales.csv', encoding='latin-1')

# Primeira olhada: quantas linhas e colunas temos?
print("== visão geral do dataset ==")
print(f"Total de linhas: {len(df)}")
print(f"Total de colunas: {len(df.columns)}")
print()

# ver as primeiras linhas para entender a estrutura dos dados
print(df.head())
print()

# 2. Limpeza e preparação dos dados

# verificar se há valores nulos em cada coluna
print("== valores nulos por coluna ==")
print(df.isnull().sum())
print()

# Converter a coluna de data para o tipo correto
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

# Criar colunas auxiliares
df["ano"] = df['Order Date'].dt.year
df["mes"] = df['Order Date'].dt.month
df["Nome do Mes"] = df["Order Date"].dt.strftime("%B")

# 3. Análise Exploratória

faturamento_total = df['Sales'].sum()
print(f"=== Faturamento Total ===")
print(f"Faturamento total: ${faturamento_total:,.2f}")
print()

# 3.2 Qual categoria vende mais?
print("=== Categorias mais vendidas ===")
vendas_categoria = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
vendas_categoria.columns = ["Categoria", "Faturamento Total de vendas"]

vendas_categoria["Faturamento Total de vendas"] = vendas_categoria["Faturamento Total de vendas"].map(
    "R$ {:,.2f}".format
)

print(vendas_categoria.to_string(index=False))
print()

# 3.3 Qual o produto mais vendido?
print("=== top 10 produtos mais vendidos ===")
top_produtos = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
top_produtos.columns = ["Produto", "Total de Vendas"]
print(top_produtos.head(10).to_string(index=False))
print()

# 3.4 Qual região performa melhor?
print("=== vendas por região ===")
vendas_regiao = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
vendas_regiao.columns = ["Região", "Faturamento Total de vendas"]
print(vendas_regiao.to_string(index=False))
print()

# 3.5 Evolução mensal das vendas
print("=== faturamento mensal (todos os anos) ===")
vendas_mensal = (
    df.groupby(["ano", "mes"])["Sales"]
    .sum()
    .reset_index()
    .sort_values(["ano", "mes"])
)
vendas_mensal.columns = ["Ano", "Mes", "Total de Vendas"]
print(vendas_mensal.to_string(index=False))
print()

# 3.6 Ticket médio por categoria
print("=== ticket médio por categoria ===")
ticket_medio = (
    df.groupby("Category")["Sales"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)
ticket_medio.columns = ["Categoria", "Ticket Médio"]
ticket_medio["Ticket Médio"] = ticket_medio["Ticket Médio"].map("R$ {:,.2f}".format)
print(ticket_medio.to_string(index=False))
print()

# 3.7 Lucro por segmento de cliente
print("=== lucro por segmento ===")
lucro_segmento = (
    df.groupby("Segment")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
lucro_segmento.columns = ["Segmento", "Lucro Total"]
lucro_segmento["Lucro Total"] = lucro_segmento["Lucro Total"].map(
    "R$ {:,.2f}".format
)
print(lucro_segmento.to_string(index=False))
print()

# 3.8 Produtos com prejuízo
print("=== produtos com prejuízo ===")
prejuizo = (
    df.groupby("Product Name")["Profit"]
    .sum()
    .sort_values()
    .head(10)
    .reset_index()
)
prejuizo.columns = ["Produto", "Prejuízo"]
print(prejuizo.to_string(index=False))
print()

# 4. Resumo executivo
print("=" * 50)
print("resumo executivo")
print("=" * 50)
print(f"Total de pedidos analisados : {len(df):,}")
print(f"Período                     : {df['Order Date'].dropna().min().date()} → {df['Order Date'].dropna().max().date()}")
print(f"Faturamento total           : R$ {df['Sales'].sum():,.2f}")
print(f"Lucro total                 : R$ {df['Profit'].sum():,.2f}")
print(f"Margem de lucro             : {(df['Profit'].sum() / df['Sales'].sum() * 100):.1f}%")
print(f"Categoria top               : {df.groupby('Category')['Sales'].sum().idxmax()}")
print(f"Região top                  : {df.groupby('Region')['Sales'].sum().idxmax()}")
print("=" * 50)