# -*- coding: utf-8 -*-
from main import db
from numerodasorte.models import Number
from registrador_de_numero import generate_number


def run():

    for x in range(1, 61):
        db.session.add(Number(number=("%02d" % x)))
        db.session.commit()
        generate_number()


if __name__ == '__main__':
    run()