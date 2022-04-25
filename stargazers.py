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

"""
This scripts shows what repositories those who star your repository also star.

For example, to find repositories that stargazers of pingcap/tidb, pingcap/tikv and tikv/tikv star,
run:

    python3 stargazers.py --repo pingcap/tidb --repo pingcap/tikv tikv/tikv

... and you will get:

                                        repo_name  stars
    0                                   golang/go  14237
    1                       ant-design/ant-design  13393
    2                          avelino/awesome-go  12190
    3                       tensorflow/tensorflow  12091
    4                       kubernetes/kubernetes  11746
    5                               gin-gonic/gin  11391
    6            donnemartin/system-design-primer  11088
    7                              996icu/996.ICU  10583
    8                       prometheus/prometheus  10154
    9                        sindresorhus/awesome   9851
    ... (more 40 lines omitted)
"""

import argparse
import clickhouse_driver
import pandas as pd

from clickhouse_driver.util.escape import escape_param

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', help="source repository", action='append', nargs='+')
    args = parser.parse_args()

    client = clickhouse_driver.Client(
        host = 'play.clickhouse.com',
        user = 'explorer',
        secure = True,
        settings = {
            'use_numpy': True,
        }
    )
    existence = [escape_param(repo, client.connection.context)for repos in args.repo for repo in repos]
    existence = ', '.join(existence)

    result = client.query_dataframe(f"""
    SELECT
        repo_name,
        count() AS stars
    FROM github_events
    WHERE (event_type = 'WatchEvent') AND (actor_login IN
    (
        SELECT actor_login
        FROM github_events
        WHERE (event_type = 'WatchEvent') AND (repo_name IN ({existence}))
    )) AND (repo_name NOT IN ({existence}))
    GROUP BY repo_name
    ORDER BY stars DESC
    LIMIT 50
    """)

    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(result)
