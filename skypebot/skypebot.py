import re
from datetime import datetime, timedelta, timezone
from time import sleep

import wikipedia
from wikipedia import DisambiguationError

from actions import allegro
from actions import cama
from actions import coin
from actions import fujam
from actions import hola
from actions.dict import dict
from actions.ista import ista
from actions.ponto import ponto


KEYWORDS = {
    'help': ('@ro help', '<at id="8:live:976d89d0eaa03977">Ro</at> help'),
    'fujam': ('fujam', '#fujam', 'fujam para as colinas'),
    'commit': ('#commit',),
    'hola': ('#hola',),
    'coin': ('rb©oin', 'rb©'),
    'lunch': ('#almoco', '#almoço', '#lunch'),
    'allegro': ('#allegro', '#cardapio_allegro', '#cardapioAllegro', '#cardapioallegro'),
    'menus': ('#cardapios', '#cardapio'),
    'bom_dia_silvinho': ('bom dia silvinhobot',),
}
BRAZIL_TIMEZONE = timezone(-timedelta(hours=3), 'Brazil')
wikipedia.set_lang("pt")


def handle(event):
    message = event.msg.content.lower()

    coin.coin(event)

    keywords_mapping = (
        (_ponto, message.startswith('ponto')),
        (_ista, message.endswith('ista')),
        (_pregunton, message.endswith('???')),
        (_hot_today, message.endswith('calor infernal aqui?')),
        (_radical, 'é disso que eu gosto' in message),
        (_radical, 'é disso q eu gosto' in message),
        (_piorou, 'tava ruim' in message),
        (_piorou, 'tava meio ruim' in message),
        (_dict, '#dict' in message),
        (_wiki, '#wiki' in message),
        (_bom_dia_silvinho, message in KEYWORDS['bom_dia_silvinho']),
        (_allegro, message in KEYWORDS['allegro']),
        (_coin, message in KEYWORDS['coin']),
        (_help, message in KEYWORDS['help']),
        (_fujam, message in KEYWORDS['fujam']),
        (_commit, message in KEYWORDS['commit']),
        (_hola, message in KEYWORDS['hola']),
        (_lunch, message in KEYWORDS['lunch']),
        (_menus, message in KEYWORDS['menus']),
        (_chapeu, 'tirei o chapéu' in message),
        (_chapeu, 'ter um chapéu, só para tira-lo' in message),
        (_chapeu, 'ter um chapéu só para tira-lo' in message),
        (_chapeu, 'tirou o chapéu' in message),
        (_chapeu, 'tirei o chapeu' in message),
        (_chapeu, 'tirou o chapeu' in message),
    )

    for function, match in keywords_mapping:
        if match:
            event.msg.chat.setTyping()
            function(event)
            break


def _chapeu(event):
    with open('tirei-o-chapeu1.jpg', 'rb') as image1:
        with open('tirei-o-chapeu2.jpg', 'rb') as image2:
            event.msg.chat.sendFile(image1, 'chapeu1.jpg', image=True)
            event.msg.chat.sendFile(image2, 'chapeu2.jpg', image=True)


def _radical(event):
    event.msg.chat.sendMsg('RADICAAAAL!!!')


def _help(event):
    help = """
    - ? - Amigo pregunton (mariachilove)
    - #commit - #CAMA
    - #hola - Hola
    - ponto {chegada} {?saida_intervalo},{volta_intervalo?} {?horas a trabalhar?} - ponto
    - #ista - ista
    """
    event.msg.chat.sendMsg(help)


def _ista(event):
    event.msg.chat.sendMsg(ista())


def _fujam(event):
    event.msg.chat.sendMsg(fujam.switch_two())


def _piorou(event):
    event.msg.chat.sendMsg('agora parece q piorou')


def _pregunton(event):
    event.msg.chat.sendMsg('AAAAAAAAH QUE AMIGO TAN PREGUNTON!!!')
    event.msg.chat.sendMsg('(mariachilove)')


def _commit(event):
    cama.main(event.msg.chat.sendMsg)


def _hola(event):
    event.msg.chat.sendMsg(hola.main(event.msg.user.name.first))


def _ponto(event):
    params = event.msg.content.split(' ')
    horario = params[1]
    rest_hours = params[2] if len(params) > 2 else '1:00'
    working = params[3] if len(params) > 3 else '8:30'
    event.msg.chat.sendMsg(ponto(horario, working, rest_hours))


def _dict(event):
    regex_pattern = '</legacyquote>([a-záàâãéèêíïóôõöúç]*)<legacyquote>'
    msg = event.msg.content.lower()

    word = re.findall(regex_pattern, msg)[0]
    try:
        event.msg.chat.sendMsg('{}\n{}'.format(*dict(word)))
    except IndexError:
        event.msg.chat.sendMsg('Não achei essa palavra: {}'.format(word))


def _coin(event):
    coin.status(event)


def _lunch(event):
    now = datetime.now(tz=BRAZIL_TIMEZONE)
    lunch_time = now.replace(hour=11, minute=30)

    if now == lunch_time:
        event.msg.chat.sendMsg('#PartiuAlmoço')
        return
    elif now > lunch_time:
        # Tomorrow lunch
        lunch_time += timedelta(days=1)

    seconds_left = (lunch_time - now).seconds
    minutes, seconds = divmod(seconds_left, 60)
    hours, minutes = divmod(minutes, 60)
    msg = 'Faltam {}h{}min para o almoço'.format(hours, minutes)
    event.msg.chat.sendMsg(msg)


def _hot_today(event):
    event.msg.chat.sendMsg('impressão tua')


def _allegro(event):
    date_posted, image = allegro.get_menu_image_content()
    if image:
        event.msg.chat.sendFile(image, 'allegro.jpg', image=True)
    else:
        msg_format = 'Último cardápio do Allegro foi publicado dia {}'
        formated_date_posted = date_posted.strftime('%d/%m/%Y')
        event.msg.chat.sendMsg(msg_format.format(formated_date_posted))


def _menus(event):
    menus = (
        '#allegro',
        '#cardapioAltis',
        '#cardapioCantina',
        '#cardapioDelicia',
    )
    for menu in menus:
        event.msg.chat.sendMsg(menu)


def _bom_dia_silvinho(event):
    sleep(1)
    if event.msg.chat.getMsgs()[0].userId == 'live:silvinho485_1':
        event.msg.chat.setTyping(active=False)
        return
    msg = 'devido a realização de atividade durante a madrugada, o Silvinho ira chegar um pouco mais tarde.' # noqa
    event.msg.chat.sendMsg(msg)


def _wiki(event):
    regex_pattern = '</legacyquote>([a-záàâãéèêíïóôõöúç -]*)<legacyquote>'
    msg = event.msg.content.lower()

    word = re.findall(regex_pattern, msg)[0]
    try:
        page = wikipedia.page(word)
        content_lines = page.content.split('\n')
        event.msg.chat.sendMsg('{}\n{}'.format(content_lines[0], page.url))
    except DisambiguationError as error:
        msg_format = 'Desambiguação de {}: {}'
        options = ', '.join(error.options)
        event.msg.chat.sendMsg(msg_format.format(error.title, options))
    except IndexError:
        event.msg.chat.sendMsg('Não achei no Wikipedia: {}'.format(word))
