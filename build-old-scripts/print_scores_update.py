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

def printsql(field_updated, gsis_ids, field_values):
    print "update game set %s = data_table.%s from (select unnest(array%s) as gsis_id, unnest(array%s) as %s) as data_table where game.gsis_id = data_table.gsis_id;" % (field_updated, field_updated, gsis_ids, field_values, field_updated)

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

    gsis_ids = []
    home_scores = []
    away_scores = []
    for g in dom.getElementsByTagName("g"):
        gsis_ids.append(g.getAttribute('eid').encode('utf-8'))
        home_scores.append(int(g.getAttribute('hs')))
        away_scores.append(int(g.getAttribute('vs')))

    printsql("home_score", gsis_ids, home_scores)
    printsql("away_score", gsis_ids, away_scores)

