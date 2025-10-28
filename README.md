# Conversão de AFN para AFD
---

Todo AFN pode ser transformado em um AFD equivalente, ou seja, um autômato que reconhece exatamente o mesmo conjunto de palavras. A técnica utilizada é chamada de `construção por subconjuntos` (subset construction) ou método do `conjunto das partes`.

---

## Passos do processo

1. Defina o &-fecho (epsilon-closure):

Para cada estado `q`, calcule o &-fecho, ou seja, o conjunto de estados alcançaveis a partir de `q` apenas com transições &(vazias)

- Isso é essencial para AFN`s com transições &(x-transições)

2. Determine o estado inicial AFD:

O estado inicial do AFD é o &-fecho do estado inicial do AFN.

- Representa todos os estrado que o autômato pode estar inicialmente sem consumir nenhum simbolo

3. Crie novos estados (conjunto de estados do AFN)

Cada estado do AFD corresponde a um conjunto de estados do AFN

. Para cada símbolo de entrada `a`:
- Veja, a partir de cada estado do conjunto atual, para onde o AFN pode ir com `a`.
- Aplique o &-fecho no resultado.
- O conjunto obtido forma um novo estado do AFD (se ainda nao existir).

. Continue até que nenhum novo conjunto seja gerado

4. Determine os estados finais AFD:

Um estado do AFD é final se pelo menos um dos estados do AFN contidos nesse conjunto for um estado final

---

## Algorítmo:

O algorítmo de convsersão de autômato AFN para AFD é dividido em 4 partes `main.py`, `afn.py`, `afd.py`, `conversor.py`.

1. main.py:

- O arquivo `main.py` conta com as funções principais, onde será coletado os dados do AFN(como a coleta dos estados, coleta de alfabeto, coleta do estado inicial, coleta dos estados de aceitação e a coleta da função de transição) e retornar um objeto AFN. 

- Após a coleta dos dados do autômato AFN é chamada a função de `conversor_afn_para_afd(passando por parâmetro o AFN gerado pelo usuário)`

- Por fim, após a conversão do autômato, é solicitado que o usuário digite uma cadeia de simbolos para testar o AFD gerado. A função deverá retornar `ACEITA` caso a cadeia digitada satisfaça o AFD ou retornar `REJEITA` caso a cadeia digitada não satisfaça o AFD.

---

2. afn.py:

- O arquivo `afn.py` conta com a criação da classe `AFN` onde será criado os objetos `estados`, `alfabeto`, `func_transicao`, `estado_inicial` e `estados_aceitacao`. O arquivo também conta com o calculo do fecho-epsilon para o conjunto de estados do `AFN`, utilizando o algoritmo de busca em profundidade (DFS) com uma pilha, percorrendo todos os estados alcançáveis por transições vazias.

---

3. afd.py:

- O arquivo `afd.py` conta com a criação da classe `AFD` onde será criado os objetos `estados`, `alfabeto`, `func_transicao`, `estado_inicial` e `estados_aceitacao`. O arquivo também conta com dois métodos pricipais para o funcionamento do AFD:

- `processar_cadeia`: Funciona como o simulador do AFD. Ele recebe uma cadeia e a processa símbolo por símbolo. Para cada símbolo, ele faz duas verificações: 

1) se o símbolo pertence ao alfabeto 
2) se existe uma transição definida para o estado atual com aquele símbolo. 

- Se a cadeia inteira for processada e o autômato parar em um estado de aceitação, a função retorna `True`.

- `imprimir`: Um método auxiliar para visualizar o AFD gerado. Ele imprime no console todos os componentes do autômato (estados, alfabeto, inicial, finais) e a função de transição de forma ordenada e legível.

---

4. conversor.py:

- Este é o "cérebro" do projeto, onde a conversão realmente acontece. Ele contém a função `conversor_afn_para_afd` que implementa o algorítmo de Construção de Subconjuntos.

O processo segue os passos do código:

1. Inicialização: Ele define o alfabeto do AFD (o mesmo do AFN, sem o `&`) e calcula o primeiro estado do AFD, que é o `calcula_fecho_epsilon` do estado inicial do AFN.

2. Controle: Ele cria uma `fila` (para a busca em largura - BFS) e um conjunto de `estados_descobertos` (para não processar o mesmo "macro-estado" várias vezes).

3. Loop Principal (while fila): Enquanto a `fila` não estiver vazia, ele:

- Retira um "macro-estado" (um conjunto de estados) da fila.

- Para cada `simbolo` do alfabeto:

- Cálculo da Transição Estendida: Ele descobre para onde esse macro-estado vai. Primeiro, vê todos os estados que o AFN alcança com o `simbolo` (Passo A no código).

- Aplicação do Fecho: Em seguida, aplica o `calcula_fecho_epsilon` nesse resultado (Passo B no código).

- O novo conjunto gerado (`proximo_macro_estado`) é o estado de destino no AFD. Se for um conjunto novo (que não está em `estados_descobertos`), ele é adicionado na `fila` para ser processado.

---

## Como executar:

No terminal, execute o seguinte comando:

```
python3 main.py
```

A seguir, siga as instruções de preenchimento do `AFN` e execute a validação do `AFD` quando solicitado.