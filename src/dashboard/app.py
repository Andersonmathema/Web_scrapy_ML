import streamlit as st
import pandas as pd
import sqlite3

# Conectar ao DB
conn = sqlite3.connect('../data/quotes.db')

# Carregar dados da tabela 'mercadolivre_items' em um DataFrame pandas
df = pd.read_sql("SELECT * FROM mercadolivre_items", conn)

# Fecha conexão
conn.close()

# Titulo do app
st.title('Pesquisa de mercado do ML')

# Melhorar layout com KPIs
st.subheader('KPIs principais do sistema')
col1, col2, col3 = st.columns(3)

# KPI 1: Numeros total de itens
total_itens = df.shape[0]
col1.metric(label='Número Total de Itens', value=total_itens)

# KPI 2: Numero de marcas únicas
unique_brands = df['brand'].nunique()
col2.metric(label="Número de Marcas Únicas", value=unique_brands)

# KPI 3: Preço Médio novo (em reais)
average_new_price = df['new_price'].mean()
col3.metric(label="Preço Médio Novo (R$)", value=f"{average_new_price:.2f}")

# Quais marcas são as mais encontradas até a 10ª página
st.subheader("Marcas mais encontradas até a 10ª página")
col1, col2 = st.columns([4,2]) # Tem 6 partes, proporcional 4/2
top_10_page_brands = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10_page_brands)
col2.write(top_10_page_brands)

# Preço médio por marca
st.subheader('Preço Médio por Marca')
col1, col2 = st.columns([4,2])
average_price_by_brand = df.groupby('brand')['new_price'].mean().sort_values(ascending=False)
col1.bar_chart(average_price_by_brand)
col2.write(average_price_by_brand)

# Qual a satisfação por marca
st.subheader('Satisfação por marca')
col1, col2 = st.columns([4, 3])
df_non_zero_reviews = df[df['reviews_rating_number'] > 0]
satisfaction_by_brand = df_non_zero_reviews.groupby('brand')['reviews_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)
#st.write(df)
