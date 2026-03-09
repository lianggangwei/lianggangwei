import requests
from bs4 import BeautifulSoup
import time
import csv
import json
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
import os


class WebScraper:
    def __init__(self, base_url: str, delay: float = 1.0):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.visited_urls = set()

    def get_page(self, url: str) -> Optional[str]:
        try:
            time.sleep(self.delay)
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response.text
        except Exception as e:
            print(f"获取页面失败 {url}: {e}")
            return None

    def parse_links(self, html: str, base_url: str = None) -> List[str]:
        soup = BeautifulSoup(html, 'lxml')
        links = []
        base = base_url or self.base_url
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(base, href)
            if full_url not in self.visited_urls:
                links.append(full_url)
        return links

    def extract_text(self, html: str, selector: str = None) -> str:
        soup = BeautifulSoup(html, 'lxml')
        if selector:
            elements = soup.select(selector)
            return '\n'.join([elem.get_text(strip=True) for elem in elements])
        return soup.get_text(strip=True)

    def extract_tables(self, html: str) -> List[List[List[str]]]:
        soup = BeautifulSoup(html, 'lxml')
        tables = []
        for table in soup.find_all('table'):
            rows = []
            for tr in table.find_all('tr'):
                cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                if cells:
                    rows.append(cells)
            if rows:
                tables.append(rows)
        return tables

    def scrape_single_page(self, url: str) -> Dict[str, Any]:
        html = self.get_page(url)
        if not html:
            return {}
        soup = BeautifulSoup(html, 'lxml')
        title = soup.title.string if soup.title else ''
        meta_desc = ''
        meta_tag = soup.find('meta', {'name': 'description'})
        if meta_tag:
            meta_desc = meta_tag.get('content', '')
        return {
            'url': url,
            'title': title,
            'description': meta_desc,
            'html': html,
            'text': self.extract_text(html),
            'tables': self.extract_tables(html),
            'links': self.parse_links(html, url)
        }

    def save_to_csv(self, data: List[Dict], filename: str):
        if not data:
            return
        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

    def save_to_json(self, data: List[Dict], filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


class GithubRepoScraper(WebScraper):
    def __init__(self, owner: str, repo: str):
        super().__init__(f"https://github.com/{owner}/{repo}")
        self.owner = owner
        self.repo = repo

    def get_repo_info(self) -> Dict[str, Any]:
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"获取仓库信息失败: {e}")
            return {}
