#  PROJETO 2: Dashboard Visual de Vendas
#  Autor   : Seu Nome
#  Dataset : Superstore Sales Dataset (Kaggle)
#  Link    : https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
#  Objetivo: Transformar dados de vendas em gráficos claros
#            que contam uma história para o negócio.
#  Libs    : Pandas · Matplotlib · Seaborn

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# 1. configuração visual

# Estilo geral dos gráficos — deixa tudo mais limpo e moderno
sns.set_theme(style="whitegrid", palette="muted")

# 2. tamanho padrão de fonte
plt.rcParams["font.size"] = 11
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.titleweight"] = "bold"

# 3. carregando preparando os dados
df = pd.read_csv("superstore_sales.csv", encoding="latin-1")

# Converter datas e criar colunas auxiliares
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["ano"] = df["Order Date"].dt.year    
df["mês"] = df["Order Date"].dt.to_period("M").astype(str)

# 4. preparar os dados para os gráficos

# vendas por categoria
vendas_categoria = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

# vendas por região
vendas_regiao = ( 
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

# Evolução mensal de vendas (todos os anos juntos)
vendas_mensal = (
    df.groupby("mês")["Sales"]
    .sum()
    .reset_index()
    .sort_values("mês")
)

# Lucro vs Vendas por sub-categoria
lucro_subcategoria = (
    df.groupby("Sub-Category")[["Sales", "Profit"]]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
    .head(10)
    .reset_index()
)


# Distribuição de desconto por categoria
# (para mostrar o impacto do desconto no lucro)

# Top 10 produtos por faturamento
top_produtos = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# 5. criar dashboard (figura com 6 gráficos)


# Criamos uma figura grande com grade 3x2 (3 linhas, 2 colunas)
fig, axes = plt.subplots(3, 2, figsize=(16, 18))
fig.suptitle("Dashboard de Vendas — Superstore", fontsize=18, fontweight="bold", y=0.98)

# Paleta de cores consistente
cores = sns.color_palette("muted", 10)

# gráfico 1: Vendas por Categoria (barras horizontais)
ax1 = axes[0, 0]
bars = ax1.barh(
    vendas_categoria["Category"],
    vendas_categoria["Sales"],
    color=cores[:3],
    edgecolor="black",
)
ax1.set_title("Faturamento por Categoria")
ax1.set_xlabel("Total de Vendas (USD)")
ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
# adiciona os valores no topo das barras
for bar in bars:
    width = bar.get_width()
    ax1.text(
        width * 1.01, bar.get_y() + bar.get_height() / 2,
        f"${width:,.0f}", va="center", fontsize=10
    )
    ax1.set_xlim(0, vendas_categoria["Sales"].max() * 1.2)

    #  gráfico 2: Vendas por Região (barras verticais)
ax2 = axes[0, 1]
sns.barplot(
    data=vendas_regiao,
    x="Region", y="Sales",
    palette="muted", ax=ax2
)
ax2.set_title("Faturamento por Região")
ax2.set_xlabel("Região")
ax2.set_ylabel("Total de Vendas (USD)")
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
# Valor em cima de cada barra
for p in ax2.patches:
    ax2.annotate(
        f"${p.get_height():,.0f}",
        (p.get_x() + p.get_width() / 2, p.get_height()),
        ha="center", va="bottom", fontsize=10
    )

    # gráfico 3: Evolução mensal de vendas (linha)
ax3 = axes[1, 0]
ax3.plot(
   vendas_mensal["mês"],
   vendas_mensal["Sales"],
   marker="o", linewidth=2,
   color=cores[0], markersize=4
)
ax3.set_title("Evolução Mensal de Vendas")
ax3.set_xlabel("Mês")
ax3.set_ylabel("Total de Vendas (USD)")
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
# Mostrar só alguns rótulos no eixo X para não poluir
step = max(1, len(vendas_mensal) // 10)
ax3.set_xticks(range(0, len(vendas_mensal), step))
ax3.set_xticklabels(vendas_mensal["mês"].iloc[::step], rotation=45, ha="right")
ax3.fill_between(
    range(len(vendas_mensal)),
    vendas_mensal["Sales"],
    alpha=0.08, color=cores[0]
)
#  gráfico 4: Lucro vs Vendas por Sub-Categoria
ax4 = axes[1, 1]
# Colorir barras de lucro negativo em vermelho
cores_lucro = ["#d9534f" if v < 0 else cores[1] for v in lucro_subcategoria["Profit"]]
bars4 = ax4.barh(lucro_subcategoria["Sub-Category"], lucro_subcategoria["Profit"], color=cores_lucro)
ax4.set_title("Lucro por Sub-Categoria")
ax4.set_xlabel("Lucro Total (USD)")
ax4.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax4.axvline(0, color="black", linewidth=0.8, linestyle="--")
 
# ── gráfico 5: Top 10 Produtos por Faturamento ──
ax5 = axes[2, 0]
# Encurtar nomes muito longos para caber no gráfico
top_produtos["Produto Curto"] = top_produtos["Product Name"].str[:35]
sns.barplot(
    data=top_produtos,
    y="Produto Curto", x="Sales",
    palette="Blues_r", ax=ax5
)
ax5.set_title("Top 10 Produtos por Faturamento")
ax5.set_xlabel("Total de Vendas (USD)")
ax5.set_ylabel("")
ax5.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
 
# gráfico 6: Relação Desconto x Lucro (scatter) 
ax6 = axes[2, 1]
# Este gráfico mostra visualmente que descontos altos = prejuízo
scatter_data = df[["Discount", "Profit", "Category"]].copy()
categorias = scatter_data["Category"].unique()
for i, cat in enumerate(categorias):
    subset = scatter_data[scatter_data["Category"] == cat]
    ax6.scatter(
        subset["Discount"], subset["Profit"],
        alpha=0.3, s=15, label=cat, color=cores[i]
    )
ax6.axhline(0, color="red", linewidth=1, linestyle="--")
ax6.axvline(0.3, color="orange", linewidth=1, linestyle="--")
ax6.set_title("Desconto vs Lucro por Pedido")
ax6.set_xlabel("Desconto (%)")
ax6.set_ylabel("Lucro por Pedido (USD)")
ax6.legend(title="Categoria", fontsize=9)
ax6.text(0.31, ax6.get_ylim()[0] * 0.85, "30% desconto", color="orange", fontsize=9)
 

# 5. ajustes finais e salvar o dashboard

 
# Ajusta espaçamento entre os gráficos
plt.tight_layout(rect=[0, 0, 1, 0.96])
 
# Salva o dashboard como imagem PNG (ótimo para postar no LinkedIn)
plt.savefig("dashboard_vendas.png", dpi=150, bbox_inches="tight")
print("Dashboard salvo como 'dashboard_vendas.png'")
 
# Exibe na tela
plt.show()

