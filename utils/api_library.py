import json, requests, urllib2
import random
from requests.auth import HTTPBasicAuth

lastfm_key = "e711999d7d3e55af0f0d28b12de31bfb"



#input: diary entry
#output: a dictionary --> {Anger:<score> , Joy:<score> , Fear:<score> , Sadness:<score>, Disgust:<score>}
#score is from 0 to 1
#this dictionary of mood info should be stored in diary table of db
#-------------------------------------------------------------------
def analyze_tone(diary_entry):
    encoded_entry = urllib2.quote(diary_entry)
    link =  'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2016-05-19&text=' + encoded_entry

    tone_results = requests.get(link, auth=HTTPBasicAuth("11595b44-c4bf-4abd-bd37-404256bde5a6","1vPhhGJ2V7Xu"))

    #tone_results is now a dictionary 
    tone_results = tone_results.json()

    tone_scores_dict = {}
    
    #print tone_results

    for d in (tone_results["document_tone"])["tone_categories"][0]["tones"]:
        tone_scores_dict[d["tone_name"]] = d["score"]
        
    #print tone_scores_dict
    return tone_scores_dict


#finds most prevalent mood
#input: the mood info dict from the diary table of db
#output: string of the mood w/ highest score e.g. "Joy"
#----------------------------------------------------------
def primary_tone(mood_info_dict):
    max_score = mood_info_dict["Joy"]
    max_mood = "Joy"
    for key in mood_info_dict:
        if mood_info_dict[key] > max_score:
            max_mood = key

    return max_mood
        

#input: 1-3 stars, song name, artist name
#output: list of [child song, child son artist]
#when user is recommended the inputted song depending on what they rate it they will be given a child song as determined by this fxn
#-----------------------------------------------------------------------------------------------------------------------------------
def get_child_songs(num_stars, song, artist):
    artist_encoded =  urllib2.quote(artist)
    song_encoded =  urllib2.quote(song)
    link = "http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist=" + artist_encoded + "&track=" + song_encoded + "&api_key=" + lastfm_key + "&format=json"

    u= urllib2.urlopen(link)
    info = u.read()
    similiar_tracks_dict = json.loads(info)

    child_song = []

    rand_num = 0
    
    if num_stars == "one":
        rand_num = random.randint(0,32)
        
    if num_stars == "two":
        rand_num = random.randint(33,66)

    if num_stars == "three":
        rand_num = random.randint(67,99)

    child_song.append(similiar_tracks_dict["similartracks"]["track"][rand_num]["name"])
    child_song.append(similiar_tracks_dict["similartracks"]["track"][rand_num]["artist"]["name"])

    child_song[0] = (child_song[0]).replace("'", "")
    child_song[1] = (child_song[1]).replace("'", "")

    return child_song

    
#returns not youtube link, last.fm link
#-------------------------------------------------------
def get_link(song,artist):
    song_encoded = urllib2.quote(song)
    link = "http://ws.audioscrobbler.com/2.0/?method=track.search&track=" + song_encoded + "&api_key=" + lastfm_key + "&format=json"
    u= urllib2.urlopen(link)
    info = u.read()
    search_results = json.loads(info)

    search_results = search_results["results"]["trackmatches"]["track"]

    
    for i in range(3):
        if ((search_results[i]["artist"]).replace("'", "")).lower() == artist:
            url = search_results[i]["url"]
            return url
    
#TEST CASES ------------------------------
#print get_link("let it be", "the beatles")
#print  get_child_songs(1, "the night we met", "lord huron")
#print "\n\n\n"
#d = analyze_tone("i like pie")
#print d
#print "\n\n"
#print primary_tone(d)


