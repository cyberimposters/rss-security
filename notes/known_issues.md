## **Known Issues**

1. The Logstash `fingerprint` filter is using the `message` field to create hashes. If any of the text in the `message` changes, then it creates a new hash despite the article being the same. Currently testing the `fingerprint` filter on the `title` field to see if it improves.

2. **Talos** links will not take you to the article; the links prompt for an RSS reader. 

3. **ILM** index rollover results in new doc _id leading to duplicates.