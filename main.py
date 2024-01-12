import os

import requests
from bs4 import BeautifulSoup


def extract_data(url):
    response = requests.get(url, timeout=5)
    soup = BeautifulSoup(response.text, "html.parser")
    news_items = soup.find_all("div", class_="news-item")
    datas = []
    tot_articles = len(news_items)
    print("[+] Total news: " + str(tot_articles))
    print("[+] Filtering out invalid articles...")
    counter = 0
    for news_item in news_items:
        # Extract the article link and title
        article_link = news_item.find_all("a")[0].get("href")
        if "allsides.com" not in article_link:
            tot_articles -= 1
            continue
        counter += 1
        print("[+] Processing news: " + str(counter) + "/" + str(tot_articles))
        article_title = news_item.find("div", class_="news-title").text.strip()
        print("[*] Summarizing: " + article_link)
        # Summarize the article
        with open("link", "w+") as f:
            f.write(article_link)
        # trunk-ignore(bandit/B605)
        # trunk-ignore(bandit/B607)
        os.system("python summarizer.py")
        print("[OK] Done. Proceeding...")
        with open("response", "r") as f:
            article_summary = f.read().strip()
        # with open(article_title, "w+") as f:
        # f.write(article_summary)
        # Extract the source and media bias rating
        try:
            source_name = news_item.find("span").text
        except Exception:
            source_name = "Unknown"

        try:
            media_bias_rating = (
                news_item.find("img")
                .get("alt")
                .replace("AllSides Media Bias Rating: ", "")
                .lower()
            )
        except Exception:
            media_bias_rating = "Unknown"

        # Build the JSON
        data = {
            "article_link": article_link,
            "article_title": article_title,
            "article_summary": article_summary,
            "source_name": source_name,
            "media_bias_rating": media_bias_rating,
        }

        datas.append(data)

    return datas


def handle_pagination(soup):
    next_page = soup.find("a", {"rel": "next"})
    if next_page:
        return next_page["href"]
    return None


def main():
    url = "https://www.allsides.com/unbiased-balanced-news"
    all_data = []

    while url:
        data = extract_data(url)
        all_data.extend(data)
        url = handle_pagination(
            BeautifulSoup(requests.get(url, timeout=5).text, "html.parser")
        )

    # Prepare a nice CSS for the viewing page (nice and clean)
    css = """
    body {
        font-family: sans-serif (Helvetica, Arial);
    }
    h1 {
        font-size: 2em;
    }
    h2 {
        font-size: 1.5em;
    }
    h3 {
        font-size: 1.2em;
    }
    p {
        font-size: 1em;
    }
    """

    # Create a nice HTML view of all the articles each one in its own page
    html = "<html><head><title>AllSides Unbiased News</title>"
    html += "<style>" + css + "</style>"
    html += "</head><body>"
    for item in all_data:
        html += "<h1>" + item["article_title"] + "</h1>"
        html += "<h2>" + item["source_name"] + "</h2>"
        html += "<h3>" + item["media_bias_rating"] + "</h3>"
        html += "<p>" + item["article_summary"] + "</p>"
        html += "<a href='" + item["article_link"] + "'>Read the full article</a>"
        html += "<hr>"
    html += "</body></html>"
    with open("allsides.html", "w+") as f:
        f.write(html)

    print("Total articles: ", len(all_data))
    # Do some math to find the number of articles per bias rating
    bias_ratings = {}
    for item in all_data:
        if item["media_bias_rating"] in bias_ratings:
            bias_ratings[item["media_bias_rating"]] += 1
        else:
            bias_ratings[item["media_bias_rating"]] = 1
    # Assign percentages
    for key in bias_ratings:
        bias_ratings[key] = round(bias_ratings[key] / len(all_data) * 100, 2)

    print(bias_ratings)


if __name__ == "__main__":
    main()
