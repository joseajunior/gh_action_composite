import os, requests
from pathlib import Path

DEFAULT_URL = "https://api.github.com/repos/{OWNER}/{REPO}/commits/{COMMIT_SHA}/comments"

def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-gt', '--github-token', help='The GitHub token', required=False, default=os.environ.get('GITHUB_TOKEN'), type=str)
    parser.add_argument('-f', '--file', help='The Markdown file', required=False, default='report.md', type=Path)
    parser.add_argument('--sha', help='The commit SHA', required=False, default=os.environ['SHA'], type=str)
    parser.add_argument('--webhook-url', help='The webhook URL', required=False, default=os.environ['WEBHOOK_URL'], type=str)
    args = parser.parse_args()

    try:
        if args.sha.lower() == 'none':
            url = DEFAULT_URL.format(OWNER=os.environ['REPOSITORY_OWNER'], REPO=os.environ['REPOSITORY_NAME'], COMMIT_SHA=args.sha)
            post_comment(url, args.github_token, args.file)
    except:
        pass

    try:
        if args.webhook_url.lower() == 'none':
            post_webhook(args.webhook_url, args.file)
    except:
        pass

def post_comment(url: str, token: str, file: Path):
    with open(file, 'r') as f:
        content = f.read()

    headers = {'Authorization': f'token {token}',
               'Accept': 'application/vnd.github+json',
               'X-GitHub-Api-Version': '2022-11-28'}
    payload = {'body': content}

    response = requests.post(url, headers=headers, json=payload)
    print(response.status_code)
    print(response.text)
    response.raise_for_status()

    
def post_webhook(url: str, file: Path):
    NOTIFICATION_HEADER = {
        "title": "Byte Beard, the Unbearded",
        "subtitle": "Captain of the Blind Dutchmen",
        "imageType": "SQUARE",
        "imageUrl": "https://lh6.googleusercontent.com/proxy/LuXT5faWBJGTYOs6ht5knPYYkE690VGuzcSMextFYLvUSBFHeuQDwPPklio0LnoNWIWrwjpnMrX6SmebKRMjgwcOJhLukzjIyryZzYaVaYfnMAaTWr_0yqnOA5hNwFKY6sxyodeO8OaOhn_Ns0nRtmPOjjYsXEvsb_8Ju3MIO79P0VhAZiexknJUxrs1XOdI9mn6uHyq0w9KDJv5nrJX2lNR2PWqBbRasZvId6SwpucY8kJMhe_3lA"
    }

    MESSAGE_HEADERS = {'Content-Type': 'application/json; charset=UTF-8'}

    with open(file, 'r') as f:
        content = f.read()

    data_raw = {
        "cardsV2": [
            {
                "cardId": "release",
                "card": {
                    "header": NOTIFICATION_HEADER,
                    "sections": [
                        {
                            "header": f"<b>Robot Framework Report</b>",
                            "widgets": [
                                {
                                    "textParagraph": {
                                        "text": f"""{content}"""
                                    }
                                },
                            ]
                        }
                    ]
                }
            }
        ]
    }

    response = requests.post(url, headers=MESSAGE_HEADERS, json=data_raw)
    print(response.status_code)
    print(response.text)
    response.raise_for_status()

if __name__ == '__main__':
    main()