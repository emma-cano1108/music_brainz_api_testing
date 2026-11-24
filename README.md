# MusicBrainz API Testing

A lightweight Python project testing queries on the [MusicBrainz](https://musicbrainz.org/) database using the [`musicbrainzngs`](https://python-musicbrainzngs.readthedocs.io/) wrapper. The repo showcases how to authenticate queries, perform syntactic searches, apply filters, and parse nested data across different core MusicBrainz entities.

---

## Overview

The main script (`main.py`) performs four distinct query operations against the MusicBrainz Web Service:

1. **Artist Search** — Finds artists matching a query string and displays their name, type, and geographic origin.
2. **Release Group (Album) Search** — Performs a strict query with a result limit to retrieve album details, release dates, and credited artists.
3. **Recording (Song) Search** — Performs a filtered search by track title and artist name, extracting song duration and associated releases.
4. **Album + Track Listing** — Retrieves a release group, resolves its first concrete release by ID, and lists every song it contains across its physical media (CDs, Vinyls, etc.).

---

## Query Parameters

Every search function in `musicbrainzngs` accepts parameters that shape what gets returned. These can be freely changed to target different searches:

| Parameter | Type | Effect |
|---|---|---|
| `query` | `str` | Main search term. Change it to look for different artists, albums, or songs. |
| `artist` | `str` | Filters results to those credited to a specific artist.
| `strict` | `bool` | When `True`, the search requires a close match to the query. When `False` (default), fuzzy/broad matching is used. |
| `limit` | `int` | Maximum number of results returned (default: 25, max: 100).

**Parameters used in the example:**

```python
# Broad search — returns any artist vaguely matching "Sodom"
music_client.search_artists(query="Sodom")

# Strict filtered search — only recordings named "vampiro" by "french police"
music_client.search_recordings(query="vampiro", artist="french police", strict=True, limit=10)

# Strict album search capped at 5 results
music_client.search_release_groups(query="888 Reencarnacion", strict=True, limit=5)
```

---

## MusicBrainz Entities & Data Structures

MusicBrainz organizes musical data using specific core entities. Below each entity's description you will find a minimal diagram showing how the response data is structured.

>[!NOTE]
> **TO HAVE IN ACCOUNT** : these diagrams **DO NOT** show the whole entity structure and attributes, only the attributes used for this repo

---

### 1. Artist (`artist`)

Represents an individual musician, a group/band, or another music creator.

- **Query Method**: `music_client.search_artists(...)`
- **Response key checked**: `artist-count` (to verify results exist), then `artist-list`

**Attributes used:**
- `name` *(str)*: Official display name of the artist or band.
- `type` *(str)*: Classification — `Group`, `Person`, `Orchestra`, etc.
- `area` *(dict | None)*: Geographic entity linked to the artist. Can be `None`.

**Response structure:**

```
search_artists() response
│
├── "artist-count"  →  int  (total matches found)
│
└── "artist-list"   →  [ artist, artist, ... ]
                           │
                           ├── "name"   →  str  ("Sodom")
                           ├── "type"   →  str  ("Group")
                           └── "area"   →  dict | None
                                              └── "name"  →  str  ("Gelsenkirchen")
```

---

### 2. Release Group (`release-group`)

Represents an abstract musical work: an album concept that groups together all physical and digital versions (editions, remasters, regional releases) of a title.

- **Query Method**: `music_client.search_release_groups(...)`
- **Response key checked**: `release-group-count`, then `release-group-list`

**Attributes used:**
- `title` *(str)*: Title of the album or release group.
- `type` *(str)*: Primary type — `Album`, `Single`, `EP`, etc.
- `first-release-date` *(str)*: Earliest known release date in `YYYY-MM-DD` format.
- `artist-credit` *(list)*: Mixed list of artist dicts and join strings like `" feat. "` or `" & "`. Non-dict entries are filtered out in code.
- `release-list` *(list of dicts)*: Concrete releases (editions) under this group. Each one contains an `id` used to fetch full release details.

**Response structure:**

```
search_release_groups() response
│
├── "release-group-count"  →  int
│
└── "release-group-list"   →  [ release-group, ... ]
                                      │
                                      ├── "title"               →  str
                                      ├── "type"                →  str
                                      ├── "first-release-date"  →  str  ("YYYY-MM-DD")
                                      ├── "artist-credit"       →  [ dict | str, ... ]
                                      │       ├── { "name": str, ... }   ← artist dict
                                      │       └── " & "                  ← join string (filtered out)
                                      └── "release-list"        →  [ { "id": str, ... }, ... ]
                                                                        └── "id"  →  used in get_release_by_id()
```

---

### 3. Recording (`recording`)

Represents an audio track: a distinct recording that can appear across multiple albums or singles.

- **Query Method**: `music_client.search_recordings(...)`
- **Response key checked**: `recording-count`, then `recording-list`

**Attributes used:**
- `title` *(str)*: Title of the recorded track.
- `length` *(int | str)*: Duration in **milliseconds**.
- `release-list` *(list of dicts | None)*: Releases (albums, compilations, singles) where this recording appears.

**Response structure:**

```
search_recordings() response
│
├── "recording-count"  →  int
│
└── "recording-list"   →  [ recording, ... ]
                               │
                               ├── "title"        →  str  ("vampiro")
                               ├── "length"       →  str  ("210000")  ← milliseconds
                               └── "release-list" →  [ release, ... ] | None
                                                          └── "title"  →  str  (album name)
```

---

### 4. Release + Medium + Track (album song listing)

A **Release Group** contains multiple concrete **Releases** (e.g., CD edition, vinyl edition). Each **Release** has a `medium-list` that represents the physical media (a CD, a vinyl side, etc.). Each medium has a `track-list` with the actual songs, where each track wraps a full **Recording** entity.

- `music_client.search_release_groups()` — find the album, get a release `id` from `release-list[0]`.
- `music_client.get_release_by_id(id, includes=["recordings"])` — fetch the full release with all track data.

**Attributes used:**
- `medium-list` *(list)*: Array of media (CDs/Vinyls).
- `track-list` *(list)*: Songs within each medium.
- `recording` *(dict)*: Full recording entity embedded in each track, containing `title`, `length`, etc.

**Nested data structure:**

```
get_release_by_id() response
│
└── "release"
       │
       ├── "title"        →  str  (album name)
       └── "medium-list"  →  [ medium, medium, ... ]   ← one per CD/vinyl
                                   │
                                   └── "track-list"  →  [ track, track, ... ]
                                                              │
                                                              ├── "number"     →  str  ("1", "2", ...)
                                                              ├── "position"   →  str
                                                              └── "recording"  →  dict
                                                                       │
                                                                       ├── "title"   →  str  (song title)
                                                                       └── "length"  →  str  (ms)
```

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/emma-cano1108/music_brainz_api_testing
```

### 2. Create and Activate a Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py
```

>[!NOTE]
> **User-Agent** : MusicBrainz methods used here require all client applications to identify themselves before sending queries. This is set once by using `music_client.set_useragent("AppName", "Version", "contact@example.com")`

