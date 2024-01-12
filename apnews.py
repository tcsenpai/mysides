
def fetchAndDigest(soup):

    news_items = soup.find_all("div", class_="PagePromo")
    print("[+] Filtering out invalid articles...")
    links = []
    for news_item in news_items:
        article_title = news_item['data-gtm-region']
        # Extract the article link and title
        try:
            article_link = news_item.find_all("div", class_="PagePromo-media").pop().find("a").get("href")
        except Exception:
            try:
                article_link = news_item.find_all("h3", class_="PagePromo-title").pop().find("a").get("href")
            except Exception:
                print("[!] Invalid article. Skipping...")
                print(news_item)
            continue
        links.append([article_title, article_link])

    print("[+] Total news: " + str(len(links)))
    return links