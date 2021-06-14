import configparser
import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


config = configparser.ConfigParser()
config.read('email.ini')

SENDER_EMAIL: str = config['MAIL']['FROM']
RECEIVER_EMAIL: str = config['MAIL']['TO']
CC_MAIL: str = config['MAIL'].get('CC', None)
PASSWORD: str = config['MAIL']['PASSWD']
SMTP_SERVER: str = config['SERVER']['HOST']
PORT: int = int(config['SERVER']['PORT'])

subject = "Ocorrência Ponto - data"

h1 = input()
h2 = input()
h3 = input()
h4 = input()

text = f"""\
Informo ocorrência para registro do ponto biométrico, no dia DATE

{h1} - Trabalhando home-office;
{h2} - {h3} Intervalo;
{h4} - Saída;


Att,

--
Níkolas Martins Vargas
Líder de Desenvolvimento de Software
Equipe de Tecnologia da Informação e Comunicação

Barbara Starfield
Telefone:(51) 3333-7025
http://www.ufrgs.br/telessauders/
"""

message = MIMEMultipart("alternative")
message['From'] = SENDER_EMAIL
message["To"] = RECEIVER_EMAIL
message["Cc"] = CC_MAIL

message['Subject'] = subject
message.attach(MIMEText(text, "plain"))


def run() -> bool:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        try:
            server.login(SENDER_EMAIL, PASSWORD)
            server.send_message(message)
        except Exception as error:
            print(error)
        else:
            return True
    return False


def main() -> str:
    ok = run()
    if ok:
        print('success')
        return
    print('fail')


main()
