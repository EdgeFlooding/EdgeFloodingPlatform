import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = "AAAAAAAAAAAAAAAAAAAAACpyWAEAAAAAZdivw%2FpWKUtBaK0xIZVZ045Z%2B0Q%3DrIexy1px1FiNoo3HPlyDhHnEcHXdMG976MXlLgulGEDe1gPw6b"


def create_url():
    # UMBC Flood Bot id
    user_id = 1173295284874596358
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at"}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    url = create_url()
    params = get_params()
    try:
        json_response = connect_to_endpoint(url, params)
        json_response2 = connect_to_endpoint(url, params)
    except Exception:
        exit("Impossible to retrieve json")

    n_id = json_response['meta']['newest_id']
    n_id2 = json_response2['meta']['newest_id']

    print(n_id)
    print(n_id2)
    
    if n_id == n_id2:
        print("Uguali")
    

    #print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()