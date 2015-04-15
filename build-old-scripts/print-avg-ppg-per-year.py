import nfldb
db = nfldb.connect()

for year in range(1970, 2014 + 1):
    q = nfldb.Query(db)
    games = q.game(season_year=year, season_type='Regular').as_games()
    total_points = 0
    for g in games:
        total_points += g.home_score + g.away_score
    print "Year: %d # of Games: %d Avg Points Per Game: %.2f" %(year, len(games), total_points * 1.0 / len(games))

