import base64
import ipaddress
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import xml.etree.ElementTree as ET
import whois
from datetime import datetime
from dateutil.parser import parse as date_parse
import googlesearch
import tldextract
import favicon

# Generate data set by extracting the features from the URL


def generate_data_set(url):
    data_set = []

    # Converts the given URL into standard format
    if not re.match(r"^https?", url):
        url = "http://" + url

    global soup

    # Stores the response of the given URL
    try:
        response = requests.get(url)  # status code
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        response = ""
        soup = -999

    # Extracts domain from the given URL
    domain = urlparse(url).netloc
    if re.match(r"^www.", domain):
        domain = domain.replace("www.", "")

    # whois_response = whois.whois(domain)

    rank_checker_response = requests.post(
        "https://www.checkpagerank.net/index.php", {"name": domain})

    # Extracts global rank of the website
    try:
        pRank = str(re.findall(
            r"Google PageRank: <span style=\"color:#000099;\">[0-9]*/10", rank_checker_response.text)[0])
        blinks = re.findall(
            r"External Backlinks: ([0-9]+(,[0-9]+)+)", rank_checker_response.text)[0]
        bl = str(blinks[0])
        backlinks = bl.replace(",", "")
        globalRank = re.findall(
            r"Global Rank: ([0-9]+(,[0-9]*)*)", rank_checker_response.text)[0]
        print(globalRank[0])
        gloR = str(globalRank[0])
        GlobalRank = gloR.replace(",", "")
        print(GlobalRank)
        last_chars = pRank[-5:]

        if last_chars[0] == "1":
            pageRank = 1
        if last_chars[0] == ">":
            n = int(last_chars[1])

            pageRank = n / 10
    except:
        pageRank = -1
        backlinks = 0

    # 1.having_IP_Address
    try:
        ipaddress.ip_address(domain)
        data_set.append(-1)
    except:
        data_set.append(1)

    # 2.URL_Length
    if len(url) < 54:
        data_set.append(1)
    elif len(url) >= 54 and len(url) <= 75:
        data_set.append(0)
    else:
        data_set.append(-1)

    # 3.Shortining_Service
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net',
                      url)
    if match:
        data_set.append(-1)
    else:
        data_set.append(1)

    # 4.having_At_Symbol
    if re.findall("@", url):
        data_set.append(-1)
    else:
        data_set.append(1)

    # 5.double_slash_redirecting
    pos = url.rfind('//')
    if pos > 7:
        data_set.append(-1)
    else:
        data_set.append(1)

    # 6.Prefix_Suffix
    if re.findall(r"https?://[^\-]+-[^\-]+/", domain):
        data_set.append(-1)
    else:
        data_set.append(1)

    # 7.having_Sub_Domain
    ext = tldextract.extract(url)

    if len(re.findall("\.", ext.subdomain)) == 0:
        data_set.append(1)
    elif len(re.findall("\.", ext.subdomain)) == 1:
        data_set.append(0)
    else:
        data_set.append(-1)

    # 8.SSLfinal_State
    try:
        if response.text:
            data_set.append(1)
    except:
        data_set.append(-1)

    # 9.Domain_registeration_length
    try:
        whois_info = whois.whois(domain)
        exp = whois_info.expiration_date

        try:
            today = datetime.now()

            length = exp - today

            if length.days > 365:
                data_set.append(1)
            else:
                data_set.append(-1)
        except:
            data_set.append(-1)
    except Exception:
        data_set.append(-1)

    # 10.Favicon
    def check_favicon(url):
        try:
            extract_res = tldextract.extract(url)
            url_ref = extract_res.domain

            favs = favicon.get(url)

            match = 0
            for favi in favs:
                url2 = favi.url
                extract_res = tldextract.extract(url2)
                url_ref2 = extract_res.domain

                if url_ref in url_ref2:
                    match += 1

            if match >= len(favs) / 2:
                return 1
            return -1
        except:
            return -1

    data_set.append(check_favicon(url))

    # 11. port

    # url1=url
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # lenn = len(url)-1

    # score9 = 0

    # if (url1[lenn] != '/'):
    #     url1 = url1+'/'

    # if 'https://' in url1:
    #     url1 = url1.replace('https://','')

    # elif 'http://' in url1:
    #     url1 = url1.replace('http://','')

    # for i in range(lenn):
    #     if url1[i] == '/':
    #         j = i
    # url1 = url1[:j:]
    # result = 0
    # result1 = sock.connect_ex((url1,21))
    # result2 = sock.connect_ex((url1,22))
    # result3 = sock.connect_ex((url1,23))
    # result4 = sock.connect_ex((url1,80))
    # result5 = sock.connect_ex((url1,443))
    # result6 = sock.connect_ex((url1,445))
    # result7 = sock.connect_ex((url1,1433))
    # result8 = sock.connect_ex((url1,1521))
    # result9 = sock.connect_ex((url1,3306))
    # result10 = sock.connect_ex((url1,3389))

    # if result1 == 0:
    #     result+=1
    # if result2 == 0:
    #     result+=1
    # if result3 == 0:
    #     result+=1
    # if result4 == 0:
    #     result+=1
    # if result5 == 0:
    #     result+=1
    # if result6 == 0:
    #     result+=1
    # if result7 == 0:
    #     result+=1
    # if result8 == 0:
    #     result+=1
    # if result9 == 0:
    #     result+=1
    # if result10 == 0:
    #     result+=1

    # if result>2:
    #     score9 = -11
    # else:
    #     score9 = 11

    data_set.append(1)

    # 12. HTTPS_token
    if 'http' in domain or 'https' in domain:

        data_set.append(-1)
    else:
        data_set.append(1)

    # 13. Request_URL
    if response == "":
        data_set.append(-1)
    else:
        percimg = f121_findsrcdomain('img', domain)
        percvid = f121_findsrcdomain('video', domain)
        percsound = f121_findsrcdomain('embed', domain)

        perc = percimg + percvid + percsound

        if perc >= 21:
            if perc >= 61:
                data_set.append(-1)
            else:
                data_set.append(0)
        else:
            data_set.append(1)

    # 14. URL_of_Anchor
    href = []
    count = 0
    invalidhref = 0
    if response == "":
        data_set.append(-1)
    else:
        for a in soup.find_all('a'):
            href.append(a.get('href'))
        nullweb = ['#', '#content', '#skip', 'JavaScript ::void(0)']

        for h in href:
            if h in nullweb:
                invalidhref += 1
            else:
                dom = urlparse(h).netloc
                if (dom != domain and dom != '' and dom != b''):
                    invalidhref += 1
        count = len(href)
        percc = checkperc(invalidhref, count)
        print(percc)

        if percc >= 31:
            if percc > 67:
                data_set.append(-1)
            else:
                data_set.append(0)
        else:
            data_set.append(1)

    # 15. Links_in_tags
    if response == "":
        data_set.append(-1)
    else:
        othlink, cntlink = f141_find_domain('link', domain)
        othscript, cntscript = f141_find_domain('script', domain)
        othmeta, cntmeta = f141_find_domain('meta', domain)
        perclink = checkperc(othlink, cntlink)
        percscript = checkperc(othscript, cntscript)
        percmeta = checkperc(othmeta, cntmeta)

        perccc = perclink + percmeta + percscript

        if perccc >= 17:
            if perccc > 81:
                data_set.append(-1)
            else:
                data_set.append(0)
        else:
            data_set.append(1)

    # 16. SFH
    if response == "":
        data_set.append(-1)
    else:
        if soup.find_all('form', action=True):
            for form in soup.find_all('form', action=True):

                if form['action'] == "" or form['action'] == "about:blank":
                    data_set.append(-1)

                    break
                elif url not in form['action'] or domain not in form['action']:

                    data_set.append(0)
                    break
                else:
                    data_set.append(1)
                    break
        else:
            data_set.append(1)

    # 17. Submitting_to_email
    if response == "":
        data_set.append(-1)
    else:
        if re.findall(r".*mail\(\)|mailto:?.*", response.text):

            data_set.append(-1)
        else:
            data_set.append(1)

    # 18. Abnormal_URL
    if response == "":
        data_set.append(-1)
    else:  # change
        if response.text == "":
            data_set.append(1)
        else:
            data_set.append(-1)

    # 19. Redirect
    if response == "":
        data_set.append(-1)
    else:
        if len(response.history) <= 1:
            data_set.append(1)
        elif len(response.history) <= 4:
            data_set.append(0)
        else:
            data_set.append(-1)

    # 20. on_mouseover
    if response == "":
        data_set.append(-1)
    else:
        if re.findall(".+onMouseOver=\"window.status=.*\"", response.text):
            data_set.append(-1)
        else:
            data_set.append(1)

    # 21. RightClick
    if response == "":
        data_set.append(-1)
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            data_set.append(-1)
        else:
            data_set.append(1)

    # 22. popUpWidnow
    if response == "":
        data_set.append(-1)
    else:
        if soup.find("script"):
            script = soup.find("script").extract()

            if re.findall(r'(?<=prompt\(\").+(?=\")', script.text):
                data_set.append(-1)
            else:
                data_set.append(1)
        else:
            data_set.append(1)

    # 23. Iframe
    if response == "":
        data_set.append(-1)
    else:
        if re.findall(r"<iframe ([a-zA-Z]+=.*)+ frameborder.*>", response.text):

            data_set.append(-1)
        else:
            data_set.append(1)

    # 24. age_of_domain

    try:
        w = whois.whois(domain)
    except Exception:
        data_set.append(-1)
    else:
        try:
            whois_info = whois.whois(domain)
            cre_date = whois_info.creation_date

            exp_date = whois_info.expiration_date

            age = exp_date-cre_date

            if age.days >= 180:
                data_set.append(1)
            else:
                data_set.append(-1)
        except:
            data_set.append(-1)
    # 25. DNSRecord

    extract_res = tldextract.extract(url)
    url_ref = extract_res.domain + "." + extract_res.suffix
    try:
        whois_res = whois.whois(url)
        data_set.append(1)
    except:
        data_set.append(-1)

    # 26. web_traffic
    try:
        # extract_res = tldextract.extract(url)
        # url_ref = extract_res.domain + "." + extract_res.suffix
        # html_content = requests.get(
        #     "https://www.alexa.com/siteinfo/" + url_ref).text
        # soupp = BeautifulSoup(html_content, "lxml")
        # value = str(soupp.find(
        #     'div', {'class': "rankmini-rank"}))[42:].split("\n")[0].replace(",", "")
        # value = int(value)

        # if not value.isdigit():
        #     data_set.append(-1)

        if int(GlobalRank) < 100000:
            data_set.append(1)
        else:
            data_set.append(0)
    except:
        data_set.append(-1)

    # 27. Page_Rank
    try:
        if pageRank < 0.3:
            data_set.append(-1)
        else:
            data_set.append(1)
    except:
        data_set.append(-1)

    # 28. Google_Index
    site = googlesearch.search(url, 5)
    if site:
        data_set.append(1)
    else:
        data_set.append(-1)

    # 29. Links_pointing_to_page
    if response == "":
        data_set.append(-1)
    else:
        if int(backlinks) == 0:
            data_set.append(-1)
        elif int(backlinks) <= 2:
            data_set.append(0)
        else:
            data_set.append(1)

    # 30. Statistical_report
    def check_statistical_report(url):

        headers = {
            'format': 'json',

        }

        def get_url_with_ip(URI):
            """Returns url with added URI for request"""
            url = "http://checkurl.phishtank.com/checkurl/"
            new_check_bytes = URI.encode()
            base64_bytes = base64.b64encode(new_check_bytes)
            base64_new_check = base64_bytes.decode('ascii')
            url += base64_new_check
            return url

        def send_the_request_to_phish_tank(url, headers):
            """This function sends a request."""
            response = requests.request("POST", url=url, headers=headers)
            return response

        url = get_url_with_ip(url)
        r = send_the_request_to_phish_tank(url, headers)

        def parseXML(xmlfile):

            root = ET.fromstring(xmlfile)
            verified = False
            for item in root.iter('verified'):
                if item.text == "true":
                    verified = True
                    break

            phishing = False
            if verified:
                for item in root.iter('valid'):
                    if item.text == "true":
                        phishing = True
                        break

            return phishing

        try:
            inphTank = parseXML(r.text)

            if inphTank:
                return -1
            return 1
        except:
            return 1

    data_set.append(check_statistical_report(url))
    return data_set


def checkperc(oth, cnt):
    perc = 0
    if(cnt != 0):
        perc = (oth*100)/cnt
    return perc


def f141_find_domain(tag, domain):
    href = []
    link_other_domain = 0
    count = 0

    for t in soup.find_all(tag):
        href.append(t.get('href'))

    for h in href:
        dom = urlparse(h).netloc
        if (dom != domain and dom != '' and dom != b''):
            link_other_domain += 1
        count += 1

    return (link_other_domain, count)


def f121_findsrcdomain(tag, domain):

    srcs = []
    invalidhref = 0
    count = 0

    for t in soup.find_all(tag):
        srcs.append(t.get('src'))

    for src in srcs:
        dom = urlparse(src).netloc
        if (dom != domain and dom != '' and dom != b''):
            invalidhref += 1
    count = len(srcs)
    perc = checkperc(invalidhref, count)
    return (perc)
