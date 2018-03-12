import calendar
import random
from datetime import datetime


def greetings(name):
    return random.choice([
        "Hola ¿que tal?",
        "Buenos dias/tardes",
        "Buenas",
        "Hola {}".format(name),
        "Konnichiha {}-san".format(name),
    ])


def before_day(day):
    if day == 'miercoles':
        return "espero que tengan un excelente dia de mier...coles"
    return random.choice([
        "como esta en este " + day,
        "espero que tenga un excelente " + day,
        "que le parece este " + day,
        "hoy es " + day,
    ])


def weekday(day):
    return {
        0: 'lunes',
        1: 'martes',
        2: 'miercoles',
        3: 'jueves',
        4: 'viernes',
    }[day]


def joke(day):
    if day == 'jueves':
        habla = "Hoy es dia de conbeber jeje"
    elif day == 'viernes':
        habla = "hoy es viernes e el cuerpo lo sabe :D"
    else:
        phrases = [
            "¿Mucho frio/calor ahi?",
            "Aquí Faro es el amo. :D",
            "¿Como esta el tiempo ahi?",
            "Aca sigue caliente como siempre :/",
        ]
        habla = random.choice(phrases)
    return habla


def main(name):
    calendar.setfirstweekday(calendar.SUNDAY)
    now = datetime.now()

    weekd = weekday(calendar.weekday(now.year, now.month, now.day))
    msg = "{}. {}. {}".format(greetings(name), before_day(weekd), joke(weekd))
    msg = random.choice([msg, 'Oi internautas!', msg])
    return msg
