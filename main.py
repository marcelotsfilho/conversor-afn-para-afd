# em main.py
import xml.etree.ElementTree as ET
from afn import AFN, EPSILON
from conversor import conversor_afn_para_afd
from io_jflap import carregar_afn_jflap, salvar_afd_jflap

def afn_jflap(caminho_arquivo: str) -> AFN:
    tree = ET.parse(caminho_arquivo)
    root = tree.getroot()

    estados = set()
    alfabeto = set()
    func_transicao = {}
    estado_inicial = None
    estados_aceitacao = set()

    for state in root.findall(".//state"):
        nome = state.get("name")
        estados.add(nome)
        if state.find("initial") is not None:
            estado_inicial = nome
        if state.find("final") is not None:
            estados_aceitacao.add(nome)

    for trans in root.findall(".//transition"):
        origem = root.findtext(".//state[@id='" + trans.findtext('from') + "']").get("name")
        destino = root.findtext(".//state[@id='" + trans.findtext('to') + "']").get("name")
        simbolo = trans.findtext("read") or "ε"

        alfabeto.add(simbolo)
        func_transicao.setdefault((origem, simbolo), set()).add(destino)

    return AFN(
        estados = estados,
        alfabeto = alfabeto - {EPSILON},
        func_transicao = func_transicao,
        estado_inicial = estado_inicial,
        estados_aceitacao = estados_aceitacao
    )

def obter_definicao_afn_usuario():
    """
    funcao para coletar os dados do AFN do usuario e retornar um objeto AFN.
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
    print(f"\nDefina as transicoes, usando um simbolo valido ou '{EPSILON}' (digite 'fim' para parar):")
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
        print("==============================")
        print("   Conversor AFN para AFD ")
        print("==============================")
        print("Escolha uma opcao:")
        print("  1 - Digitar AFN (entrada via prompt)")
        print("  2 - Ler AFN de arquivo JFLAP (.jff)")
        escolha = input("Opção (1 ou 2): ").strip()

        if escolha == '1':
            afn = obter_definicao_afn_usuario()
            afd_convertido = conversor_afn_para_afd(afn)

            # gera ou nao uma saida jflap
            salvar = input("Deseja salvar o AFD gerado em arquivo .jff? (s/n): ").strip().lower()
            if salvar == 's':
                caminho_saida = input("Caminho do arquivo de saida (.jff): ").strip()
                salvar_afd_jflap(afd_convertido, caminho_saida)
                print(f"AFD salvo em: {caminho_saida}")

        elif escolha == '2':
            caminho_entrada = input("Caminho do arquivo .jff (AFN): ").strip()
            caminho_saida = input("Caminho do arquivo de saida .jff (AFD): ").strip()

            afn = carregar_afn_jflap(caminho_entrada)
            afd_convertido = conversor_afn_para_afd(afn)
            salvar_afd_jflap(afd_convertido, caminho_saida)
            print(f"Conversao concluida. O AFD foi salvo no arquivo: {caminho_saida}")

        else:
            print("Opcao invalida.")
            return

        # exibe e permite testar o AFD convertido (mesma lógica já existente)
        print("\n--- AFD Equivalente ---")
        afd_convertido.imprimir()

        print("\nTeste aqui as cadeias no AFD equivalente (digite 'sair' para encerrar):")
        while True:
            cadeia = input("Cadeia: ").strip()
            if cadeia.lower() == 'sair':
                break
            resultado = afd_convertido.processar_cadeia(cadeia)
            print("ACEITA" if resultado else "REJEITA")

    # tratamento de erro (para identificar melhor)
    except Exception as e:
        print(f"\nOcorreu um erro: {e}")
        import traceback
        traceback.print_exc()

# Ponto de entrada do script
if __name__ == "__main__":
    main()