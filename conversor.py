from afn import AFN, EPSILON
from afd import AFD
from typing import Set, Dict, Tuple, FrozenSet
"""
a importação da biblioteca typing auxilia na estruturacao dos dados, exemplo:
set -> conjunto imutavel de elementos de um tipo (conjunto de string)
frozenset -> conjunto imutavel (hashable) de elementos de um tipo (chave de um dicionario)
dict -> dicionario que mapeia chaves de um tipo para valores de outro tipo (estado, simbolo -> estados)
tuple -> tupla com dois tipos especificos (representacao do estado, simbolo)
"""
MacroEstado = Set[str] # permite adicionar e remover elementos (set)
MacroEstadoHashable = FrozenSet[str] # nao permite alteracao (frozenset)

def conversor_afn_para_afd(afn: AFN) -> AFD:
    """
    algoritmo de construcao de subconjuntos para converter um AFN para um AFD
    argumentos:
        afn (AFN): objeto AFN de entrada (contendo epsilon ou nao)
    retorno:
        afd: o objeto AFD equivalente
    """
    print("=============================================================")
    print("   Iniciando a conversão do AFN para seu equivalente AFD    ")
    print("=============================================================")
    
    afd_alfabeto = afn.alfabeto
    estado_inicial_afd: MacroEstado = afn.calcula_fecho_epsilon({afn.estado_inicial})
    # fila para os macro-estados a serem explorados (busca em largura - BFS)
    fila: list[MacroEstado] = [estado_inicial_afd]
    
    # conjunto de macro-estados ja descobertos/processados (usando frozenset como chave)
    # todos os estados do AFD serao frozensets no inicio
    estados_descobertos: Set[MacroEstadoHashable] = {frozenset(estado_inicial_afd)}
    
    # dicionario temporario para as transicoes, usando frozensets como estados
    # chave: (macro_estado_origem, simbolo) -> valor: macro_estado_destino
    afd_transicoes_temp: Dict[Tuple[MacroEstadoHashable, str], MacroEstadoHashable] = {}

    # loop principal: descoberta de estados e transicoes
    while fila:
        # pega o proximo macro-estado (conjunto de estados no AFN) e processa
        macro_estado_atual: MacroEstado = fila.pop(0)
        macro_estado_hash: MacroEstadoHashable = frozenset(macro_estado_atual)
        
        for simbolo in afd_alfabeto:
            # if simbolo == EPSILON: continue 
            # o alfabeto do AFN deve ser passado sem o EPSILON
            # 1- encontrar todos os destinos do AFN para o simbolo
            estados_destino_simbolo: Set[str] = set()
            for estado_individual in macro_estado_atual:
                # O AFN retorna um conjunto de destinos para o par (estado, simbolo)
                destinos = afn.func_transicao.get((estado_individual, simbolo), set())
                estados_destino_simbolo.update(destinos)
                
            # 2- aplicar o fecho-epsilon no resultado
            proximo_macro_estado: MacroEstado = afn.calcula_fecho_epsilon(estados_destino_simbolo)
            
            proximo_macro_estado_hash: MacroEstadoHashable = frozenset(proximo_macro_estado)
            
            # adciona a transicao
            afd_transicoes_temp[(macro_estado_hash, simbolo)] = proximo_macro_estado_hash

            if proximo_macro_estado_hash not in estados_descobertos:
                estados_descobertos.add(proximo_macro_estado_hash)
                fila.append(proximo_macro_estado)
    
    # definicao AFD: {frozenset} -> 'S0', 'S1', ...
    # apresentacao dos estados na forma ordenada
    estados_ordenados = sorted(list(estados_descobertos), key=lambda x: str(x))
    mapa_nomes = {fs: f"S{i}" for i, fs in enumerate(estados_ordenados)}
    
    print(f"O AFD equivalente gerado contem {len(estados_descobertos)} estados.")
    
    afd_estados_nomes = set(mapa_nomes.values())
    afd_estado_inicial_nome = mapa_nomes[frozenset(estado_inicial_afd)]
    
    afd_transicoes_finais: Dict[Tuple[str, str], str] = {}
    for (origem_fs, simbolo), destino_fs in afd_transicoes_temp.items():
        nome_origem = mapa_nomes[origem_fs]
        nome_destino = mapa_nomes[destino_fs]
        afd_transicoes_finais[(nome_origem, simbolo)] = nome_destino
        
    afd_estados_finais_nomes: Set[str] = set()
    for macro_estado_fs in estados_descobertos:
        # regra do estado final: o macro-estado e final se contiver pelo menos um estado final do AFN
        # convertendo o frozenset de volta para set para usar 'any' com o conjunto de aceitacao do AFN
        macro_estado_set = set(macro_estado_fs) 
        
        if any(estado_afn in afn.estados_aceitacao for estado_afn in macro_estado_set):
            afd_estados_finais_nomes.add(mapa_nomes[macro_estado_fs])
            
    # cria e retona o objeto AFD
    return AFD(
        estados=afd_estados_nomes,
        alfabeto=afd_alfabeto,
        func_transicao=afd_transicoes_finais,
        estado_inicial=afd_estado_inicial_nome,
        estados_aceitacao=afd_estados_finais_nomes
    )