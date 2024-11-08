import pandas as pd
import networkx as nx
import streamlit as st

# Ler os dados do Excel
caminho_excel = 'Base.xlsx'
df = pd.read_excel(caminho_excel)

# Padronizar nomes das cidades
df['ORIGEM'] = df['ORIGEM'].str.strip().str.upper()
df['DESTINO'] = df['DESTINO'].str.strip().str.upper()

# Construir o grafo não direcionado com atributos nas arestas
G = nx.Graph()

for _, row in df.iterrows():
    origem = row['ORIGEM']
    destino = row['DESTINO']
    prefixo = row['PREFIXO']
    linha = row['LINHA']
    G.add_edge(origem, destino, prefixo=prefixo, linha=linha)

# Função para encontrar rotas com detalhes
def encontrar_rotas_detalhadas(grafo, origem, destino, max_conexoes=3):
    try:
        # Encontrar todas as rotas simples com o limite de conexões
        rotas_cidades = list(nx.all_simple_paths(grafo, source=origem, target=destino, cutoff=max_conexoes))

        rotas_detalhadas = []
        for rota in rotas_cidades:
            detalhes_rota = []
            for i in range(len(rota) - 1):
                cidade_origem = rota[i]
                cidade_destino = rota[i + 1]
                dados_aresta = grafo.get_edge_data(cidade_origem, cidade_destino)
                detalhes_rota.append({
                    'origem': cidade_origem,
                    'destino': cidade_destino,
                    'prefixo': dados_aresta['prefixo'],
                    'linha': dados_aresta['linha']
                })
            rotas_detalhadas.append(detalhes_rota)
        return rotas_detalhadas
    except nx.NetworkXNoPath:
        return []

# Interface com o usuário usando Streamlit

# Adicionar o logo da empresa no canto superior esquerdo
logo_path = 'logo.jpg'  # Certifique-se de que o arquivo do logo está neste caminho
st.image(logo_path, width=150)

st.title("Pesquisa de Rotas")

# Entrada de Origem e Destino
origem = st.text_input("Origem:").strip().upper()
destino = st.text_input("Destino:").strip().upper()

# Selecionar o número máximo de conexões
max_conexoes = st.selectbox("Número máximo de conexões:", options=[1, 2, 3, 4, 5], index=2)

if st.button("Pesquisar"):
    if origem not in G.nodes():
        st.error(f"A cidade de origem '{origem}' não está na base de dados.")
    elif destino not in G.nodes():
        st.error(f"A cidade de destino '{destino}' não está na base de dados.")
    else:
        rotas_detalhadas = encontrar_rotas_detalhadas(G, origem, destino, max_conexoes)

        if rotas_detalhadas:
            st.write(f"Rotas encontradas de {origem} para {destino} (máximo de {max_conexoes} conexões):")
            for i, rota in enumerate(rotas_detalhadas, 1):
                st.write(f"**Rota {i}:**")
                for trecho in rota:
                    texto_trecho = f"- {trecho['origem']} -> {trecho['destino']} | Prefixo: {trecho['prefixo']} | Linha: {trecho['linha']}"
                    st.write(texto_trecho)
        else:
            st.write(f"Nenhuma rota encontrada de {origem} para {destino} com até {max_conexoes} conexões.")
