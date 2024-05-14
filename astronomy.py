import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


class ExternalLinkCrawler:
    def __init__(self, seed_urls, max_pages):
        self.seed_urls = seed_urls
        self.max_pages = max_pages
        self.visited_urls = set()
        self.external_links = set()

    def crawl(self):
        for url in self.seed_urls:
            self._crawl_url(url)
        return self.external_links

    def _crawl_url(self, url):
        if len(self.visited_urls) >= self.max_pages:
            return

        if url in self.visited_urls:
            return

        try:
            response = requests.get(url)
            if response.status_code != 200:
                return

            soup = BeautifulSoup(response.content, "html.parser")
            self.visited_urls.add(url)

            parsed_url = urlparse(url)
            domain = parsed_url.netloc

            for link in soup.find_all("a", href=True):
                next_url = urljoin(url, link["href"])
                next_parsed_url = urlparse(next_url)
                if next_parsed_url.netloc != domain:
                    self.external_links.add(next_url)

            for link in soup.find_all("a", href=True):
                next_url = urljoin(url, link["href"])
                if next_url not in self.visited_urls:
                    self._crawl_url(next_url)

        except Exception as e:
            print(f"Error crawling {url}: {e}")


# Seed URLs
seed_urls = ["https://en.wikipedia.org/wiki/Astronomy"]

crawler = ExternalLinkCrawler(seed_urls, max_pages=10)
external_links = crawler.crawl()
url_astro = []
print("External links found:")
for link in external_links:
    url_astro.append(link)


print(url_astro)
