import sys

def ler_gramatica(file_path):
    producoes = {}
    with open(file_path, 'r') as f:
        for linha in f:
            if '->' in linha:
                esquerda, direita = linha.strip().replace(' ', '').split('->')
                producoes[esquerda] = direita.split('|')
    return producoes

def remover_vazias(producoes):
    vazios = {s for s, v in producoes.items() if '@' in v}
    while vazios:
        vazio = vazios.pop()
        novas_producoes = {}
        for s, v in producoes.items():
            novas_v = []
            for prod in v:
                if vazio in prod:
                    novas_v.append(prod.replace(vazio, ''))
            novas_v.extend(v)
            novas_producoes[s] = list(set(novas_v))
        producoes = {s: [p for p in v if p != '@'] for s, v in novas_producoes.items()}
        novos_vazios = {s for s, v in producoes.items() if '@' in v}
        if novos_vazios == vazios:
            break
        vazios = novos_vazios
    return producoes

def substituir_unitarias(producoes):
    while True:
        unitarias = {s: [p for p in v if len(p) == 1 and p.isupper()] for s, v in producoes.items()}
        if not any(unitarias.values()):
            break
        for s, v in unitarias.items():
            for u in v:
                if u in producoes:
                    producoes[s].extend(producoes[u])
            producoes[s] = [p for p in producoes[s] if p not in v]
    return producoes

def remover_inuteis(producoes):
    start_symbol = next(iter(producoes))
    terminais = {s for s, v in producoes.items() if any(all(c.islower() for c in p) for p in v)}
    while True:
        novos_terminais = terminais | {s for s, v in producoes.items() if all(any(c in terminais for c in p if c.isupper()) for p in v)}
        if novos_terminais == terminais:
            break
        terminais = novos_terminais
    producoes = {s: v for s, v in producoes.items() if s in terminais or s == start_symbol}
    producoes = {s: [p for p in v if all(c in terminais or c.islower() for c in p)] for s, v in producoes.items()}
    return producoes

def escrever_etapa(etapa, descricao, producoes, f):
    f.write(f"\nEtapa {etapa}: {descricao}\n")
    for s, v in producoes.items():
        f.write(f"{s} -> {' | '.join(v)}\n")

def simplificar_gramatica(producoes, f):
    escrever_etapa(1, "Gramática original", producoes, f)

    producoes = remover_inuteis(producoes)
    escrever_etapa(2, "Símbolos inúteis/inalcançáveis", producoes, f)

    producoes = remover_vazias(producoes)
    escrever_etapa(3, "Produções vazias", producoes, f)

    producoes = substituir_unitarias(producoes)
    escrever_etapa(4, "Substituição de produções unitárias", producoes, f)

    return producoes

def main(glc_file, output_file):
    producoes = ler_gramatica(glc_file)
    with open(output_file, 'w') as f:
        producoes = simplificar_gramatica(producoes, f)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python simplificacao.py <arquivo_da_gramatica.glc> <arquivo_de_saida.out>")
        sys.exit(1)

    glc_file = sys.argv[1]
    output_file = sys.argv[2]
    main(glc_file, output_file)
