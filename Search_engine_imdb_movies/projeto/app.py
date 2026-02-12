import streamlit as st
import pandas as pd
import busca

df_filmes = pd.read_csv('base_dados/filmes_imdb.csv')

# --- Barra superior da página --- #

# Configuração do separador da página

st.set_page_config(
    page_title="Pesquisa de Filmes",         # Nome do separador da página
    page_icon="multimedia/page_icon.ico",    # Icon do separador da página
    layout="wide"                            # Disposição da página á largura total   
)

# --- Barra lateral --- #

with st.sidebar:
    st.sidebar.title('Menu')
    botao_lista_de_filmes = st.button('Lista de filmes')
    botao_imdb = st.link_button('IMDB', 'https://www.imdb.com')     # Link para a página oficial do IMDB
        
    if botao_lista_de_filmes:
        st.write('Filmes')
        st.dataframe(df_filmes['Movie Name'], hide_index = True, )

# --- Página principal --- #

botao_limpar = st.button('Limpar')                              # Botão para limpar o conteúdo de toda a página

if botao_limpar:
    st.empty()

# Título da página (Centrado, de cor azul com emoji do streamlit no início)

st.title(':streamlit: :blue[Top 1000 filmes do IMDB]', text_alignment = 'center')

# Breve descrição da página e a sua finalidade

st.write('Este é um motor de busca onde podes procurar através de uma palavra-chave pelo filme que pretendes saber mais informações.')

# Divisão em duas colunas o corpo da página

col1, col2 = st.columns(2)

# --- Coluna de pesquisa --- #

# Na coluna 1 irão estar contidos um campo para inserir os termos da pesquisa e os resultados da pesquisa que dai resultarem.

with col1:
    # Inclusão da 'lista' para guardar os dados que nela entrem.

    # Iniciação de um dicionário para guardar.
    if 'resultado_pesquisa' not in st.session_state:
        st.session_state.resultado_pesquisa = {}

    filmes = st.session_state.resultado_pesquisa
          
    # Lista com as opções de pesquisa.
    opcao_pesquisa = st.selectbox(label = 'Atributo para pesquisar filme', options = ['Ano', 'Avaliação','Nome'], index = None, placeholder= 'Selecione uma opção')      
        
    # Para a opção 'Ano', aparece uma barra para a seleção do ano pretendido.
    if opcao_pesquisa == 'Ano':                  
    
        ano = st.slider(label = 'Escolha o ano', min_value = df_filmes['Year of Release'].min(), max_value = df_filmes['Year of Release'].max())
    
    # Para a opção 'Avaliação', aparece uma barra para a seleção da Avaliação pretendida.   
    elif opcao_pesquisa == 'Avaliação':
        
        avaliacao = st.slider(label = 'Avaliação', min_value = 0.0, max_value = 10.0, value = (0.0, 10.0))

    # Para a opção 'Nome', aparece uma caixa de texto para digitar os termos a pesquisar.
    elif opcao_pesquisa == 'Nome':                 
           
        nome_filme = st.text_input('Nome do Filme:', placeholder= 'Escreva aqui o nome do filme', width = 500)
        
        semelhanca_min = st.slider('Semelhança mínima', 0, 100)
        
    # Criação do botão para a pesquisa
    botao_pesquisar = st.button('Pesquisar', type='primary')
    
    try:
        
        # --- Carregando no botão 'Pesquisar'.
    
        if botao_pesquisar:
            # Limpa-se a lista que está na memória
            filmes.clear()
            
            st.subheader('Resultado da Pesquisa:')
            
            # --- Quando se tem a opção Ano.        
            if opcao_pesquisa == 'Ano':
                
                st.write(f'**:blue[Filmes de {ano}]**')
                
                # Indices dos filmes resultantes da pesquisa.
                indices_filmes = df_filmes[df_filmes['Year of Release'] == ano].index
                
                # Dicionário com nome do filme (Key) e indice no dataframe (Value)

                lista_filmes = busca.listagem(indices_filmes, df_filmes)
                
                
                busca.mostrar_filmes(lista_filmes)

            # --- Quando se tem a opção Avaliação
            elif opcao_pesquisa == 'Avaliação':
                
                st.write(f'Avaliação entre {avaliacao[0]} e {avaliacao[1]}')
                
                # Seleção dos filmes entre a avaliação mínima & avaliação máxima, com a exibição das colunas nome do filme e avaliação.

                indices_filmes = df_filmes[(df_filmes['Movie Rating'] >= avaliacao[0]) & (df_filmes['Movie Rating'] <= avaliacao[1])].index
                
                lista_filmes = busca.listagem(indices_filmes, df_filmes)
                
                busca.mostrar_filmes(lista_filmes)    
                
            # --- Quando se tem a opção Nome.
            elif opcao_pesquisa == 'Nome':
            
                # Para que os termos da pesquisa tenham pelo menos 3 caracteres. 
                # Adiciona-se o método strip para eliminar os espaços.    
                if len(nome_filme.strip()) >= 3:
                    
                    st.warning('ATENÇÃO: O texto é sensivel a maiúsculas!')
                    
                    # Tupla dos resultados obtidos
                    resultado = busca.busca(nome_filme, df_filmes, 'Movie Name', semelhanca = semelhanca_min)
                    
                    for nome, corr, index in resultado:
                        st.write(f'✅ {nome} (Semelhança: {corr :.1f} %)')

                        # Armazenamento na memória dos resultados como dicionário onde a 'nome do filme : [correlação, index no dataframe]' 
                        filmes[nome] = index
                    
                else:
                    # Mensagem de erro para quando os termos não são cumpridos.
                    st.error('Digite no mínimo 3 caracteres para a pesquisa')  
                
    except NameError:
        st.write('''Opção inválida.
                \nEscolha uma opção''')

    filmes = st.session_state.resultado_pesquisa

# --- Coluna de detalhes do filme --- #
        
with col2:
    
    filme = st.selectbox(label = '**Lista de Filmes**',options = filmes, index = None, placeholder = 'Filme')
    
    if filme is not None:
        
        st.header(filme)
        
        ano_filme = str(df_filmes.loc[filmes[filme], 'Year of Release'])
        
        duracao_filme = str(df_filmes.loc[filmes[filme], 'Watch Time'])
        
        descricao_filme = str(df_filmes.loc[filmes[filme], 'Description'])
    
        st.subheader(ano_filme)
        
        st.write(f'**Duração:** {duracao_filme} min')
        
        st.write(f'**Descrição**: \n\r{descricao_filme}')
    
    else:
        st.warning('Selecione um filme para ver os seus detalhes')