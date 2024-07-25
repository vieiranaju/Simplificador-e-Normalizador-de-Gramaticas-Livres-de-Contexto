import csv
import sys

def ler_gramatica(file_path):
    producoes = {}
    with open(file_path, 'r') as f:
        for linha in f:
            if '->' in linha:
                linha = linha.replace(' ', '')
                esquerda, direita = linha.strip().split('->')
                producoes[esquerda] = direita.split('|')
    return producoes

def main(glc_file, output_file):
    producoes = ler_gramatica(glc_file)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python glc_simplificador.py <arquivo_da_gramatica.glc> <arquivo_de_saida.out>")
        sys.exit(1)
    
    glc_file = sys.argv[1]
    output_file = sys.argv[2]
    main(glc_file, output_file)