# Fistfight!

## Background
This is a flask app. My initial inspiration was 'the "lowest-level" online multiplayer game that would work'. In this case, "low-level" meant basic js, and Flask. Over time, I  ended up using a few Flask plugins in the back as well as bootstrap and socket.io for the front.

### [Demo](https://https://fistfight.onrender.com)
(Allow time for Dynos to rev up...)

## Running the App Locally
For dev purposes:

`python arena_dev.py`

Keep in mind you will need to set REDIS_URL and DATABASE_URL in your environment. This will require you to have a postgres and redis server instance.
