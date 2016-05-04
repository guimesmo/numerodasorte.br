from main import db


class ModelMixin(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Number(ModelMixin, db.Model):
    __tablename__ = 'number'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String())

    def __repr__(self):
        return repr(self.number)

    def __str__(self):
        return self.number


class NumberApparition(ModelMixin, db.Model):
    __tablename__ = 'numberapparition'
    id = db.Column(db.Integer, primary_key=True)
    number_id = db.Column(db.Integer, db.ForeignKey('number.id'))
    apparition_datetime = db.Column(db.DateTime(timezone=True))


class NumberSequence(ModelMixin, db.Model):
    __tablename__ = 'numbersequence'

    id = db.Column(db.Integer, primary_key=True)
    generation_datetime = db.Column(db.DateTime(timezone=True))
    sequence = db.Column(db.String())

    def __repr__(self):
        return repr(self.sequence)

    def __str__(self):
        return self.sequence
