#!/usr/bin/env python3

import argparse
import os
import dotenv
import pandas as pd
import requests

"""
GitHub's contributor graph shows only the first 100 contributors.
"""

def contributors_to_pandas(contributors):
    result = [{
        'login': contributor['login'],
        'contributions': contributor['contributions'],
    } for contributor in contributors]
    result = pd.DataFrame(result)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', help="source repository", default='pingcap/tidb')
    args = parser.parse_args()

    dotenv.load_dotenv()

    headers = {}
    headers['Accept'] = 'application/vnd.github.v3+json'
    headers['Authorization'] = os.getenv('GITHUB_TOKEN')

    page = 1
    repo = args.repo
    contributors = []
    while True:
        result = requests.get(url=f'https://api.github.com/repos/{repo}/contributors?per_page=100&page={page}', headers=headers)
        links = result.links
        contributors += result.json()
        if 'next' not in links:
            break
        page = links['next']['url']

    contributors = contributors_to_pandas(contributors)
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(contributors)
