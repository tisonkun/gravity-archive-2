#!/usr/bin/env python3

# Copyright 2022 tison <wander4096@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import dotenv
import pandas as pd
import requests


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
    contributors = []
    while True:
        result = requests.get(url=f'https://api.github.com/repos/{args.repo}/contributors?per_page=100&page={page}', headers=headers)
        links = result.links
        contributors += result.json()
        if 'next' not in links:
            break
        page = links['next']['url']

    contributors = contributors_to_pandas(contributors)
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(contributors)
