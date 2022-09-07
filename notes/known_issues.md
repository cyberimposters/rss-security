## **Known Issues**

1. The Logstash `fingerprint` filter is using the `message` field to create hashes. If any of the text in the `message` changes, then it creates a new hash despite the article being the same. Currently testing the `fingerprint` filter on the `title` field to see if it improves.