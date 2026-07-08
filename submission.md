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

I traced the rating endpoint from routes/songs.py. The route POST /songs/<song_id>/rate calls rate_song() in services/notification_service.py.

Before changing the code, I rated a song shared by another user and then checked the original sharer's notifications endpoint:

GET /users/<shared_by_user_id>/notifications

The rating was saved, but no notification appeared, which matched the reported issue.

### How I found the root cause

I compared the working playlist notification path to the rating path in services/notification_service.py. The add_to_playlist() function creates a notification after adding a song to a playlist. The rate_song() function had similar user and song lookup logic, but after saving the rating it only committed and returned the rating. It never created a notification.

### The root cause

The rating logic was missing the notification creation step. The function saved or updated a Rating record, but it did not call create_notification() afterward. Because of that, the rating existed in the database, but the song sharer never received a notification.

### My fix and check

I added a create_notification() call after the rating commit, only when the rater is not the original sharer. This matches the pattern used by playlist-add notifications and avoids notifying users about their own actions. After the fix, I rated another user's song again and confirmed that the original sharer received a new song_rated notification.

---

## Issue #2 – Friends Listening Now

### How I reproduced it
I read the issue description and traced the endpoint GET /feed/<user_id>/listening-now. The issue described that users who listened late the previous evening still appeared in the "Listening Now" feed the next morning. I tested the endpoint using one of the seeded users and confirmed that the feed logic was based on a rolling time window rather than the current calendar day.

### How I found the root cause
I started with the route in routes/feed.py, which calls get_friends_listening_now() in services/feed_service.py. Inside that function, I found the cutoff time was calculated using datetime.now(timezone.utc) minus a 24-hour timedelta. That explained why listening events from yesterday evening were still included the following morning.

### The root cause
The function filtered listening events using a rolling 24-hour window (datetime.now() - timedelta(hours=24)). That allowed listening events from late the previous evening to remain visible the next morning. The feature requirements expected "Listening Now" to include only events from the current calendar day.

### My fix and check
I changed the cutoff from a rolling 24-hour window to the start of the current day by setting the cutoff time to midnight. This ensures that only today's listening events appear in the feed. I verified that events from the current day are still returned while events from the previous day are excluded.
---

# Git Log Screenshot

(Add your screenshot here before submitting.)