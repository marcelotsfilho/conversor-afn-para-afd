# em main.py

from afn import AFN, EPSILON
from conversor import conversor_afn_para_afd

def obter_definicao_afn_usuario():
    """
    Função para coletar os dados do AFN do usuário e retornar um objeto AFN.
    """
    print("--- Definição do AFN ---")
    # Nota: Usamos aspas simples ' ' para o EPSILON, o que ajuda na digitação se o EPSILON for uma string vazia ("")
    # Se EPSILON for "", a mensagem será: (Use '' para transições épsilon/vazias)
    print(f"(Use '{EPSILON}' para transicoes epsilon)")
    
    # 1. COLETAR Estados (Q)
    estados = input("Estados (separados por espaço): ").strip().split()
    
    # 2. COLETAR Alfabeto (Σ)
    alfabeto = input("Alfabeto (separados por espaço, sem épsilon): ").strip().split()
    
    # 3. COLETAR Estado Inicial (q0)
    estado_inicial = input("Estado Inicial: ").strip()
    
    # 4. COLETAR Estados Finais (F)
    estados_aceitacao = input("Estados Finais (separados por espaço): ").strip().split()
    
    # 5. COLETAR Função de Transição (δ)
    func_transicao = {}
    # Incluímos o EPSILON no conjunto de símbolos válidos para a coleta
    simbolos_validos = set(alfabeto) | {EPSILON}
    print(f"\nDefina as transições, usando um símbolo válido ou '{EPSILON}' (digite 'fim' para parar):")
    
    while True:
        # Formato esperado: q0, a = q1 q2
        entrada = input("  δ(estado, simbolo) = ").strip()
        if entrada.lower() == 'fim':
            break
            
        try:
            # 1. Tenta dividir a entrada no símbolo de igual (=)
            parte_chave, parte_valor = entrada.split('=')
            
            # 2. Processa a chave (estado, simbolo)
            # A chave está no formato "q0, a" ou "δ(q0, a)"
            # A linha abaixo busca por vírgula para separar estado e símbolo
            if ',' not in parte_chave:
                 raise ValueError("Formato da chave inválido. Use 'estado, simbolo = ...'")

            estado_origem, simbolo = [s.strip() for s in parte_chave.split(',')]
            
            # Remove "δ(" e ")" se o usuário digitou
            estado_origem = estado_origem.replace("δ(", "").strip()
            simbolo = simbolo.replace(")", "").strip()
            
            # 3. Processa os destinos (valor)
            # Os destinos podem ser múltiplos e devem ser convertidos para um conjunto
            estados_destino = set(s.strip() for s in parte_valor.strip().split())
            
            # 4. Validação adicional: Verifica se o símbolo é válido
            if simbolo not in simbolos_validos:
                 print(f"  AVISO: Símbolo '{simbolo}' não é '{EPSILON}' nem parte do alfabeto definido. Ignorado.")
                 continue

            # 5. Adiciona ao dicionário de transições
            chave = (estado_origem, simbolo)
            
            # No AFN, a transição pode ser definida uma vez, depois atualizada
            if chave not in func_transicao:
                func_transicao[chave] = set()
            
            func_transicao[chave].update(estados_destino)
            
            print(f"  -> Adicionado: δ({estado_origem}, {simbolo}) = {estados_destino}")
            
        except ValueError as e:
            # Captura erros de formatação (e.g., falta o '=' ou a vírgula)
            print(f"  Erro de sintaxe/formato: {e}. O formato esperado é: ESTADO, SIMBOLO = DESTINO1 DESTINO2 ...")
            
    # 6. CRIAR e RETORNAR o objeto AFN
    return AFN(estados, alfabeto, func_transicao, estado_inicial, estados_aceitacao)


# --- Função Principal ---
def main():
    try:
        # 1. Obter o AFN do usuário
        meu_afn = obter_definicao_afn_usuario()
        
        # 2. Chamar o conversor
        meu_afd_convertido = conversor_afn_para_afd(meu_afn)
        
        # 3. Imprimir o AFD resultante
        print("\n--- Conversão Concluída! ---")
        meu_afd_convertido.imprimir() # Chama o método que definimos no afd.py
        
        # 4. Loop para testar cadeias
        print("\n--- Teste do AFD ---")
        while True:
            cadeia = input("Digite uma cadeia para testar no AFD (ou 'sair'): ").strip()
            if cadeia.lower() == 'sair':
                break
                
            if meu_afd_convertido.processar_cadeia(cadeia):
                print(f"Cadeia '{cadeia}' Resultado: ACEITA")
            else:
                print(f"Cadeia '{cadeia}' Resultado: REJEITA")
                
    except Exception as e:
        print(f"\nOcorreu um erro fatal na execução: {e}")
        # Use traceback para ver onde o erro ocorreu na sua lógica de conversão
        import traceback
        traceback.print_exc()

# Ponto de entrada do script
if __name__ == "__main__":
    main()