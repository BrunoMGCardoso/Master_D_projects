import streamlit as st
import pandas as pd
import busca

lista_filmes = pd.read_csv('base_dados/filmes_imdb.csv')

# --- Barra superior da página --- #

# Configuração do separador da página

st.set_page_config(
    page_title="Pesquisa de Filmes",         # Nome do separador da página
    page_icon="multimedia/page_icon.ico",    # Icon do separador da página
    layout="wide"                               
)



# --- Barra lateral --- #

with st.sidebar:
    st.sidebar.title('Menu')
    botao_lista = st.button('Lista de filmes')
    botao_imdb = st.link_button('IMDB', 'https://www.imdb.com')     # Link para a página oficial do IMDB
        
    if botao_lista:
        st.write('Filmes')
        st.dataframe(lista_filmes['Movie Name'], hide_index = True)



# --- Página principal --- #

botao_limpar = st.button('Limpar')                              # Botão para limpar o conteúdo de toda a página

if botao_limpar:
    st.empty()

# Título da página (Centrado, de cor azul com emoji do streamlit no início)

st.title(':streamlit: :blue[Top 1000 filmes do IMDB]', text_alignment = 'center')

# Breve descrição da página e a sua finalidade

st.write('''
         Este é um motor de busca onde podes procurar através de uma palavra-chave pelo filme que pretendes saber mais informações.
         ''')

# Divisão em duas colunas o corpo da página

col1, col2 = st.columns(2)



# --- Coluna de pesquisa --- #

# Na coluna 1 irão estar contidos um campo para inserir os termos da pesquisa e os resultados da pesquisa que dai resultarem.

with col1:
    # Inclusão da 'lista' para guardar os dados que nela entrem.

    # Iniciação de um dicionário para guardar.
    if 'lista_pesquisa' not in st.session_state:
        st.session_state.lista_pesquisa = {}
          
    # Lista com as opções de pesquisa.
    opcao = st.selectbox(label = 'Atributo para pesquisar filme', options = ['Ano', 'Avaliação','Nome'], index = None)      
        
    # Para a opção 'Ano', aparece uma barra para a seleção do ano pretendido.
    if opcao == 'Ano':                  
    
        ano = st.slider('Escolha o ano', lista_filmes['Year of Release'].min(), lista_filmes['Year of Release'].max())
    
    # Para a opção 'Avaliação', aparece uma barra para a seleção da Avaliação pretendida.   
    elif opcao == 'Avaliação':
        
        avaliacao = st.slider('Avaliação', 0.0, 10.0, value= (0.0, 10.0))

    # Para a opção 'Nome', aparece uma caixa de texto para digitar os termos a pesquisar.
    elif opcao == 'Nome':                 
           
        filme = st.text_input('Nome do Filme:', placeholder= 'Escreva aqui o nome do filme', width = 500)
        
    # Criação do botão para a pesquisa
    botao_pesquisar = st.button('Pesquisar', type='primary')

    try:
        
        # --- Carregando o botão 'Pesquisar'.
        if botao_pesquisar:
            
            # Limpa-se a lista que está na memória
            st.session_state.lista_pesquisa.clear()
            
            st.subheader('Resultado da Pesquisa:')
            
            # --- Quando se tem a opção Ano.        
            if opcao == 'Ano':
                
                st.write(f'Filmes de {ano}')
                
                st.dataframe(lista_filmes[lista_filmes['Year of Release'] == ano][['Movie Name', 'Movie Rating']], hide_index = True)
             
            # --- Quando se tem a opção Avaliação
            elif opcao == 'Avaliação':
                
                st.write(f'Avaliação entre {avaliacao[0]} e {avaliacao[1]}')
                
                # Seleção dos filmes entre a avaliação mínima & avaliação máxima, com a exibição das colunas nome do filme e avaliação.
                st.dataframe(lista_filmes[(lista_filmes['Movie Rating'] >= avaliacao[0]) & (lista_filmes['Movie Rating'] <= avaliacao[1])][['Movie Name', 'Movie Rating']], hide_index = True)
                
            # --- Quando se tem a opção Nome.
            elif opcao == 'Nome':
                
                # Para que os termos da pesquisa tenham pelo menos 3 caracteres.    
                if len(filme) >= 3:
                    
                    # Tupla dos resultados obtidos
                    resultado = busca.busca(filme)

                    for nome, corr, index in resultado:
                        st.write(f'✅ {nome} (Semelhança: {corr :.1f} %)')

                        # Armazenamento na memória dos resultados como dicionário onde a 'nome do filme : [correlação, index no dataframe]' 
                        st.session_state.lista_pesquisa[nome] = [corr, index]
                else:
                    # Mensagem de erro para quando os termos não são cumpridos.
                    st.error('Digite no mínimo 3 caracteres para a pesquisa')  
                      
    except NameError:
        st.write('''Opção inválida.
                \nEscolha uma opção''')



