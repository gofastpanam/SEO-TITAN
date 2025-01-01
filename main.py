"""
Script principal de l'analyseur SEO
"""

from colorama import init, Fore, Style
from seotitan.analyzer import SEOAnalyzer
from seotitan.report import SEOReport

def main():
    init()  # Initialize colorama
    print(f"{Fore.YELLOW}=== Analyseur SEO ===\n{Style.RESET_ALL}")
    
    while True:
        url = input("Entrez l'URL du site à analyser (ou 'q' pour quitter) : ").strip()
        if url.lower() == 'q':
            break
            
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        output_file = input("Nom du fichier de sortie (ex: rapport_seo.txt) : ").strip()
        if not output_file.endswith('.txt'):
            output_file += '.txt'
            
        try:
            analyzer = SEOAnalyzer(url)
            report = SEOReport(analyzer)
            report.generate(output_file)
        except Exception as e:
            print(f"{Fore.RED}Erreur: {str(e)}{Style.RESET_ALL}")
        
        print("\nVoulez-vous analyser un autre site ?")

if __name__ == "__main__":
    main()
