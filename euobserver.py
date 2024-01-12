import feedparser

def fetchAndDigest():
    links = []
    feed = feedparser.parse("https://xml.euobserver.com/rss.xml")
    for entry in feed.entries:

        article_title = entry.title
        article_link = entry.link
        links.append([article_title, article_link])

    print("[+] Total news: " + str(len(links)))
    return links