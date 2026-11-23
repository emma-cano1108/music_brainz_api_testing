import musicbrainzngs as music_client

#User-Agent is needed for any request
music_client.set_useragent("EmmaTesting", 1.0, "emmatesting@test.com")

#Artists
#Generic query
#search_artists returns dict with two attributes: artist-list and artist-count
result = music_client.search_artists(query="Sodom")

#artist list contains each artist with the whole stored info in the MusicBrainz API
if result['artist-count'] != 0:
    for artist in result['artist-list']:
        name = artist.get("name")
        artist_type = artist.get("type")
        #Dict with id, area type (City, country...), area name, sort-name and life-span. Can be None
        area = artist.get("area")
        if (area is not None):
            print(f"Found {artist_type} named '{name}' from {area.get("name")}")
else:
    print("Could not find any artist using this query")

#Albums (release-group-list)
#Strict query with limits, search_release_groups get "albums"
result_2 = music_client.search_release_groups(query="888 Reencarnacion", strict=True, limit=5)
if result_2['release-group-count'] != 0:
    for album in result_2['release-group-list']:
        album_title = album.get("title")
        #YYYY-MM-DD formated date
        release_date = album.get("first-release-date")
        album_type = album.get("type")
        #List of dicts where each one is a related artist
        artist_credit = album.get("artist-credit")
        print(f"Found {album_type} named '{album_title}' released in {release_date} by:")
        for artist in artist_credit:     
            #Some strings like 'feat' or '&' are stored into artist_credit, these are discarded 
            if type(artist) is not str:   
                print(f"- {artist.get("name")}")
else:
    print("Could not find any album using this query")
#Songs (Recording)

result_3 = music_client.search_recordings(query="Panic", artist="Johnny Goth", strict=True, limit=10)
#Song is a dict where each attribute is a string
if result_3['recordings-count'] != 0:
    for song in result_3['recording-list']:
        song_title = song.get("title")
        #The length is measured in miliseconds
        length = song.get("length")
        #release-list returns an array with related albums or singles (dicts) where the song appears.
        release_list = song.get("release-list")
        print(f"Found song '{song_title}' and its length is {length} miliseconds")
        if release_list is not None:
            print("Related albums: ")
            for album in release_list:
                print(f" - {album.get("title")}")
        else:
            print(" - Could not find any related album for this song")
else:
    print("Could not find any song using this query")
