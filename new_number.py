# -*- coding: utf-8 -*-
from timer import RepeatedTimer
import time

from datetime import datetime
from registrador_de_numero import generate_number


def new_number():
    """Gera um novo numero com registro do datetime da solicitacao"""
    print('.', end="", flush=True)
    now = datetime.now()
    generate_number(gen_datetime=now)

if __name__ == '__main__':
    print("Running", end="", flush=True)
    rt = RepeatedTimer(1, new_number)


