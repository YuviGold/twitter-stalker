# Twitter Stalker

Just a simple script I made that fetches a user's Twitter followers list.
Combined with a crontab running on a daily basis so I can find out who unfollows me :)

Actually, you can change the `TWITTER_USER` and just stalk whoever you want ;)

## Setup

Need to define 2 environment variables

Key | Description
--|--
`TWITTER_USER` | username or handle. Begins with the “@” symbol, is unique per account, and appears in the profile URL.
`TWITTER_TOKEN` | Used for authorization. It can be fetched by launching Twitter on your browser after being logged-in and copying the `authorization` header of any request.

## How To Run

### Local

Just run the script!

```shell
./main.py
date='2023/02/15', followers=77, added_names=['Mendy Landa (LandaMendy)', 'Tal Borenstein (talboren)'], removed_names=[]
```

## Scheduled job

Run `crontab -e` to add a new cronjob

- Define the environment variables
- Define interval, check [crontab.guru](https://crontab.guru/)
- Store logs to a log file

Here's an example running the script on a daily basis:

```
TWITTER_USER=<user_to_stalk>
TWITTER_TOKEN=<auth_token>
...
0 0 * * * <path/to/repo>/twitter-stalker/main.py >> <path/to/repo>/twitter-stalker/log.txt 2>&1
```
