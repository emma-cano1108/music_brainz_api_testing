#Syntactic search and categoric filters applied to MusicBrainz API info
import musicbrainzngs

#User-Agent is needed for any request
musicbrainzngs.set_useragent("EmmaTesting", 1.0, "emmatesting@test.com")

#Generic query
#search_artists returns dict with two attributes: artist-list and artist-count
result = musicbrainzngs.search_artists(query="Metallica")

#artist list contains each artist with the whole stored info in the MusicBrainz API
for artist in result['artist-list']:
    name = artist.get("name")
    artist_type = artist.get("type")
    #Dict with id, area type (City, country...), area name, sort-name and life-span. Can be None
    area = artist.get("area")
    if (area is not None):
        print(f"Found {artist_type} named '{name}' from {area.get("name")}")
