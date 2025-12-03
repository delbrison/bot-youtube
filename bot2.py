# Import de Web Bot
from botcity.web import WebBot, Browser, By

# Import de integração com BotCity Maestro SDK
from botcity.maestro import *

# WebDriver Manager para gerenciamento automático do driver
from webdriver_manager.chrome import ChromeDriverManager # Instale com: pip install webdriver-manager

# Desativa mensagem de erros por não estar conectado ao Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    # Instancia do BotMaestroSDK
    maestro = BotMaestroSDK.from_sys_args()
    # Objeto com informações da execução
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()

    # Configuração do modo headless
    bot.headless = False

    # Configuração do navegador
    bot.browser = Browser.CHROME

    # Usa WebDriver Manager para definir automaticamente o caminho do driver
    # Isso garante que a versão correta do geckodriver seja baixada e usada
    bot.driver_path = ChromeDriverManager().install()

    # Lista de canais para pesquisar
    canais = ['botcity_br', 'botcity-dev', 'youtube', 'github']

    for canal in canais:
        # Inicia o navegador na URL do canal
        bot.browse(f"https://www.youtube.com/@{canal}")

        # Retorna lista de elementos com os dados do canal
        element = bot.find_elements(
            selector='//span[@class="yt-core-attributed-string yt-content-metadata-view-model-wiz__metadata-text yt-core-attributed-string--white-space-pre-wrap yt-core-attributed-string--link-inherit-color" and @role="text"]',
            by=By.XPATH
        )

        # Captura o texto de cada elemento encontrado
        nome_canal = element[0].text
        numero_inscritos = element[1].text
        quantidade_videos = element[2].text

        print(f"Nome do canal: {nome_canal} | Número de inscritos: {numero_inscritos} | Quantidade de vídeos: {quantidade_videos}")

        # Espera 3 segundos e encerra o navegador
        bot.wait(3000)
        bot.stop_browser()


if __name__ == '__main__':
    main()