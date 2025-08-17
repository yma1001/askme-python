#Bibliotecas necessárias a instalação: colorama
import time
import random
import json
from colorama import Fore, Style, init

# Inicializa o uso de cores no terminal
init(autoreset=True)

# Carregar as perguntas do arquivo JSON
def carregar_perguntas():
    try:
        with open('c:/Users/yagom/Desktop/Yago Mendes Fase 01/Arquivos AskMe.json', 'r', encoding='utf-8') as arquivo:
            perguntas = json.load(arquivo)
        return perguntas
    except FileNotFoundError:
        print(Fore.RED + "Erro: Arquivo de perguntas não encontrado.")
        return []

# Função para exibir uma pergunta e obter a resposta
def exibir_pergunta(pergunta, dicas_restantes, eliminacoes_restantes, pulos_restantes):
    print(f"{Fore.CYAN}\nCategoria: {pergunta['category']}")
    print(f"{Fore.YELLOW}Pergunta: {pergunta['questionText']}")
    print("Alternativas: ")
    for i in range(1, 6):
        print(f"{Fore.GREEN}{i}) {pergunta[f'option{i}']}")

    print(f"{Fore.MAGENTA}Dicas restantes: {dicas_restantes} | Pulos restantes: {pulos_restantes} | Eliminações restantes: {eliminacoes_restantes}")
    print("Opções adicionais: ")
    print("Digite '0' para usar uma dica")
    print("Digite 'P' para pular a questão")
    print("Digite 'E' para eliminar duas alternativas")

    resposta = input(Fore.WHITE + "Digite o número da alternativa correta ou uma das opções acima: ").strip().upper()

    if resposta == '0' and dicas_restantes > 0:
        print(Fore.LIGHTBLUE_EX + f"Dica: {pergunta['hint'][0]}")
        dicas_restantes -= 1
        resposta = input(Fore.WHITE + "Digite o número da alternativa correta: ").strip()
    elif resposta == 'E' and eliminacoes_restantes > 0:
        eliminar_opcoes(pergunta)
        eliminacoes_restantes -= 1
        resposta = input(Fore.WHITE + "Digite o número da alternativa correta: ").strip()
    elif resposta == 'P':
        print(Fore.LIGHTRED_EX + "Questão pulada!")
        pulos_restantes -= 1
        return None, dicas_restantes, eliminacoes_restantes, pulos_restantes, True
    else:
        resposta = resposta.strip()
    
    return resposta, dicas_restantes, eliminacoes_restantes, pulos_restantes, False

# Função para eliminar duas alternativas erradas
def eliminar_opcoes(pergunta):
    opcoes_erradas = [f"option{i}" for i in range(1, 6) if pergunta[f"option{i}"] != pergunta["answer"]]
    opcoes_a_eliminar = random.sample(opcoes_erradas, 2)

    print(Fore.LIGHTYELLOW_EX + "Duas alternativas erradas foram eliminadas:")
    for i in range(1, 6):
        if f"option{i}" in opcoes_a_eliminar:
            print(f"{Fore.RED}{i}) [ELIMINADA]")
        else:
            print(f"{Fore.GREEN}{i}) {pergunta[f'option{i}']}")

# Função para salvar o Hall da Fama
def salvar_hall_da_fama(nome_jogador, pontos, modo):
    try:
        with open(f'hall_da_fama_{modo}.json', 'r', encoding='utf-8') as arquivo:
            hall_da_fama = json.load(arquivo)
    except FileNotFoundError:
        hall_da_fama = []

    # Insere o jogador atual
    hall_da_fama.append({'nome': nome_jogador, 'pontos': pontos})
    
    # Ordena pela pontuação em ordem decrescente
    hall_da_fama = sorted(hall_da_fama, key=lambda x: x['pontos'], reverse=True)
    
    # Mantém apenas os top 5 jogadores
    if len(hall_da_fama) > 5:
        hall_da_fama = hall_da_fama[:5]

    # Salva novamente o Hall da Fama no arquivo
    with open(f'hall_da_fama_{modo}.json', 'w', encoding='utf-8') as arquivo:
        json.dump(hall_da_fama, arquivo, indent=4)

    # Exibe o Hall da Fama
    print(Fore.YELLOW + "\n=== Hall da Fama ===")
    for i, jogador in enumerate(hall_da_fama):
        print(f"{Fore.CYAN}{i + 1}. {jogador['nome']} - {jogador['pontos']} pontos")

