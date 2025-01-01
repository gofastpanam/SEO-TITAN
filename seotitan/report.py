"""
Module de génération de rapport SEO
"""

from datetime import datetime
from colorama import Fore, Style
from .suggestions import SEOSuggestions

class SEOReport:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def generate(self, output_file):
        print(f"{Fore.CYAN}Analyse SEO approfondie en cours pour {self.analyzer.url}...{Style.RESET_ALL}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            def write_section(title, content):
                separator = "="*50
                f.write(f"\n{separator}\n{title}\n{separator}\n")
                f.write(content + "\n")
            
            # En-tête du rapport
            f.write(f"Rapport d'analyse SEO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"URL analysée: {self.analyzer.url}\n")
            
            # Informations de base
            write_section("TITRE", self.analyzer.get_title())
            write_section("DESCRIPTION META", self.analyzer.get_meta_description())
            write_section("MOTS-CLÉS META", self.analyzer.get_meta_keywords())
            
            # Structure des titres
            headings = self.analyzer.get_headings_count()
            content = ""
            for tag, data in headings.items():
                content += f"\nNombre de {tag}: {data['count']}\n"
                if data['text']:
                    content += "Texte des balises:\n"
                    for text in data['text']:
                        content += f"- {text}\n"
            write_section("STRUCTURE DES EN-TÊTES", content)
            
            # Liens
            links = self.analyzer.get_links()
            content = f"Liens internes: {len(links['internal'])}\n"
            content += f"Liens externes: {len(links['external'])}\n"
            content += f"Liens cassés: {len(links['broken'])}\n"
            write_section("ANALYSE DES LIENS", content)
            
            # Images
            images = self.analyzer.get_images()
            content = f"Nombre total d'images: {len(images)}\n\n"
            for img in images:
                content += f"Source: {img['src']}\n"
                content += f"Alt: {img['alt']}\n\n"
            write_section("IMAGES ET ATTRIBUTS ALT", content)
            
            # Contenu
            write_section("LONGUEUR DU CONTENU", f"Nombre total de mots: {self.analyzer.get_content_length()}")
            
            # Densité des mots-clés
            density = self.analyzer.get_keyword_density()
            content = "Top 20 des mots-clés les plus utilisés:\n"
            for word, freq in density.items():
                content += f"{word}: {freq:.2f}%\n"
            write_section("DENSITÉ DES MOTS-CLÉS", content)
            
            # Éléments techniques
            write_section("URL CANONIQUE", self.analyzer.get_canonical())
            write_section("META ROBOTS", self.analyzer.get_robots_meta())
            write_section("FAVICON", self.analyzer.get_favicon())
            write_section("SSL", str(self.analyzer.check_ssl()))
            write_section("MOBILE OPTIMIZATION", str(self.analyzer.check_mobile_optimization()))
            write_section("SCHEMA.ORG", str(self.analyzer.get_schema_org()))
            write_section("OPEN GRAPH TAGS", str(self.analyzer.get_open_graph_tags()))
            write_section("ROBOTS.TXT", str(self.analyzer.check_robots_txt()))
            write_section("SITEMAP", str(self.analyzer.check_sitemap()))
            write_section("PERFORMANCE", f"Temps de chargement: {self.analyzer.load_time:.2f} secondes")

            # Suggestions d'amélioration
            suggestions = SEOSuggestions(self.analyzer)
            write_section("SUGGESTIONS D'AMÉLIORATION", suggestions.format_suggestions())

        print(f"{Fore.GREEN}Analyse terminée ! Le rapport a été enregistré dans {output_file}{Style.RESET_ALL}")
