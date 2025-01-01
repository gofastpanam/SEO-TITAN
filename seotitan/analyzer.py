"""
Module principal d'analyse SEO
"""

import requests
from bs4 import BeautifulSoup
import time
from collections import Counter
from urllib.parse import urljoin, urlparse
import re
import ssl
import socket
import json
from urllib.robotparser import RobotFileParser
from xml.etree import ElementTree as ET

class SEOAnalyzer:
    def __init__(self, url):
        self.url = url
        self.start_time = time.time()
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            self.response = self.session.get(url, timeout=10, allow_redirects=True)
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            self.load_time = time.time() - self.start_time
        except Exception as e:
            raise Exception(f"Erreur lors de l'accès à l'URL: {str(e)}")

    def get_title(self):
        title = self.soup.find('title')
        return title.text.strip() if title else "Pas de titre trouvé"

    def get_meta_description(self):
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        return meta_desc.get('content', '').strip() if meta_desc else "Pas de description META trouvée"

    def get_meta_keywords(self):
        meta_keywords = self.soup.find('meta', attrs={'name': 'keywords'})
        return meta_keywords.get('content', '').strip() if meta_keywords else "Pas de mots-clés META trouvés"

    def get_headings_count(self):
        headings = {}
        for i in range(1, 4):
            tags = self.soup.find_all(f'h{i}')
            headings[f'h{i}'] = {
                'count': len(tags),
                'text': [tag.text.strip() for tag in tags]
            }
        return headings

    def get_links(self):
        base_domain = urlparse(self.url).netloc
        internal_links = []
        external_links = []
        broken_links = []

        for link in self.soup.find_all('a', href=True):
            href = link.get('href')
            full_url = urljoin(self.url, href)
            
            try:
                if urlparse(full_url).netloc == base_domain:
                    internal_links.append(full_url)
                else:
                    external_links.append(full_url)
            except:
                broken_links.append(full_url)

        return {
            'internal': internal_links,
            'external': external_links,
            'broken': broken_links
        }

    def get_images(self):
        images = []
        for img in self.soup.find_all('img'):
            images.append({
                'src': img.get('src', ''),
                'alt': img.get('alt', 'Pas de texte alternatif')
            })
        return images

    def get_content_length(self):
        text = self.soup.get_text()
        words = re.findall(r'\w+', text)
        return len(words)

    def get_keyword_density(self):
        text = self.soup.get_text().lower()
        words = re.findall(r'\w+', text)
        total_words = len(words)
        word_freq = Counter(words)
        
        density = {word: (count/total_words)*100 
                  for word, count in word_freq.items() 
                  if len(word) > 3 and count > 2}
        
        return dict(sorted(density.items(), key=lambda x: x[1], reverse=True)[:20])

    def get_canonical(self):
        canonical = self.soup.find('link', attrs={'rel': 'canonical'})
        return canonical.get('href') if canonical else "Pas de balise canonical trouvée"

    def get_robots_meta(self):
        robots = self.soup.find('meta', attrs={'name': 'robots'})
        return robots.get('content') if robots else "Pas de meta robots trouvée"

    def get_favicon(self):
        favicon = self.soup.find('link', attrs={'rel': ['icon', 'shortcut icon']})
        return favicon.get('href') if favicon else "Pas de favicon trouvé"

    def check_ssl(self):
        parsed_url = urlparse(self.url)
        hostname = parsed_url.netloc
        context = ssl.create_default_context()
        try:
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        'secure': True,
                        'expiry': cert['notAfter'],
                        'issuer': dict(x[0] for x in cert['issuer'])
                    }
        except:
            return {'secure': False}

    def check_mobile_optimization(self):
        viewport = self.soup.find('meta', attrs={'name': 'viewport'})
        return {
            'viewport_present': bool(viewport),
            'viewport_content': viewport.get('content') if viewport else None,
        }

    def get_schema_org(self):
        schema_tags = self.soup.find_all('script', type='application/ld+json')
        schemas = []
        for tag in schema_tags:
            try:
                schemas.append(json.loads(tag.string))
            except:
                continue
        return schemas

    def get_open_graph_tags(self):
        og_tags = {}
        for tag in self.soup.find_all('meta', property=re.compile(r'^og:')):
            og_tags[tag.get('property')] = tag.get('content')
        return og_tags

    def check_robots_txt(self):
        parsed_url = urlparse(self.url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        rp = RobotFileParser()
        rp.set_url(robots_url)
        try:
            rp.read()
            return {
                'can_fetch': rp.can_fetch("*", self.url),
                'sitemaps': rp.site_maps()
            }
        except:
            return {'error': 'Impossible de lire robots.txt'}

    def check_sitemap(self):
        parsed_url = urlparse(self.url)
        sitemap_url = f"{parsed_url.scheme}://{parsed_url.netloc}/sitemap.xml"
        try:
            response = self.session.get(sitemap_url)
            root = ET.fromstring(response.content)
            urls = [url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text 
                   for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')]
            return {'urls_count': len(urls), 'urls': urls[:10]}
        except:
            return {'error': 'Sitemap non trouvé ou invalide'}
