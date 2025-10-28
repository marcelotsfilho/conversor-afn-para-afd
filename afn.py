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
        Calcula o fecho-épsilon (epsilon-closure) para um conjunto de estados no AFN.

        O fecho-épsilon de um conjunto S é o conjunto de todos os estados alcançáveis
        a partir de qualquer estado em S seguindo zero ou mais transições-épsilon (&).

        Utiliza o algoritmo de busca em profundidade (DFS) com uma pilha
        para percorrer todos os estados alcançáveis por transições vazias.

        Args:
            estados (set): O conjunto inicial de estados do AFN.

        Returns:
            set: O conjunto completo de estados que inclui os estados originais
                 mais todos os estados alcançáveis via transições-épsilon.
        """
        fecho = set(estados)
        pilha = list(estados)
        
        while pilha:
            estado_atual = pilha.pop()
            
            # Obtém os estados alcançáveis a partir do estado_atual via EPSILON (&)
            for proximo_estado in self.func_transicao.get((estado_atual, EPSILON), set()):
                if proximo_estado not in fecho:
                    fecho.add(proximo_estado)
                    pilha.append(proximo_estado)
                    
        return fecho
    
    