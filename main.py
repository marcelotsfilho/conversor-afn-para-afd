# em main.py

from afn import AFN, EPSILON
from conversor import conversor_afn_para_afd

def obter_definicao_afn_usuario():
    """
    Função para coletar os dados do AFN do usuário e retornar um objeto AFN.
    """
    print("--- Definição do AFN ---")
    # aviso para informar ao usuario que como deve ser preenchido a transicao epsilon
    print(f"(Atencao, use '{EPSILON}' para transicoes epsilon)")
    
    # a seguir consta a coleta de dados do AFN 
    estados = input("Digite os estados do automato (separados por espaço): ").strip().split()
    alfabeto = input("Digite o alfabeto do automato (separados por espaço, sem epsilon): ").strip().split()
    # verificacao se o estado fornecido como inicial esta presente nos estados do automato
    while True:
        estado_inicial = input("Digite o estado inicial do automato: ").strip()
        if(estado_inicial not in estados):
            print(f"---------------------")
            print(f"Erro: O estado '{estado_inicial}' nao pertence aos estados do automato")
            print(f"Selecione um estado inicial '{estados}': ")
            print(f"---------------------")    
            continue
        break

    # todo: implementar uma logica que obrigue a ter estados finais
    while True:
        estados_aceitacao = input("Digite os estados de aceitacao do automato (separados por espaço): ").strip().split()
        estados_invalidos = []
        for estado in estados_aceitacao:
            if estado not in estados:
                estados_invalidos.append(estado)
        if estados_invalidos:
            print(f"---------------------")
            print(f"Erro: O(s) estado(s) {estados_invalidos} nao pertence(m) aos estados do automato \\n")
            print(f"Selecione um ou mais estados de aceitacao '{estados}': ")
            print(f"---------------------")    
            continue
        break      
    
    # coletando as transicoes do automato
    func_transicao = {}
    # aqui adicionamos o a transicao epsilon no alfabeto
    simbolos_validos = set(alfabeto) | {EPSILON}
    print(f"\nDefina as transicoes, usando um simbolo válido ou '{EPSILON}' (digite 'fim' para parar):")
    print(f"Formato esperado -> ESTADO, SIMBOLO = DESTINO1 DESTINO2 ...")
    
    while True:
        # formato esperado: q0, a = q1 q2
        entrada = input("  δ(estado, simbolo) = ").strip()
        if entrada.lower() == 'fim':
            break
            
        try:
            """
            divide as partes leitura e resultado_leitura por um "="
            - leitura => conjunto de estado e leitura de simbolo (q0, a)
            - resultado_leitura => o que acontece com a leitura de um simbolo em um deterimado estado
            """
            leitura, resultado_leitura = entrada.split('=')
            
            # processamento da leitura (estado, simbolo)
            # a condicional porcura a "," para separa o estado do simbolo na entrada fornecida
            if ',' not in leitura:
                 raise ValueError("Formato da chave inválido. Use 'estado, simbolo = ...'")

            estado_origem, simbolo = [s.strip() for s in leitura.split(',')]
            
            # remove "δ(" e ")" se o usuario digitou
            estado_origem = estado_origem.replace("δ(", "").strip()
            simbolo = simbolo.replace(")", "").strip()
            
            # processamento dos destinos (valor)
            # removendo os espacos em branco extra do inicio e fim da string resultado_leitura
            resultado_limpo = resultado_leitura.strip()
            # divindo a string em uma lista de estados, separando por espacos
            lista_estados = resultado_limpo.split()
            estados_destino = set()
            # removendo espcaos extras e add no conjunto estados_destino
            for estado in lista_estados:
                estado_limpo = estado.strip()
                estados_destino.add(estado_limpo)
            
            # verificacao se o simbolo digitado esta presente nao alfabeto
            if simbolo not in simbolos_validos:
                print(f"---------------------")
                print(f"AVISO: O simbolo '{simbolo}' nao e '{EPSILON}' e nao faz parte do alfabeto definido.")
                print(f"Digite novamente a transicao desejada. ")
                print(f"---------------------")
                continue

            # adicionando as transicoes
            chave = (estado_origem, simbolo)
            
            # atualizando a transicao caso desejado
            if chave not in func_transicao:
                func_transicao[chave] = set()
            func_transicao[chave].update(estados_destino)
            print(f"  -> Transicao adicionada: δ({estado_origem}, {simbolo}) = {estados_destino}")
            
        except ValueError as e:
            # corrigindo erros de formatacao
            print(f"---------------------")
            print(f"  Erro de sintaxe/formato: {e}. O formato esperado é: ESTADO, SIMBOLO = DESTINO1 DESTINO2 ...")
            print(f"Digite novamente a transicao desejada. ")
            print(f"---------------------")
            
    # cria e retorna o objeto AFN
    return AFN(estados, alfabeto, func_transicao, estado_inicial, estados_aceitacao)


# --- Função Principal ---
def main():
    try:
        afn = obter_definicao_afn_usuario()
        afd_convertido = conversor_afn_para_afd(afn)
        
        print("\n----------------------------")
        print("\n    Conversão Concluída!    ")
        print("\n----------------------------")
        afd_convertido.imprimir() # metodo definido em afd.py
        
        # funcao para testar as cadeias de entrada e validar a linguagem no automato convertido
        print("\n----------------------------")
        print("\n   Teste o AFD convertido   ")
        print("\n----------------------------")
        while True:
            cadeia = input("Digite uma cadeia para testar no AFD (ou 'sair'): ").strip()
            if cadeia.lower() == 'sair':
                break
                
            if afd_convertido.processar_cadeia(cadeia):
                print(f"Cadeia '{cadeia}' Resultado: ACEITA")
            else:
                print(f"Cadeia '{cadeia}' Resultado: REJEITA")
                
    except Exception as e:
        print(f"\nOcorreu um erro fatal na execução: {e}")
        # tratamento de erro para detectar onde ocorreu na implementacao da logica
        import traceback
        traceback.print_exc()

# Ponto de entrada do script
if __name__ == "__main__":
    main()