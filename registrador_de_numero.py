import re

from datetime import datetime, timedelta
from numero_da_sorte import numero_da_sorte
from numerodasorte.models import Number, NumberApparition, NumberSequence
from main import db
from sqlalchemy import text

numbers_filter = """
select
    number.number,
    count(number_id) count_nid,
    numberapparition.apparition_datetime apparition_datetime
from
    number
left join
    numberapparition on number.id=numberapparition.number_id
where apparition_datetime >= '{date_limit}'
group by
    number_id, number.number, numberapparition.apparition_datetime
order by
    count_nid DESC limit 6;
"""

def numbers(qs):
    numbers = [n.number for n in qs]
    numbers.sort()
    return numbers

def generate_data_table():
    now = datetime.now()
    filters = (
        ("na última hora", now - timedelta(minutes=60)),
        ("de hoje", now - timedelta(days=1)),
        ("da semana", now - timedelta(days=7)),
        ("este mês", now - timedelta(days=30)),
        ("este ano", now - timedelta(days=365)),
    )

    sequences = tuple()
    for label, date_limit in filters:
        result = db.engine.execute(text(numbers_filter.format(date_limit=date_limit)))
        sequences += ((label, result),)

    format_numbers = lambda qs: "".join(["<span class=\"number\">%s</span>" % n for n in numbers(qs)])
    cell = lambda label, qs: ("<span class=\"time\">Mais sorteados %s</span>" % label + format_numbers(qs))

    table = "<div>"
    for label, sequence in sequences:
        try:
            table += "<div class='col-md-4'><div class='luck-number'>%s</div></div>" % cell(label, sequence)
        except IndexError:
            table += "<div class='col-md-4'><div class='luck-number'>&nbsp;</div></div>"
    table += "</div>"
    return table


def update_numbers_apparitions(sequence, current_datetime):
    """
    Atualiza as informações de aparições dos números na base de dados
    """
    numbers = re.findall(r'[0-9]+', sequence)
    for number in numbers:
        instance = Number.query.filter(Number.number == number).first()
        if instance:
            number_apparition = NumberApparition(number_id=instance.id, apparition_datetime=current_datetime)
            db.session.add(number_apparition)
            db.session.commit()


def add_sequence_to_database(sequence, current_datetime):
    """Insere a sequencia no banco como texto"""
    sequence_instance = NumberSequence(sequence=sequence, generation_datetime=current_datetime)
    db.session.add(sequence_instance)
    db.session.commit()


def generate_number(gen_datetime=None):
    sequence = numero_da_sorte()
    current_datetime = gen_datetime or datetime.now()
    number_sequence = NumberSequence(sequence=sequence, generation_datetime=current_datetime)
    db.session.add(number_sequence)
    db.session.commit()
    update_numbers_apparitions(sequence, current_datetime)
    return sequence


def get_latest_number():
    latest_number = NumberSequence.query.order_by('-id').first()
    return latest_number.sequence
