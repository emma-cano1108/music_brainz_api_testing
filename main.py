#Syntactic search and categoric filters applied to MusicBrainz API info
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
result_3 = music_client.search_recordings(query="vampiro", artist="french police", strict=True, limit=10)

#Song is a dict where each attribute is a string
if result_3['recording-count'] != 0:
    for song in result_3['recording-list']:
        song_title = song.get("title")
        #The length is measured in milliseconds
        length = song.get("length")
        #release-list returns an array with related albums or singles (dicts) where the song appears.
        release_list = song.get("release-list")
        print(f"Found song '{song_title}' and its length is {length} milliseconds")
        if release_list is not None:
            print("Related albums: ")
            for album in release_list:
                print(f" - {album.get("title")}")
        else:
            print(" - Could not find any related album for this song")
else:
    print("Could not find any song using this query")


#Albums with its songs
result_4 = music_client.search_release_groups(query="Verdun 1916", strict=True, limit=5)

if result_4['release-group-count'] != 0:

    #Only first release group found is used to get the first release id
    #(release-group-list contains many release-groups which each one contains a release-list) 
    first_group = result_4['release-group-list'][0]
    first_album_id = first_group['release-list'][0].get('id')

    if first_album_id is not None:
        #album_details stores the release info including each song
        #get_release_by_id returns an object whose first value is "release", that contains the whole info
        album_details = music_client.get_release_by_id(first_album_id, includes=['recordings'])['release']
        #mediums is an array that represents CD's/Vinyls that contain the songs
        mediums = album_details.get('medium-list')

        album_title = album_details.get('title')
        if mediums is not None:
            for medium in mediums:
            #track-list is an array that contains each song in the medium
                songs = [track for track in medium.get('track-list')]

            print(f"The album '{album_title}' contains these {len(songs)} songs: ")

            for song in songs:
                #Each element of track-list contains a "recording" value, that represents a recording entity (seen above)
                track_info = song.get('recording')
                print(f" - {track_info.get('title')}")
        else:
            print(f"Could not find mediums for '{album_title}'. Songs can not be displayed")
    else:
        print("Could not find album id using this query")

else:
    print("Could not find any album using this query")