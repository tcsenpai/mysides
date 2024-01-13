import os
from dotenv import load_dotenv

# Our modules
import apnews
import rss
import summarizer

load_dotenv()

# Loading environment variables
pplx_api_key = os.getenv("PPLX_API_KEY")
model = os.getenv("MODEL")

# Fetch and summarize the article
def transform_links(links):
    datas = []
    counter = 0
    print("[+] Extracting data from articles...")
    for link in links:
        counter += 1
        print("[+] Article " + str(counter) + " of " + str(len(links)))
        article_title = link[0]
        article_link = link[1]
        print("[ " + article_title + " ]")
        print("[+] Extracting data from: " + article_link)
        try:
            article_summary = summarizer.summarize(article_link, pplx_api_key, model)
        except Exception as e:
            print(e)
            print("[!] Invalid article. Skipping...")
            continue
        datas.append(
            {
                "article_title": article_title,
                "article_link": article_link,
                "article_summary": article_summary,
            })
    return datas

# Downloads the site and extracting the data using the appropriate module
def extract_data():
    links = []

    # Add your rss link to the .env file
    rss_links = os.getenv("ENABLED_RSS").split(",")
    links.extend(rss.fetchAndDigest(rss_links))

    # Plug in your module here (links.extend(your_module.fetchAndDigest())
    # TODO Programmatically scan and import modules
    links.extend(apnews.fetchAndDigest())

    print("[+] Total news: " + str(len(links)))
    datas = transform_links(links)
    return datas

def handle_pagination(soup):
    next_page = soup.find("a", {"rel": "next"})
    if next_page:
        return next_page["href"]
    return None


def main():
    all_data = []

    datas = extract_data()
    all_data.extend(datas)

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
    html = "<html><head><title>Unbiased News</title>"
    html += "<style>" + css + "</style>"
    html += "</head><body>"
    for item in all_data:
        html += "<h1>" + item["article_title"] + "</h1>"
        html += "<p>" + item["article_summary"] + "</p>"
        html += "<a href='" + item["article_link"] + "'>Read the full article</a>"
        html += "<hr>"
    html += "</body></html>"
    with open("ap.html", "w+") as f:
        f.write(html)

    # Archiving (skip if causes errors)
    os.system("./archiver.sh")

    print("Total articles: ", len(all_data))


if __name__ == "__main__":
    main()
