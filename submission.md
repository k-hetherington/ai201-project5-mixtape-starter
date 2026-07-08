# AI Usage

(To be completed as we work.)

---

# Codebase Map

## Main Files

(To be completed.)

## Data Flow

(To be completed.)

---

# Root Cause Analysis
## Issue #5 – The last song in a playlist never shows up

### How I reproduced it

I started the Flask app and opened the playlist detail endpoint for the Friday Energy playlist:

GET /playlists/fa64daf5-02fc-486a-8b60-480630772183

The playlist detail showed `song_count: 7`.

Then I opened:

GET /playlists/fa64daf5-02fc-486a-8b60-480630772183/songs

That endpoint returned `count: 6`, which confirmed the bug because the playlist said it had 7 songs but only 6 were returned.

### How I found the root cause

I started from the endpoint GET /playlists/<playlist_id>/songs, then looked at routes/playlists.py to see which service function it called. That led me to get_playlist_songs() in services/playlist_service.py. The query itself returned the playlist songs in position order, but the return statement used songs[:-1], which removes the final song from the list.

### The root cause

The get_playlist_songs() function was slicing the song list with songs[:-1]. In Python, that returns every item except the last one. Since the playlist songs were already ordered by position, the last item was always the most recently added song. This caused the newest playlist song to be hidden every time.


### My fix and check

I changed the return statement from songs[:-1] to songs so the function returns every song in the playlist. After the fix, I refreshed the Friday Energy playlist songs endpoint and confirmed the count changed from 6 to 7, matching the playlist detail endpoint.

---

## Issue #4 – Rating notifications

### How I reproduced it

### How I found the root cause

### The root cause

### My fix and side-effect check

---

## Issue #2 – Friends Listening Now

### How I reproduced it

### How I found the root cause

### The root cause

### My fix and side-effect check

---

# Git Log Screenshot

(Add your screenshot here before submitting.)