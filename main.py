import sys
from utils import ler_gramatica, escrever_etapa, escrever_intermediarias
from simplificacao import remover_inuteis_e_inalcancaveis, remover_producoes_vazias, substituir_producoes_unitarias
from cnf import normalizar_para_cnf

def simplificar_gramatica(producoes, f):
    escrever_etapa(1, "Gramática original", producoes, f)

    producoes = remover_inuteis_e_inalcancaveis(producoes)
    escrever_etapa(2, "Símbolos inúteis/inalcançáveis", producoes, f)

    producoes = remover_producoes_vazias(producoes)
    escrever_etapa(3, "Produções vazias", producoes, f)

    producoes = substituir_producoes_unitarias(producoes)
    escrever_etapa(4, "Substituição de produções unitárias", producoes, f)

    producoes_cnf, intermediarias = normalizar_para_cnf(producoes)

    escrever_etapa(5, "Normalização para CNF", producoes_cnf, f)
    escrever_intermediarias(intermediarias, f)

    return producoes_cnf

def main(glc_file, output_file):
    producoes = ler_gramatica(glc_file)
    with open(output_file, 'w') as f:
        producoes = simplificar_gramatica(producoes, f)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python main.py <arquivo_entrada.glc> <arquivo_saida.out>")
        sys.exit(1)

    glc_file = sys.argv[1]
    output_file = sys.argv[2]
    main(glc_file, output_file)