#Syntactic search and categoric filters applied to MusicBrainz API info
import musicbrainzngs as music_client

#User-Agent is needed for any request
music_client.set_useragent("EmmaTesting", 1.0, "emmatesting@test.com")

#Generic query
#search_artists returns dict with two attributes: artist-list and artist-count
result = music_client.search_artists(query="Sodom")

#artist list contains each artist with the whole stored info in the MusicBrainz API
for artist in result['artist-list']:
    name = artist.get("name")
    artist_type = artist.get("type")
    #Dict with id, area type (City, country...), area name, sort-name and life-span. Can be None
    area = artist.get("area")
    if (area is not None):
        print(f"Found {artist_type} named '{name}' from {area.get("name")}")

#Strict query with limits, search_release_groups get "albums"
result_2 = music_client.search_release_groups(query="888 Reencarnacion", strict=True, limit=5)

for album in result_2['release-group-list']:
    title = album.get("title")
    #YYYY-MM-DD formated date
    release_date = album.get("first-release-date")
    album_type = album.get("type")
    #List of dicts where each one is a related artist
    artist_credit = album.get("artist-credit")
    print(f"Found {album_type} named {title} released in {release_date} by:")
    for artist in artist_credit:     
        #Some strings like 'feat' or '&' are stored into artist_credit, these are discarded 
        if type(artist) is not str:   
            print(f"- {artist.get("name")}")