import feedparser

def fetchAndDigest(rss_feeds):
    links = []
    for rss_url in rss_feeds:
        rss_url = rss_url.replace("'", "")
        print("[+] Fetching RSS feed: " + rss_url)
        links.extend(fetchAndDigest_subroutine(rss_url))
    return links

def fetchAndDigest_subroutine(rss_url):
    links = []
    feed = feedparser.parse(rss_url)
    for entry in feed.entries:

        article_title = entry.title
        article_link = entry.link
        links.append([article_title, article_link])

    print("[+] Total news: " + str(len(links)))
    return links