EPSILON = ''

class AFN:
    def __init__(self, estados, alfabeto, func_transicao, estado_inicial, estados_aceitacao):
        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.func_transicao = func_transicao
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = set(estados_aceitacao)

    """
    o metodo calcula_fecho epsilon recebe um conjunto de estados e retorna o fecho-epsilon desses estados
    utilizando uma abordagem de busca em profundidade (dfs) para explorar todas as transicoes
    """
    def calcula_fecho_epsilon(self, estados: set) -> set:
        """
        calcula o fecho-epsilon (epsilon-closure) para um conjunto de estados no AFN

        o fecho-epsilon de um conjunto S e o conjunto de todos os estados alcancaveis
        a partir de qualquer estado em S seguindo zero ou mais transicoes-epsilon (&).

        utiliza o algoritmo de busca em profundidade (DFS) com uma pilha
        para percorrer todos os estados alcancaveis por transicoes vazias

        argumentos:
            estados (set): o conjunto inicial de estados do AFN.

        retorno:
            set: o conjunto completo de estados que inclui os estados originais
                 mais todos os estados alcancaveis via transicoes-epsilon.
        """
        fecho = set(estados)
        pilha = list(estados)
        
        while pilha:
            estado_atual = pilha.pop()
            
            # obtem os estados alcancaveis a partir do estado_atual via EPSILON (&)
            for proximo_estado in self.func_transicao.get((estado_atual, EPSILON), set()):
                if proximo_estado not in fecho:
                    fecho.add(proximo_estado)
                    pilha.append(proximo_estado)
                    
        return fecho
    
    