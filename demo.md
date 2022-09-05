## A Quick RSS Cybersecurity News Feed
---

### **Software**
- Elasticsearch (v.8.4.1)
- Logstash 
- Kibana

### **RSS Feeds**
- Dark Reading
- Zero Day Initative
- Bleeping Computer
- The Hacker News
- The Register
- Krebs on Security
- US-CERT
- Cisco Talos
- KnowBe4
- Threatpost
- Malwarebytes

### **Quick Instructions**
- Add **[Index Templates](./templates/rss-index_template.json)** and **[Component Templates](./templates/rss-component_template.json)** to your Elastic Stack 
- Create the Logstash **[rss-security-feed.conf](./logstash/rss-security-feed.conf)** file and then start Logstash
    - Modify the **[pipelines.yml](./logstash/pipelines.yml)** file (optional). You can also run Logstash via the command line. Reference [documentation](https://www.elastic.co/guide/en/logstash/current/getting-started-with-logstash.html) for additional details.
- Validate data is incoming and mapping is correct
    - Check data in **Discover**
    - Run `GET indexname/_mappings` in **Dev Tools**. Your mapping should match the contents in the **[rss-feed-mappings.json](./templates/rss-feed-mappings.json)** file.
- Import Kibana **Saved Objects**
    - Import the **[saved_objects.ndjson](./kibana/saved_objects.ndjson)** file to import the **Saved Objects** displayed in the image below

![image](./kibana/rss-feed-dashboard.png)

### **Quick Notes**
- Fingerprint filter in Logstash is used to avoid document duplication
- Have fun!

