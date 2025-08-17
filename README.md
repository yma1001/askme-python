# askme-python
Ask Me is a quiz game with several modes and a ranking with the scores of the best players.
# 🎲 AskMe – Jogo de Perguntas e Respostas em Python

AskMe é um jogo de quiz em Python que permite ao usuário responder perguntas em diferentes modos de jogo, acumulando pontos e registrando os melhores resultados no Hall da Fama.


## 🛠 Dependências

O jogo utiliza a biblioteca `colorama` para colorir o terminal.  
Instale com:
pip install colorama

Não é necessário instalar nada extra no Linux ou macOS, apenas Python 3.x e colorama.
No Windows, basta instalar colorama normalmente.

📂 Arquivos necessários
Para o jogo funcionar corretamente, você precisa ter:
Arquivo de perguntas (AskMe.json)
Contém todas as perguntas, alternativas, respostas e dicas.
Deve estar no mesmo diretório do script ou ajustar o caminho no código.
Arquivos do Hall da Fama (hall_da_fama_fixas.json, hall_da_fama_tempo.json, hall_da_fama_tente.json)
São gerados automaticamente na primeira execução.
Armazenam os melhores jogadores de cada modo.

🎮 Modos de jogo
Número de Questões Fixas – Responde um número limitado de perguntas.
Limite de Tempo – Responde perguntas dentro de um tempo máximo (ex: 120 segundos).
Tente Não Errar – O jogo termina ao errar qualquer pergunta.
Ver Hall da Fama – Mostra os melhores jogadores de todos os modos.

⌨️ Controles e dicas
Digite o número da alternativa correta (1 a 5).
Digite 0 para usar uma dica (máx. 3 por partida).
Digite E para eliminar duas alternativas erradas (máx. 1 por partida).
Digite P para pular a questão (máx. 3 por partida).

🚀 Como executar
Baixe todos os arquivos necessários (AskMe.json e o script Python).
Abra o terminal na pasta do projeto.
Execute:python askme.py

📚 Aprendizados
Manipulação de arquivos JSON para salvar dados persistentes.
Uso da biblioteca colorama para estilizar saída no terminal.
Lógica de múltiplos modos de jogo, dicas e eliminatórias.
Implementação de sistema de pontuação e Hall da Fama.
