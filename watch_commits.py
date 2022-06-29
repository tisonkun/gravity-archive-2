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

from collections import namedtuple
import os

import dotenv
import requests


if __name__ == "__main__":
    dotenv.load_dotenv()

    headers = {}
    headers['Accept'] = 'application/vnd.github.v3+json'
    headers['Authorization'] = os.getenv('GITHUB_TOKEN')

    Watcher = namedtuple('Watcher', ['repo', 'commit'])
    watchers = [
        Watcher(repo='stretchr/testify', commit='cf1284f8dd6f0bf34eed4ab8808ef88f40f7d00f')
    ]

    exit_code = 0
    for watcher in watchers:
        result = requests.get(url=f'https://api.github.com/repos/{watcher.repo}/commits?per_page=1', headers=headers)
        commit = result.json()[0]['sha']

        if commit != watcher.commit:
            print(f'{watcher.repo} has been pushed new commit: {commit}, last commit: {watcher.commit}')
            exit_code = 1

    exit(exit_code)
