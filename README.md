# Twitter Followers follower

Just a simple cronjob script I made that fetches my Twitter followers list on a daily basis so I can find out who unfollows me :)

## Setup

Need to define 2 environment variables
- `TWITTER_USER`
- `TWITTER_TOKEN`

## How To Run

Just run `crontab -e` to add a new cronjob

for example to run it daily you should add
```
0 0 * * * <path/to/repo>/twitter-followers-follower/main.py >> <path/to/repo>/twitter-followers-follower/log.txt 2>&1
```
