from rapidfuzz import process
import pandas as pd

df = pd.read_csv('../base_dados/filmes_imdb.csv')

def busca(palavra_chave):
    resultado = process.extract(query=palavra_chave, choices= df['Movie Name'])
    return resultado

if __name__ == '__main__':
    print(busca('God'))
    