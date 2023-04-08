import json
import os
import subprocess

TWITTER_TOKEN = os.environ['TWITTER_TOKEN']
DEFAULT_TIMEOUT = 10
DEFAULT_COUNT = 200
TWITTER_BASEURL = "https://api.twitter.com/1.1"


def call_twitter_api(path: str, parameters: list[str]) -> dict:
    params = '&'.join(parameters)
    command = f'curl -s "{TWITTER_BASEURL}/{path}?{params}" -H "Authorization: Bearer {TWITTER_TOKEN}"'
    output = subprocess.getoutput(command)
    return json.loads(output)


def get_twitter_list(api: str,
                     username: str, count: int = DEFAULT_COUNT,
                     skip_status: bool = True, include_user_entities: bool = False) -> dict[str, dict[str, str]]:
    cursor = -1
    users: dict[str, dict[str, str]] = dict()
    while cursor != 0:
        params = [f"screen_name={username}", f"{count=}", f"{cursor=}",
                  f"{skip_status=}", f"{include_user_entities=}"]
        data = call_twitter_api(api, params)
        users |= {user['id_str']: {'screen_name': user['screen_name'], 'name': user['name']} for user in data['users']}
        cursor = data['next_cursor']

    return users


def get_twitter_friends(username: str) -> dict[str, dict[str, str]]:
    '''
    ref: https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-friends-list
    '''

    return get_twitter_list('friends/list.json', username)


def get_twitter_followers(username: str) -> dict[str, dict[str, str]]:
    '''
    ref: https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-followers-list
    '''

    return get_twitter_list('followers/list.json', username)
