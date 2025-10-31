class AFD:
    def __init__(self, estados, alfabeto, func_transicao, estado_inicial, estados_aceitacao):
        """
        inicializacao do afd

        args:  
            estados (list/set): o conjunto finito de estados (Q)
            alfabeto (list/set): o alfabeto finito (Σ).
            func_transicao (dict): a funcao de transicao (δ), mapeando (estado, símbolo) -> proximo_estado
            estado_inicial (str): o estado inicial (q0)
            estados_aceitacao (list/set): o conjunto de estados finais (F)
        """
        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.func_transicao = func_transicao
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = set(estados_aceitacao)
        
        # todo: adicionar validacao se é afn
        
    def processar_cadeia(self, cadeia: str) -> bool:
        """
        simulacao do afd atraves da cadeia de entrada (string vinda do alfabeto definido pelo usuario)
        aqui, sera verificado se a cadeia de simbolos e aceita ou rejeitada pelo afd gerado

        args:
            cadeia (string): a cadeia de entrada a ser testada.

        returns:
            bool: true se a cadeia for aceita (terminar em estado de aceitação),
                  false caso contrário.
        """
        estado_atual = self.estado_inicial
        
        for simbolo in cadeia:
            """
            aqui tera uma sequencia de duas verificacoes:
            1. devera verificar se o simbolo pertence ao alfabeto definido pelo usuario
            2. devera buscar a transicao que corresponde ao estado atual e ao simbolo lido
                2.1 se a transicao for indefinida, a cadeia sera rejeitada
            """

            # verificacao 1
            if simbolo not in self.alfabeto:
                print(f"Erro: Símbolo '{simbolo}' não pertence ao alfabeto definido.")
                return False
            
            # verificacao 2
            proximo_estado = self.func_transicao.get((estado_atual, simbolo))
            
            # verificacao 2.1
            if proximo_estado is None:
                print(f"Erro: Transição indefinida para o estado '{estado_atual}' com o símbolo '{simbolo}'.")
                return False
                
            estado_atual = proximo_estado
        # Após processar toda a cadeia, verifica se o estado final está no conjunto de aceitação
        return estado_atual in self.estados_aceitacao

    def imprimir(self):
        #imprimindo o afd
        print("\n--- Autômato Finito Determinístico (AFD) ---")
        print(f"Estados (Q): {sorted(list(self.estados))}")
        print(f"Alfabeto (Σ): {sorted(list(self.alfabeto))}")
        print(f"Estado Inicial (q0): {self.estado_inicial}")
        print(f"Estados Finais (F): {sorted(list(self.estados_aceitacao))}")
        print("Função de Transição (δ):")
        
        # imprimindo de forma ordenada as funcoes de transicao
        chaves_ordenadas = sorted(self.func_transicao.keys())
        for (estado, simbolo) in chaves_ordenadas:
            proximo = self.func_transicao[(estado, simbolo)]
            print(f"  δ({estado}, {simbolo}) = {proximo}")
        print("--------------------------------------------")