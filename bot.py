# Import de Web Bot
from botcity.web import WebBot, Browser, By

# Import de integração com BotCity Maestro SDK
from botcity.maestro import *

# WebDriver Manager para gerenciamento automático do driver
from webdriver_manager.chrome import ChromeDriverManager # Instale com: pip install webdriver-manager

import logging

from datetime import datetime

# Desativa mensagem de erros por não estar conectado ao Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    # Instancia do BotMaestroSDK
    maestro = BotMaestroSDK.from_sys_args()
    # Objeto com informações da execução
    execution = maestro.get_execution()

    # Recuperando o parametro "canais"
    canais = execution.parameters.get("canais")

    # Transforma em uma lista separando por vírgula
    canais = canais.split(",")

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    # Configuração do logging
    logging.basicConfig(
        filename="log_canais_youtube.txt",  # Arquivo que será gerado para upload
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding='utf-8'
    )

    bot = WebBot()

    # Configuração do modo headless
    bot.headless = False

    # Configuração do navegador
    bot.browser = Browser.CHROME

    # Usa WebDriver Manager para definir automaticamente o caminho do driver
    # Isso garante que a versão correta do geckodriver seja baixada e usada
    bot.driver_path = ChromeDriverManager().install()

    # Lista de canais para pesquisar
    # canais = ['botcity_br', 'botcity-dev', 'youtube', 'github']


    # Inicializa contadores
    total_canais = len(canais)
    canais_sucesso = 0
    canais_falha = 0

    maestro.alert(
        task_id=execution.task_id,
        title="BotYoutube - Inicio",
        message="Estamos iniciando o processo",
        alert_type=AlertType.INFO
    )

    for canal in canais:
        try:
            logging.info(f"Iniciando coleta de dados do canal: {canal}")
            # Inicia o navegador na URL do canal
            bot.browse(f"https://www.youtube.com/@{canal}")

            # Retorna lista de elementos com os dados do canal
            element = bot.find_elements(
                selector='//span[@class="yt-core-attributed-string yt-content-metadata-view-model__metadata-text yt-core-attributed-string--white-space-pre-wrap yt-core-attributed-string--link-inherit-color" and @role="text"]',
                by=By.XPATH
            )

            # Captura o texto de cada elemento encontrado
            nome_canal = element[0].text
            numero_inscritos = element[1].text
            quantidade_videos = element[2].text

            logging.info(f"Canal: {nome_canal} | Inscritos: {numero_inscritos} | Vídeos: {quantidade_videos}")

            canais_sucesso += 1  # Incrementa contador de sucesso

            maestro.new_log_entry(
                activity_label="EstatisticasYoutube",
                values = {
                    "data_hora": datetime.now().strftime("%Y-%m-%d_%H-%M"),
                    "canal": nome_canal,
                    "inscritos": numero_inscritos
                }
            )
            
        except Exception as ex:
            logging.error(f"Erro ao coletar dados do canal {canal}: {ex}")

            canais_falha += 1  # Incrementa contador de falha

            # Salvando captura de tela do erro
            bot.save_screenshot("erro.png")

            # Dicionario de tags adicionais
            tags = {"canal": canal}

            # Registrando o erro
            maestro.error(
                task_id=execution.task_id,
                exception=ex,
                screenshot="erro.png",
                tags=tags
            )

        finally:
            # Espera 3 segundos e encerra o navegador
            bot.wait(3000)
            bot.stop_browser()

    if canais_sucesso == total_canais:
        # Define o status de finalização da tarefa
        message = f"Todos os {total_canais} canais foram processados com sucesso."
        status = AutomationTaskFinishStatus.SUCCESS

    elif canais_falha == total_canais:
        # Define o status de finalização da tarefa
        message = f"Todos os {total_canais} canais foram processados com erro."
        status = AutomationTaskFinishStatus.FAILED

    else:
        # Define o status de finalização da tarefa
        message = f'Dos {total_canais} canais pesquisados, número de falha: {canais_falha} e número de sucesso: {canais_sucesso}.'
        status = AutomationTaskFinishStatus.PARTIALLY_COMPLETED


    # Enviando para a plataforma com o nome "Captura Canal..."
    maestro.post_artifact(
                task_id=execution.task_id,
                artifact_name=f"log_canais_youtube_{execution.task_id}.txt",
                filepath="log_canais_youtube.txt"
            )


    maestro.finish_task(
        task_id=execution.task_id,
        status=status,
        message=message,
        total_items=total_canais, # Número total de itens processados
        processed_items=canais_sucesso, # Número de itens processados com sucesso
        failed_items=canais_falha # Número de itens processados com falha
        )

    logging.info("Execução finalizada.")
    logging.info(f"Total canais: {total_canais} | Canais com sucesso: {canais_sucesso} | Canais com falha: {canais_falha}")






if __name__ == '__main__':
    main()