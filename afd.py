class AFD:
    def __init__(self, estados, alfabeto, func_transicao, estado_inicial, estados_aceitacao):
        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.func_transicao = func_transicao
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = set(estados_aceitacao)
        
    def processar_cadeia(self, cadeia: str) -> bool:
        """
        simulacao do afd atraves da cadeia de entrada (string vinda do alfabeto definido pelo usuario)
        aqui sera verificado se a cadeia de simbolos e aceita ou rejeitada pelo afd gerado

        argumentos:
            cadeia (string): a cadeia de entrada a ser testada
        retorno:
            bool: true se a cadeia for aceita (terminar em estado de aceitação),
                  false caso contrario
        """
        estado_atual = self.estado_inicial
        
        for simbolo in cadeia:
            """
            sequencia de verificacoes:
            1. verificacao se o simbolo na cadeia fornecida pertence ao alfabeto
            2. devera buscar a transicao que corresponde ao estado atual e ao simbolo lido
                2.1 se a transicao for indefinida(None), a cadeia sera rejeitada
            """
            if simbolo not in self.alfabeto:
                print(f"---------------------")    
                print(f"Erro: Símbolo '{simbolo}' não pertence ao alfabeto definido.")
                print(f"Selecione simbolos do alfabeto fornecido: ")
                print(f"---------------------")    
                return False
            
            # 2
            proximo_estado = self.func_transicao.get((estado_atual, simbolo))
            # 2.1
            if proximo_estado is None:
                print(f"Erro: Transição indefinida para o estado '{estado_atual}' com o símbolo '{simbolo}'.")
                return False
            estado_atual = proximo_estado
        # apos processar toda a cadeia, verifica se o estado final esta no conjunto de aceitacao
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