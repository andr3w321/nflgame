import xml.dom.minidom as xml
import os
import re 

nfl_schedules_path = './nfl-schedules'

def sort_nicely( l ): 
  """ Sort the given list in the way that humans expect. 
  """ 
  convert = lambda text: int(text) if text.isdigit() else text 
  alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
  l.sort( key=alphanum_key ) 

def get_filenames(dir_path, starts_with, ends_with):
    """
    Returns a list of all filenames in a dir
    that starts with a given string 
    and ends with a given string
    eg: get_filenames("./nfl-schedules", "1970", ".xml")
    """
    filenames = []
    try:
        for file in os.listdir(dir_path):
            if file.startswith(starts_with) and file.endswith(ends_with):
                filenames.append(file)
    except OSError:
        sys.stderr.write("could not load %s\n" % dir_path)
    return filenames

def add_sym_mascot_year(sym, mascot, year, teams):
    team_idx = -1
    for i in range(0, len(teams)):
        if teams[i][0] == sym and teams[i][1] == mascot:
            team_idx = i
            break
    if team_idx == -1:
        teams.append([sym.encode('utf-8'), mascot.encode('utf-8'), [year]])
    else:
        if year not in teams[team_idx][2]:
            teams[team_idx][2].append(year)
    return teams


xml_filenames = get_filenames(nfl_schedules_path, "", ".xml")
sort_nicely(xml_filenames)
xml_filenames.reverse()
teams = []
for xml_file in xml_filenames:
    year,week,stype = xml_file.split(".xml")[0].split("-")
    year = int(year)
    week = int(week)

    xml_filename = nfl_schedules_path + "/" + str(year) + "-" + str(week) + "-" + stype + ".xml"
    try:
        dom = xml.parse(open(xml_filename))
    except IOError:
        sys.stderr.write("could not load %s\n" % xml_filename)


    for g in dom.getElementsByTagName("g"):
        home_sym = g.getAttribute('h')
        home_mas = g.getAttribute('hnn')
        away_sym = g.getAttribute('v')
        away_mas = g.getAttribute('vnn')

        teams = add_sym_mascot_year(home_sym, home_mas, year, teams)
        teams = add_sym_mascot_year(away_sym, away_mas, year, teams)
teams.sort()
for team in teams:
    print team
