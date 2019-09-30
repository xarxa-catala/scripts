import argparse
import requests
import json

URL = "https://api.multimedia.xarxacatala.cat"

def main():
    args = doArgs()
    show_id = getShowID(args.show)
    season_id = getSeasonID(show_id, args.season)
    episodes = getEpisodes(show_id, season_id)
    minisodes = getEpisodes(show_id, season_id, True)
    episodes.update(minisodes)
    
    print (episodes)

def doArgs():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--show", type=str, help="Show name: DW, OP, TSJA, TW, Class.", required=True)
    parser.add_argument("--season", type=str, help="Season number: 1, 2, 3...", required=True)
    
    return parser.parse_args()

def getShowID(show):
    r = requests.get(url=URL+"/shows")
    shows = json.loads(r.text)
    for s in shows:
        if s["name"] == show:
            return (s['id'])

def getSeasonID(show_id, season):
    r = requests.get(url=URL+"/shows/"+str(show_id)+"/seasons")
    seasons = json.loads(r.text)
    for s in seasons:
        if s["number"] == int(season):
            return (s["id"])

def getEquels(show_id, season_id, episode_id, equel_type):
    r = requests.get(url=URL+"/shows/"+str(show_id)+"/seasons/"+str(season_id)+"/episodes/"+str(episode_id)+"/"+equel_type)
    equels = json.loads(r.text)
    equels_dict = {}
    for e in equels:
        equels_dict[e["url"]] = e["name"]
    return equels_dict

def getEpisodes(show_id, season_id, minisode=False):
    url = URL+"/shows/"+str(show_id)+"/seasons/"+str(season_id)+"/episodes"
    if minisode:
        url = URL+"/shows/"+str(show_id)+"/seasons/"+str(season_id)+"/minisodes"
    r = requests.get(url=url)
    episodes = json.loads(r.text)
    episodes_dict = {}
    if not minisode:
        for e in episodes:
            episodes_dict.update(getEquels(show_id, season_id, e["id"], "prequels"))
            episodes_dict[e["url"]] = e["name"]
            episodes_dict.update(getEquels(show_id, season_id, e["id"], "sequels"))
    return episodes_dict

main()
