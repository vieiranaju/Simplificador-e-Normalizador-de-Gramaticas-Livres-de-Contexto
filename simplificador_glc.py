import sys

def ler_gramatica(file_path):
    producoes = {}
    with open(file_path, 'r') as f:
        for linha in f:
            if '->' in linha:
                esquerda, direita = linha.strip().replace(' ', '').split('->')
                producoes[esquerda] = direita.split('|')
    return producoes

def remover_producoes_vazias(producoes):
    vazios = {k for k, v in producoes.items() if '@' in v}
    while vazios:
        vazio = vazios.pop()
        for k, v in producoes.items():
            novas_producoes = []
            for prod in v:
                if vazio in prod:
                    novas_producoes.append(prod.replace(vazio, ''))
            producoes[k].extend(novas_producoes)
            producoes[k] = [prod for prod in producoes[k] if prod != '@']
        producoes = {k: list(set(v)) for k, v in producoes.items()}
    return producoes

def substituicao_de_producoes(producoes):
    unitarias = {k: [p for p in v if len(p) == 1 and p.isupper()] for k, v in producoes.items()}
    while any(unitarias.values()):
        for k, v in unitarias.items():
            for u in v:
                if u not in producoes[k]:  
                    producoes[k].extend(producoes[u])
            producoes[k] = [p for p in producoes[k] if p not in v]
        unitarias = {k: [p for p in v if len(p) == 1 and p.isupper()] for k, v in producoes.items()}
    return producoes

def remover_simbolos_inuteis(producoes):
    start_symbol = next(iter(producoes))  
    terminais = {k for k, v in producoes.items() if any(all(c.islower() for c in p) for p in v)}
    while True:
        novos_terminais = terminais | {k for k, v in producoes.items() if all(any(c in terminais for c in p if c.isupper()) for p in v)}
        if novos_terminais == terminais:
            break
        terminais = novos_terminais
    producoes = {k: v for k, v in producoes.items() if k in terminais or k == start_symbol}  
    producoes = {k: [p for p in v if all(c in terminais or c.islower() for c in p)] for k, v in producoes.items()}
    return producoes

def escrever_etapa(etapa, descricao, producoes, f):
    f.write(f"\nEtapa {etapa}: {descricao}\n")
    for k, v in producoes.items():
        f.write(f"{k} -> {' | '.join(v)}\n")

def simplificar_gramatica(producoes, f):
    escrever_etapa(1, "Gramática original", producoes, f)

    producoes = remover_simbolos_inuteis(producoes)
    escrever_etapa(2, "Símbolos inúteis/inalcançáveis", producoes, f)

    producoes = remover_producoes_vazias(producoes)
    escrever_etapa(3, "Produções vazias", producoes, f)

    producoes = substituicao_de_producoes(producoes)
    escrever_etapa(4, "Substituição de produções", producoes, f)

    return producoes

def main(glc_file, output_file):
    producoes = ler_gramatica(glc_file)
    with open(output_file, 'w') as f:
        producoes = simplificar_gramatica(producoes, f)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python glc_simplificador.py <arquivo_da_gramatica.glc> <arquivo_de_saida.out>")
        sys.exit(1)

    glc_file = sys.argv[1]
    output_file = sys.argv[2]
    main(glc_file, output_file)