# em conversor.py

from afn import AFN, EPSILON
from afd import AFD
from typing import Set, Dict, Tuple, FrozenSet
"""
a importação da biblioteca typing auxilia na estruturacao dos dados, exemplo:
set -> conjunto imutavel de elementos de um tipo (conjunto de string)
frozenset -> conjunto imutavel (hashable) de elementos de um tipo (chave de um dicionario)
dict -> dicionario que mapeia chaves de um tipo para valores de outro tipo (estado, simbolo -> estado)
tuple -> tupla com dois tipos especificos (representacao do estado, simbolo)
"""

# Definimos tipos para maior clareza, especialmente para os "macro-estados" (conjuntos)
MacroEstado = Set[str]
MacroEstadoHashable = FrozenSet[str] # Usado como chave em dicionários/sets

def conversor_afn_para_afd(afn: AFN) -> AFD:
    """
    algoritmo de construcao de subconjuntos para converter um AFN para um AFD
    argumentos:
        afn (AFN): objeto AFN de entrada (contendo epsilon ou nao)
    retorno:
        afd: o objeto AFD equivalente
    """
    print("\n--- Iniciando a construcao de Subconjuntos (AFN -> AFD) ---")
    # --- 1. Inicialização ---
    
    # o alfabeto do AFD e o alfabeto do AFN (sem o epsilon)
    afd_alfabeto = afn.alfabeto
    # 1a. estado inicial do AFD: fecho-epsilon do estado inicial do AFN
    estado_inicial_afd: MacroEstado = afn.calcula_fecho_epsilon({afn.estado_inicial})
    # fila para os macro-estados a serem explorados (busca em largura - BFS)
    fila: list[MacroEstado] = [estado_inicial_afd]
    
    # Conjunto de macro-estados já descobertos/processados (usamos frozenset como chave)
    # Todos os estados do AFD serão frozensets no início
    estados_descobertos: Set[MacroEstadoHashable] = {frozenset(estado_inicial_afd)}
    
    # Dicionário temporário para as transições, usando frozensets como estados
    # Chave: (macro_estado_origem, simbolo) -> Valor: macro_estado_destino
    afd_transicoes_temp: Dict[Tuple[MacroEstadoHashable, str], MacroEstadoHashable] = {}

    # --- 2. Loop Principal: Descoberta de Estados e Transições ---
    
    while fila:
        # Pega o próximo macro-estado (conjunto de estados do AFN) para processar
        macro_estado_atual: MacroEstado = fila.pop(0)
        macro_estado_hash: MacroEstadoHashable = frozenset(macro_estado_atual)
        
        # Para cada símbolo do alfabeto (sem o épsilon)
        for simbolo in afd_alfabeto:
            # if simbolo == EPSILON: continue # O alfabeto do AFN deve ser passado sem o EPSILON
            
            # 2a. Cálculo da Transição Estendida (δ')
            
            # Passo A: Encontrar todos os destinos do AFN para o símbolo (Union of delta)
            estados_destino_simbolo: Set[str] = set()
            for estado_individual in macro_estado_atual:
                # O AFN retorna um conjunto de destinos para o par (estado, simbolo)
                destinos = afn.func_transicao.get((estado_individual, simbolo), set())
                estados_destino_simbolo.update(destinos)
                
            # Passo B: Aplicar o Fecho-Épsilon no resultado
            proximo_macro_estado: MacroEstado = afn.calcula_fecho_epsilon(estados_destino_simbolo)
            
            proximo_macro_estado_hash: MacroEstadoHashable = frozenset(proximo_macro_estado)
            
            # 2b. Adicionar a Transição
            afd_transicoes_temp[(macro_estado_hash, simbolo)] = proximo_macro_estado_hash
            
            # 2c. Gerenciar a Fila
            if proximo_macro_estado_hash not in estados_descobertos:
                estados_descobertos.add(proximo_macro_estado_hash)
                fila.append(proximo_macro_estado)

    # --- 3. Finalização: Renomeação e Definição do AFD ---
    
    # 3a. Mapeamento de Nomes: {frozenset} -> 'S0', 'S1', ...
    # Ordenamos os estados descobertos para garantir nomes consistentes (ex: S0 sempre será o inicial)
    estados_ordenados = sorted(list(estados_descobertos), key=lambda x: str(x))
    mapa_nomes = {fs: f"S{i}" for i, fs in enumerate(estados_ordenados)}
    
    print(f"Descobertos {len(estados_descobertos)} estados para o AFD.")

    # 3b. Tradução das Estruturas para os Nomes Finais (strings)
    
    afd_estados_nomes = set(mapa_nomes.values())
    afd_estado_inicial_nome = mapa_nomes[frozenset(estado_inicial_afd)]
    
    afd_transicoes_finais: Dict[Tuple[str, str], str] = {}
    for (origem_fs, simbolo), destino_fs in afd_transicoes_temp.items():
        nome_origem = mapa_nomes[origem_fs]
        nome_destino = mapa_nomes[destino_fs]
        afd_transicoes_finais[(nome_origem, simbolo)] = nome_destino
        
    afd_estados_finais_nomes: Set[str] = set()
    for macro_estado_fs in estados_descobertos:
        # Regra do estado final: O macro-estado é final se contiver pelo menos um estado final do AFN
        # Precisamos converter o frozenset de volta para set para usar 'any' com o conjunto de aceitação do AFN
        macro_estado_set = set(macro_estado_fs) 
        
        if any(estado_afn in afn.estados_aceitacao for estado_afn in macro_estado_set):
            afd_estados_finais_nomes.add(mapa_nomes[macro_estado_fs])
            
    # 4. Criar e retornar o objeto AFD final
    return AFD(
        estados=afd_estados_nomes,
        alfabeto=afd_alfabeto,
        func_transicao=afd_transicoes_finais,
        estado_inicial=afd_estado_inicial_nome,
        estados_aceitacao=afd_estados_finais_nomes
    )