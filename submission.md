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

(To be completed.)

### The root cause

(To be completed.)

### My fix and side-effect check

(To be completed.)

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