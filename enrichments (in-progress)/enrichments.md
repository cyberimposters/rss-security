
# Enrich the the RSS index with data from CISA's known vulnerability database

### 1) You will need to get the data from [CISA's Known Vulnerability Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

- I opted to use the `http_poller` input plugin in Logstash to collect the data from (https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json). Please reference the [known-vulnerabilites.conf](../logstash/cve/known-vulnerabilites.conf) input section

### 2) Add the [`known-vulnerabilites.conf`](../logstash/cve/known-vulnerabilites.conf) file to your Logstash `conf.d` directory

### 3) Navigate to Kibana and add the `known-vulnerabilites` [component templates](../templates/component/cve-component_templates.json) and [index templates](../templates/index/cve-index_template.json)

### 4) Create the `known-vulnerabilities` index by navigating to **Dev Tools** in Kibana and run the following command:

```
PUT known-vulnerabilities
```

### 5) Verify the mappings and index settings are correct

```
GET known-vulnerabilities
```

    
- Your output should match the [cve-mappings.json](../templates/mapping-output/cve-mappings.json) output

### 6) Create an enrichment policy

```
PUT /_enrich/policy/known_vuln_policy
{
  "match": {
    "indices": "known-vulnerabilities",
    "match_field": "vuln.id",
    "enrich_fields": [ "vuln.due_date" , "vuln.date_added" , "vuln.notes" , "vuln.required_action" , "vuln.product"]
  }
}

PUT /_enrich/policy/cvss_score_policy
{
  "match": {
    "indices": "cvss-rss-feed",
    "match_field": "vuln.id",
    "enrich_fields": [ "score1" , "score2" , "details" ]
  }
}

PUT /_enrich/policy/apt_groups_policy
{
  "match": {
    "indices": "apt-groups",
    "match_field": "apt",
    "enrich_fields": [ "apt" , "description" ]
  }
}
```

### 7) Execute the enrichment policy

```
POST /_enrich/policy/known_vuln_policy/_execute

POST /_enrich/policy/cvss_score_policy/_execute

POST /_enrich/policy/apt_groups_policy/_execute
```

### 8) Create an ingest pipeline composed of an enrich processor; you will be referencing your newly created enrichment policy.

```
PUT _ingest/pipeline/rss-feed-enrichment-pipeline
{
  "processors": [
    {
      "enrich": {
        "field": "vuln.id",
        "policy_name": "known_vuln_policy",
        "target_field": "known_data",
        "ignore_missing": true,
        "description": "Add 'vulnerability' details based on 'CISA's known vuln database'"
      }
    },
    {
      "enrich": {
        "description": "Add 'apt' description based on 'apt.id'",
        "policy_name": "apt_groups_policy",
        "field": "apt",
        "target_field": "known_data",
        "ignore_missing": true
      }
    },
    {
      "enrich": {
        "field": "vuln.id",
        "policy_name": "cvss_score_policy",
        "target_field": "score_data",
        "ignore_missing": true
      }
    }
  ]
}
```

### 9) Test your ingest pipeline

```
GET rss-feed/_search
{
  "size": 1, 
  "query": {
    "bool": {
      "must": [
        {
          "exists": {
            "field": "vuln.id"
          }
        }
      ]
    }
  }
}
```
- Copy the value in the `id` field `"_id": "ef1d6f6327c9791cde491e0fd7d0cb13a376dda81e8d416186ad0996e4d93e7f"`

- **Stack Management -> Ingest Pipeline -> rss-feed-enrichment-pipeline (Edit)**

![image](/zz-working-folder/images/Screen%20Shot%202024-02-05%20at%206.04.02%20PM.png)