from rapidfuzz import process
import pandas as pd
import streamlit as st

dframe = pd.read_csv('base_dados/filmes_imdb.csv')

def busca(palavra_chave:str, data_frame:object, col_name:str, semelhanca:int=0):
    '''Docstrings
    Comparação entre termos.
    
    Procura os termos (palavra-chave) numa determinada coluna (col_df) do ficheiro (data_frame) e retorna a similaridade comparando-os.
    
    Args: 
    
        palavra-chave (str): Texto/Palavras a comparar com a    base de dados.
        
        data_frame (dataframe/object): Ficheiro carregado com a base de dados a comparar
        
        col_df (str): Nome da coluna dentro do dataframe que contém os dados
        
        semelhanca (int): Percentagem de semelhança mínima que os termos terão que apresentar
        
    Returns:
    
        tuple: tupla com 3 valores, (correspondência, percentagem de semelhança, index no ficheiro original).
    '''
    
    resultado = process.extract(query=palavra_chave, choices= data_frame[col_name], score_cutoff = semelhanca)
    
    return resultado

def listagem(indices, data_frame):
    '''Docstrings
    Listagem de filmes pesquisados
    
    Através dos valores dos indices (indices), vai pesquisar no dataframe (data_frame) os nomes dos filmes, returnando um dicionário de estrutura 'filme : indice'
    
    Args:
    
        indices (list): lista de valores inteiros com os indices a cruzar.
        
        data_frame (object): Ficheiro onde estão os dados a cruzar.
        
    Return:

        dictionary: dicionário com a estrutura 'Filme : Indíce'
    '''
    for indice in indices:
        st.session_state.resultado_pesquisa[data_frame.iloc[indice]['Movie Name']] = indice
    
    return st.session_state.resultado_pesquisa

def mostrar_filmes(lista):
    
    with st.container(height=300):
        
        for item in lista:
            st.write(item)
            
if __name__ == '__main__':
    print(busca('God', dframe, 'Movie Name', 80))
    