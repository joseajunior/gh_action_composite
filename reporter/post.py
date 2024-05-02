import os, requests
from pathlib import Path

DEFAULT_URL = "https://api.github.com/repos/{OWNER}/{REPO}/issues/{PR_NUMBER}/comments"


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-gt', '--github-token', help='The GitHub token', required=False,
                        default=os.environ.get('GITHUB_TOKEN'), type=str)
    parser.add_argument('-f', '--file', help='The Markdown file', required=False,
                        default='report.md', type=Path)
    parser.add_argument('--pr', help='The commit SHA', required=False,
                        default=os.environ.get('PR_NUMBER', 'none'), type=str)
    parser.add_argument('-o', '--owner', help='Repository Owner', required=False,
                        default=os.environ.get('REPOSITORY_OWNER', 'none'), type=str)
    parser.add_argument('-rp', '--repository', help='Repository Name', required=False,
                        default=os.environ.get('REPOSITORY_NAME', 'none'), type=str)
    args = parser.parse_args()

    if args.pr.lower() != 'none' and args.github_token.lower() != 'none':
        url = DEFAULT_URL.format(OWNER=os.environ.get('REPOSITORY_OWNER', parser.owner),
                                 REPO=os.environ.get('REPOSITORY_NAME', parser.repository),
                                 PR_NUMBER=args.pr)
        post_comment(url, args.github_token, args.file)

def post_comment(url: str, token: str, file_path: Path):
    # skipcq: PTC-W6004
    with open(file_path, 'r') as f:
        content = f.read()

    headers = {'Authorization': f'token {token}',
               'Accept': 'application/vnd.github+json',
               'X-GitHub-Api-Version': '2022-11-28'}
    body = {'body': content}

    comments = requests.get(url, headers=headers).json()
    comment = next((comment for comment in comments if comment['user']['login'] == 'github-actions[bot]' and 'Robot Framework Report' in comment['body']), None)
    if comment:
        comment_url = comment['url']
        response = requests.patch(comment_url, headers=headers, json=body)
        response.raise_for_status()
        return

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()


if __name__ == '__main__':
    main()
