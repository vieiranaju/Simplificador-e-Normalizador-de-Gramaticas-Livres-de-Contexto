import sys
from simplificador_glc import ler_gramatica, simplificar_gramatica, escrever_etapa

def transformar_comprimento_maior_igual_dois(producoes):
    novas_producoes = {}
    contador = 1
    terminais = {s: s for s in set(''.join(sum(producoes.values(), []))) if s.islower()}
    visited = set()  # Track processed non-terminals

    for esquerda, direitas in producoes.items():
        novas_direitas = []
        for direita in direitas:
            if len(direita) == 1 and direita.islower():
                novas_direitas.append(direita)
            else:
                nova_direita = direita
                for terminal in set(direita) & set(terminais.keys()):
                    if terminal not in novas_producoes and terminal not in visited:
                        nova_variavel = f'T{contador}'
                        contador += 1
                        terminais[terminal] = nova_variavel
                        novas_producoes[nova_variavel] = [terminal]
                        visited.add(terminal)  
                    nova_direita = nova_direita.replace(terminal, terminais[terminal])
                
                if any(esquerda in direita for direita in novas_producoes.values()):
                    novas_direitas.append(direita)
                else:
                    while len(nova_direita) > 2:
                        nova_variavel = f'X{contador}'
                        contador += 1
                        if nova_variavel not in visited:
                            novas_producoes[nova_variavel] = [nova_direita[-2:]]
                            visited.add(nova_variavel) 
                        nova_direita = nova_direita[:-2] + nova_variavel
                    novas_direitas.append(nova_direita)
        novas_producoes[esquerda] = novas_direitas

    return novas_producoes

def transformar_comprimento_maior_igual_tres(producoes):
    novas_producoes = {}
    contador = 1
    visited = set() 

    for esquerda, direitas in producoes.items():
        novas_direitas = []
        for direita in direitas:
            while len(direita) > 2:
                nova_variavel = f'X{contador}'
                contador += 1
                if nova_variavel not in visited:
                    novas_producoes[nova_variavel] = [direita[-2:]]
                    visited.add(nova_variavel)  # Mark non-terminal as processed
                direita = direita[:-2] + nova_variavel
            novas_direitas.append(direita)
        novas_producoes[esquerda] = novas_direitas

    return novas_producoes

def normalizar_gramatica(producoes, f):
    producoes = transformar_comprimento_maior_igual_dois(producoes)
    escrever_etapa(5, "Transformação do comprimento maior ou igual a dois", producoes, f)

    producoes = transformar_comprimento_maior_igual_tres(producoes)
    escrever_etapa(6, "Transformação do comprimento maior ou igual a três", producoes, f)

    return producoes

def main(glc_file, output_file):
    producoes = ler_gramatica(glc_file)
    with open(output_file, 'w') as f:
        producoes = simplificar_gramatica(producoes, f)
        producoes = normalizar_gramatica(producoes, f)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python fnc_glc.py <arquivo_da_gramatica.glc> <arquivo_de_saida.out>")
        sys.exit(1)

    glc_file = sys.argv[1]
    output_file = sys.argv[2]
    main(glc_file, output_file)