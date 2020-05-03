# Flask SQLite Docker

Template for a Flask and SQLite stack. **This is made for competition purposes only.** We acknowledge that there are security flaws in our method, we don't take responsibility if this is taken in production.

## Running the App

All you need is `Docker`. Run the following command in the root of this repository:

```
docker-compose up
```

A frontend instance will be created at `http://localhost/`.

## Closing the App

The app can be closed using CTRL+C. The app can be completely closed with the following command in the root of this repository:

```
docker-compose down
```

## API

We made a simple system that lets you expand the API as you wish.

### Users

We implemented a simple user system to get basic authentication:

```
(session) -> /api/users/me -> (user_id, username): Gets the info for the current user.
(username, password) -> /api/users/register -> (user_id, username, password): Registers the user in a temporary database.
(username, password) -> /api/users/login -> (session): Sign in user and returns an HTTP-Only cookie with session.
/api/users/logout: Revokes session cookie from user.
```

### Tools

We implemented functions that could be useful for competitors.

```
/api/tools/reset: Replaces the database under tmp with the one in data. Revoke user token aswell.
```

## Static Content

All static content can be placed under the public folder. This folder will be exposed under `http://hostname/static/...`.