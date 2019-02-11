from db import *
import statistics

# must have at least 10 plate appearances
minAtBats = 10
minInnings = 10
db_type = 'sqllite'
# db_type = 'postgres'

db = get_connection(db_type)
player_model = get_player_model(db)
pl = player_model.select()

# calc min, max and stdv on ops
# create a list ops for the entire league
ops_list = []
for stats in pl.iterator():
    if stats.ab > minAtBats:
        ops_list.append(stats.ops)

print('League OPS Stats (minimum '+str(minAtBats)+' at bats)')
print('')
print('League min OPS: ', min(ops_list))
print('League max OPS: ', max(ops_list))
print('League avg OPS: ', round(sum(ops_list)/len(ops_list),3))
print('League ops STDV: ', round(statistics.stdev(ops_list),3))
print('')

# list players with ops over .8
pl = player_model.select()

print('League OPS leaders (OPS > .8)')
print('Team'.ljust(20), 'Player'.ljust(20), 'OPS'.ljust(10))
for stats in pl.iterator():
    if stats.ab > minAtBats and stats.ops > .8:
        print(stats.team.ljust(20), stats.name.ljust(20), str(round(stats.ops, 3)).ljust(10))

era_list = []
pitcher_model = get_pitcher_model(db)
pt = pitcher_model.select()
for stats in pt.iterator():
    if stats.ip > 10:
        era_list.append(stats.era)
print('')
print('')
print('League ERA Stats (minimum '+str(minInnings)+' innings pitched)')
print('')
print('League min ERA', min(era_list))
print('League max ERA', max(era_list))
print('League avg ERA', round(sum(era_list)/len(era_list),2))
print('League era STDV', round(statistics.stdev(era_list),3))
print('')
print('League ERA Leaders (ERA < 3)')
print('Team'.ljust(20), 'Player'.ljust(20), 'ERA'.ljust(10), 'IP'.ljust(10))
pt = pitcher_model.select()
for stats in pt.iterator():
    if stats.ip > 10 and stats.era < 3:
        print(stats.team.ljust(20), stats.name.ljust(20), str(round(stats.era, 2)).ljust(10), str(stats.ip).ljust(10))