# Função para exibir o Hall da Fama de todos os modos
def exibir_todos_hall_da_fama():
    modos = ['fixas', 'tempo', 'tente']
    print(Fore.YELLOW + "\n=== Hall da Fama ===")
    
    for modo in modos:
        print(Fore.MAGENTA + f"\nModo: {modo.capitalize()}")
        try:
            with open(f'hall_da_fama_{modo}.json', 'r', encoding='utf-8') as arquivo:
                hall_da_fama = json.load(arquivo)
        except FileNotFoundError:
            hall_da_fama = []
        
        if hall_da_fama:
            for i, jogador in enumerate(hall_da_fama):
                print(f"{Fore.CYAN}{i + 1}. {jogador['nome']} - {jogador['pontos']} pontos")
        else:
            print(Fore.RED + "Nenhum registro no Hall da Fama ainda.")

# Função genérica para modos de jogo
def executar_modo(perguntas, modo, limite_tempo=None):
    random.shuffle(perguntas)
    pontuacao = 0
    dicas_restantes = 3
    eliminacoes_restantes = 1
    pulos_restantes = 3
    tempo_inicial = time.time() if limite_tempo else None
    perguntas_pendentes = []

    for pergunta in perguntas:
        if limite_tempo:
            tempo_restante = limite_tempo - (time.time() - tempo_inicial)
            if tempo_restante <= 0:
                print(Fore.RED + "Tempo esgotado!")
                break
            print(Fore.CYAN + f"Tempo restante: {int(tempo_restante)} segundos")

        while True:
            resposta, dicas_restantes, eliminacoes_restantes, pulos_restantes, pulou = exibir_pergunta(
                pergunta, dicas_restantes, eliminacoes_restantes, pulos_restantes
            )

            if pulou:
                perguntas_pendentes.append(pergunta)
                break  # Vai para a próxima questão

            if resposta and resposta.isdigit() and 1 <= int(resposta) <= 5:
                alternativa_escolhida = pergunta[f"option{resposta}"]
                if alternativa_escolhida == pergunta["answer"]:
                    print(Fore.GREEN + "Resposta correta!")
                    pontuacao += int(pergunta["value"])
                else:
                    print(Fore.RED + f"Resposta errada! A correta era: {pergunta['answer']}")
                    if modo == "tente":  # Se for o modo "Tente Não Errar", termina o jogo ao errar
                        print(Fore.YELLOW + f"\nVocê terminou o jogo com {pontuacao} pontos.")
                        nome_jogador = input(Fore.CYAN + "Digite seu nome para o Hall da Fama: ")
                        salvar_hall_da_fama(nome_jogador, pontuacao, modo)
                        return  # Sai da função
                break
            else:
                print(Fore.RED + "Alternativa inválida! Tente novamente.")

    # Processa as perguntas pendentes
    for pergunta in perguntas_pendentes:
        resposta, _, _, _, _ = exibir_pergunta(pergunta, 0, 0, 0)
        if resposta and resposta.isdigit() and 1 <= int(resposta) <= 5:
            alternativa_escolhida = pergunta[f"option{resposta}"]
            if alternativa_escolhida == pergunta["answer"]:
                pontuacao += int(pergunta["value"])

    print(Fore.YELLOW + f"\nPontuação final: {pontuacao}")
    nome_jogador = input(Fore.CYAN + "Digite seu nome para o Hall da Fama: ")
    salvar_hall_da_fama(nome_jogador, pontuacao, modo)

# Menu principal
def menu():
    perguntas = carregar_perguntas()

    if not perguntas:
        print(Fore.RED + "Não é possível continuar sem perguntas.")
        return

    while True:
        print(Fore.MAGENTA + "\n=== AskMe ===")
        print("1. Número de Questões Fixas")
        print("2. Limite de Tempo")
        print("3. Tente Não Errar")
        print("4. Ver Hall da Fama")
        print("5. Sair")

        modo_de_jogo = input(Fore.CYAN + "Digite o número do modo desejado: ").strip()

        if modo_de_jogo == '1':
            executar_modo(perguntas, "fixas")
        elif modo_de_jogo == '2':
            executar_modo(perguntas, "tempo", limite_tempo=120)
        elif modo_de_jogo == '3':
            executar_modo(perguntas, "tente")
        elif modo_de_jogo == '4':
            exibir_todos_hall_da_fama()
        elif modo_de_jogo == '5':
            print(Fore.YELLOW + "Encerrando o jogo. Até logo!")
            break
        else:
            print(Fore.RED + "Opção inválida! Tente novamente.")

# Executa o jogo
menu()
# Autor: Yago Mendes de Araujo
# Componente Curricular: MI Algoritmos
# Concluído em: 09/12/2024
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
# trecho de código de outro colega ou de outro autor, tais como provindos de livros e
# apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
# de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
# do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.