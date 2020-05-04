# Snake Game

This problem is part of the `Intro to Hacking Workshop`. View the [Bug Bounty Guide](https://github.com/hackmtlca/bug-bounty-guide) for more information about the score system.

## Context

The Video Game Industry is at it's prime. Pro gamers can make millions and virtual items can be worth more than physical items. Security in this field is therefore of upmost interest. In this problem, we will explore a simple `Snake Game`. Your goal is to have an account that is first place on the leaderboard. Once you do so, the key will be on the bottom of the `leaderboard` page. We currently intend this game to be hacked in the following ways: on a game level (modifying game), on a request level (sending a request to API), on an account level (gaining access to h4x0r), and XSS (leaderboard is vulnerable, just showing that it can be done is enough). We hope that these attacks will give an understanding of the importance of encryption. In addition, we hope that game developers will be concious about trusting user data.

## Running the App

All you need is `Docker`. Run the following command in the root of this repository:

```
docker-compose up
```

A frontend instance will be created at `http://localhost/`. Database can be reset by closing the app and appending `--build` to the previous command.

## Closing the App

The app can be closed using CTRL+C. The app can be completely closed with the following command in the root of this repository:

```
docker-compose down
```