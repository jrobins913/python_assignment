from peewee import *


def get_connection(type):
    if type == 'sqllite':
        db = SqliteDatabase('big10.db')
        db.connect()
    elif type == 'postgres':
        db = PostgresqlDatabase('postgres', user='postgres', password='password_here',
                           host='localhost', port=5432)
        db.connect()

    return db


def create_tables(models, db):
    db.create_tables(models)


def get_player_model(db):
    class Player(Model):
        name = CharField()
        team = CharField()
        position = CharField()
        ba = DecimalField()
        obp = DecimalField()
        slg = DecimalField()
        ops = DecimalField()
        ab = IntegerField()

        class Meta:
            database = db

    return Player


def get_player_fields(db):
    pm = get_player_model(db)
    fields = [pm.name, pm.team, pm.position, pm.ba, pm.obp, pm.slg, pm.ops, pm.ab]
    return fields


def get_pitcher_fields(db):
    pt = get_pitcher_model(db)
    fields = [pt.name, pt.team, pt.win, pt.loss, pt.era, pt.ip]
    return fields


def get_pitcher_model(db):
    class Pitcher(Model):
        name = CharField()
        team = CharField()
        win = IntegerField()
        loss = IntegerField()
        era = DecimalField()
        ip = DecimalField()

        class Meta:
            database = db

    return Pitcher


def insert_player(name, team, position, ba, obp, slg, ops, ab):

    player_model = get_player_model(db)

    player = player_model(name=name, team = team, position=position, ba=ba, obp=obp, slg=slg, ops=ops, ab=ab)
    player.save()


def insert_pitcher(name,team,win,loss,era, ip):

    pitcher_model = get_pitcher_model(db)

    pitcher = pitcher_model(name=name, team=team, win=win, loss=loss, era=era, ip=ip)
    pitcher.save()


def drop_all(models, db):
    db.drop_tables(models)


