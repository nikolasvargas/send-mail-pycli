import configparser
import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional


config = configparser.ConfigParser()
config.read('mail.ini')

SENDER_EMAIL: str = config['MAIL']['FROM']
RECEIVER_EMAIL: str = config['MAIL']['TO']
CC_MAIL: Optional[str] = config['MAIL'].get('CC', None)
BCC_MAIL: Optional[str] = config['MAIL'].get('BCC', None)
PASSWORD: str = config['MAIL']['PASSWD']
SMTP_SERVER: str = config['SERVER']['HOST']
PORT: int = int(config['SERVER']['PORT'])


def _input(label: str) -> str:
    return input(label).strip()


date = _input('date: ')
h1 = _input('start: ')
h2 = _input('lunch start: ')
h3 = _input('lunch end: ')
h4 = _input('end: ')

subject = f'Ocorrência Ponto - {date}'

text = f"""\
Informo ocorrência para registro do ponto biométrico, no dia {date}

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


def _get_message() -> MIMEMultipart:
    message = MIMEMultipart('alternative')
    message['From'] = SENDER_EMAIL
    message['To'] = RECEIVER_EMAIL
    message['Cc'] = CC_MAIL
    message['Bcc'] = BCC_MAIL or SENDER_EMAIL
    message['Subject'] = subject
    message.attach(MIMEText(text, 'plain'))

    return message


def run() -> bool:
    msg = _get_message()
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        try:
            server.login(SENDER_EMAIL, PASSWORD)
            server.send_message(msg)
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
