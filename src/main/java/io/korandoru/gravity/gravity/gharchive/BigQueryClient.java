/*
 * Copyright 2022 Korandoru Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package io.korandoru.gravity.gravity.gharchive;

import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.FieldValueList;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.QueryParameterValue;
import java.util.HashSet;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class BigQueryClient {

    private final BigQuery bigQuery;

    @Autowired
    public BigQueryClient() {
        this.bigQuery = BigQueryOptions.getDefaultInstance().getService();
    }

    public List<String> contributors(String repository) {
        final var template = """
            SELECT
                DISTINCT actor.login
            FROM
                `githubarchive.month.*`
            WHERE
                repo.name = @repository
                AND type = 'PullRequestEvent'
                AND (_TABLE_SUFFIX BETWEEN '202101' AND '202203')
            """;
        final var contributors = new HashSet<String>();
        final var queryConfig = QueryJobConfiguration.newBuilder(template)
            .addNamedParameter("repository", QueryParameterValue.string(repository))
            .build();
        try {
            final var results = this.bigQuery.query(queryConfig);
            for (FieldValueList row : results.iterateAll()) {
                contributors.add(row.get("login").getStringValue());
            }
        } catch (Exception e) {
            log.error("BigQuery fails to list all contributors.", e);
        }
        return contributors.stream().toList();
    }
}