# --- Coluna de detalhes do filme --- #
        
with col2:
    
    # --- Por ano de lançamento --- #
    
    if opcao == 'Ano':
        
        nome_filme = st.selectbox('Lista de Filmes', lista_filmes[lista_filmes['Year of Release'] == ano], index = None, placeholder = 'Filme')
        
        if nome_filme:
            
            st.header(nome_filme)               # Nome do Filme
            
            st.subheader(int(lista_filmes[lista_filmes['Movie Name'] == nome_filme]['Year of Release']))                     # Ano do Filme
            
            st.write(f'Duração do filme: ***{int(lista_filmes[lista_filmes['Movie Name'] == nome_filme]['Watch Time'])}*** min')
            
            texto = lista_filmes.loc[lista_filmes[lista_filmes['Movie Name']== nome_filme].index, ['Description']] # Descrição do filme
            print(texto)
            
            st.write(lista_filmes[lista_filmes['Movie Name'] == nome_filme]['Description'])
    
    
    # --- Por Avaliação --- #
    
    if opcao == 'Avaliação':
        
        nome_filme = st.selectbox('Lista de Filmes', lista_filmes[(lista_filmes['Movie Rating'] >= avaliacao[0]) & (lista_filmes['Movie Rating'] <= avaliacao[1])], index = None, placeholder = 'Filme')
        
        if nome_filme:
            
            st.header(nome_filme)               # Nome do Filme
            
            st.subheader(int(lista_filmes[lista_filmes['Movie Name'] == nome_filme]['Year of Release']))                     # Ano do Filme
            
            st.write(f'Duração do filme: ***{int(lista_filmes[lista_filmes['Movie Name'] == nome_filme]['Watch Time'])}*** min')
            
            texto = lista_filmes.loc[lista_filmes[lista_filmes['Movie Name']== nome_filme].index, ['Description']] # Descrição do filme
            print(texto)
            
            st.write(lista_filmes[lista_filmes['Movie Name'] == nome_filme]['Description'])
    
    
    # --- Por Nome --- #
    
    if opcao == 'Nome':
        
        nome_filme = st.selectbox('Lista de filmes', st.session_state.lista_pesquisa, placeholder='Filme', index= None)
        
        if nome_filme != None:                  # Se o campo nome_filme estiver preenchido.
            st.header(nome_filme)               # Nome do Filme
            
            st.subheader(lista_filmes.iloc[st.session_state.lista_pesquisa[nome_filme][1]]['Year of Release'])                     # Ano do Filme
            
            st.write(f'Duração do filme: ***{lista_filmes.iloc[st.session_state.lista_pesquisa[nome_filme][1]]['Watch Time']}*** min')                   # Duração do filme

            st.write(f'Descrição: ":blue[{lista_filmes.iloc[st.session_state.lista_pesquisa[nome_filme][1]]['Description']}]"')                     # Descrição do filme