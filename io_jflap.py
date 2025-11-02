import xml.etree.ElementTree as ET
from afn import AFN, EPSILON
from afd import AFD

def carregar_afn_jflap(caminho_arquivo: str) -> AFN:
    """
    le um arquivo .jff (JFLAP) e retorna um objeto AFN.
    """
    tree = ET.parse(caminho_arquivo)
    root = tree.getroot()

    estados = set()
    alfabeto = set()
    func_transicao = {}
    estado_inicial = None
    estados_aceitacao = set()
    id_nome = {}

    # leitura dos estados
    for state in root.findall(".//state"):
        estado_id = state.get("id")
        nome = state.get("name")
        id_nome[estado_id] = nome
        estados.add(nome)

        if state.find("initial") is not None:
            estado_inicial = nome
        if state.find("final") is not None:
            estados_aceitacao.add(nome)

    # leitura das transicoes
    for trans in root.findall(".//transition"):
        origem = id_nome[trans.findtext('from')]
        destino = id_nome[trans.findtext('to')]
        # por padrão arquivos JFLAP costumam contera tag <read/> vazio para transicoes epsilon
        read_text = trans.findtext('read')
        # normaliza e decide se é epsilon
        if read_text is None:
            # tag <read/> ausente -> interpreta como epsilon
            simbolo = EPSILON
        else:
            # remove espaços em branco ao redor
            read_text_limpo = read_text.strip()
            # se apos limpar a string estiver vazia, tambem e epsilon
            if read_text_limpo == "":
                simbolo = EPSILON
            else:
                simbolo = read_text_limpo

        alfabeto.add(simbolo)
        func_transicao.setdefault((origem, simbolo), set()).add(destino)

    # remove epsilon do alfabeto publico do AFN
    alfabeto.discard(EPSILON)

    return AFN(
        estados=estados,
        alfabeto=alfabeto,
        func_transicao=func_transicao,
        estado_inicial=estado_inicial,
        estados_aceitacao=estados_aceitacao
    )

def salvar_afd_jflap(afd: AFD, caminho_saida: str):
    """
    salva o AFD em formato JFLAP (.jff).
    """
    structure = ET.Element("structure")
    ET.SubElement(structure, "type").text = "fa"
    automaton = ET.SubElement(structure, "automaton")

    id_map = {}
    for i, estado in enumerate(sorted(afd.estados)):
        st_el = ET.SubElement(automaton, "state", id=str(i), name=estado)
        ET.SubElement(st_el, "x").text = str(100 + i * 100)
        ET.SubElement(st_el, "y").text = "200"
        id_map[estado] = str(i)

        if estado == afd.estado_inicial:
            ET.SubElement(st_el, "initial")
        if estado in afd.estados_aceitacao:
            ET.SubElement(st_el, "final")

    for (origem, simbolo), destino in afd.func_transicao.items():
        tr_el = ET.SubElement(automaton, "transition")
        ET.SubElement(tr_el, "from").text = id_map[origem]
        ET.SubElement(tr_el, "to").text = id_map[destino]
        # grava string vazia para epsilon (se EPSILON == '')
        ET.SubElement(tr_el, "read").text = (simbolo if simbolo is not None else "")

    tree = ET.ElementTree(structure)
    tree.write(caminho_saida, encoding="utf-8", xml_declaration=True)