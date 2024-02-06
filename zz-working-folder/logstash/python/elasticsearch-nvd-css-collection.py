#!/usr/bin/python3
import bs4
import requests

def nvd_check():
    # CVE list output provided by elasticsearch-cve-collection.py
    file = open('/etc/logstash/cvss/cve-list.txt')
    # this is a results output file
    output = open('/etc/logstash/cvss/cve-list-output.txt', 'a')
    lines = file.readline()

    for lines in file:
      try:
        html = "https://nvd.nist.gov/vuln/detail/"
        webpage = requests.get(html + lines.strip())
        soup = bs4.BeautifulSoup(webpage.text, "html.parser")
        # this is the CVE base score
        content_box = soup.find(id="Cvss3CnaCalculatorAnchor") or soup.find(id="Cvss3NistCalculatorAnchor")
        # this is the vulnerability description
        details_box = soup.find(attrs={'data-testid':'vuln-description'}) or soup.find(attrs={'data-testid':'service-unavailable-msg'})

        while content_box:
          content = content_box.text
          details_box = soup.find(attrs={'data-testid':'vuln-description'})
          details = details_box.text
          print(lines.strip("\n") + " " + content + " " + "Details: " + details, file = output)
          break

        else: #ratings attribute is empty
          html = "https://nvd.nist.gov/vuln/detail/"
          webpage = requests.get(html + lines.strip())
          soup = bs4.BeautifulSoup(webpage.text, "html.parser")
          details_box = soup.find(attrs={'data-testid':'vuln-description'}) or soup.find(attrs={'data-testid':'service-unavailable-msg'})
          details = details_box.text
          print(lines.strip("\n") + " " + "Not Yet Rated " + "Details: " + details, file = output)
      except AttributeError:
        pass
    # Closes the output file
    output.close()

nvd_check()