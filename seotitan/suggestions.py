"""
Module de suggestions d'amélioration SEO
"""

class SEOSuggestions:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.suggestions = []
        self.priority_levels = {
            'critical': '🔴 CRITIQUE',
            'important': '🟠 IMPORTANT',
            'moderate': '🟡 MODÉRÉ',
            'minor': '🟢 MINEUR'
        }

    def analyze_title(self):
        title = self.analyzer.get_title()
        if not title:
            self.add_suggestion('critical', 'Titre manquant',
                              'Ajoutez un titre à votre page. Le titre est crucial pour le SEO.',
                              'Créez un titre unique et descriptif de 50-60 caractères.')
        elif len(title) < 30:
            self.add_suggestion('important', 'Titre trop court',
                              f'Votre titre fait {len(title)} caractères.',
                              'Allongez votre titre pour qu\'il soit plus descriptif (50-60 caractères).')
        elif len(title) > 60:
            self.add_suggestion('moderate', 'Titre trop long',
                              f'Votre titre fait {len(title)} caractères.',
                              'Raccourcissez votre titre à 50-60 caractères pour une meilleure visibilité dans les SERP.')

    def analyze_meta_description(self):
        desc = self.analyzer.get_meta_description()
        if not desc:
            self.add_suggestion('critical', 'Meta description manquante',
                              'Aucune meta description n\'est définie.',
                              'Ajoutez une meta description de 150-160 caractères qui décrit votre page.')
        elif len(desc) < 120:
            self.add_suggestion('important', 'Meta description trop courte',
                              f'Votre meta description fait {len(desc)} caractères.',
                              'Allongez votre meta description à 150-160 caractères.')
        elif len(desc) > 160:
            self.add_suggestion('moderate', 'Meta description trop longue',
                              f'Votre meta description fait {len(desc)} caractères.',
                              'Raccourcissez votre meta description à 150-160 caractères.')

    def analyze_headings(self):
        headings = self.analyzer.get_headings_count()
        if not headings.get('h1', {}).get('count'):
            self.add_suggestion('critical', 'Balise H1 manquante',
                              'Aucune balise H1 n\'est présente sur la page.',
                              'Ajoutez une balise H1 unique qui décrit le contenu principal de la page.')
        elif headings.get('h1', {}).get('count') > 1:
            self.add_suggestion('important', 'Plusieurs H1 détectés',
                              f"Il y a {headings.get('h1', {}).get('count')} balises H1 sur la page.",
                              'Gardez une seule balise H1 par page pour une meilleure structure.')

    def analyze_images(self):
        images = self.analyzer.get_images()
        missing_alt = [img for img in images if not img['alt'] or img['alt'] == 'Pas de texte alternatif']
        if missing_alt:
            self.add_suggestion('important', 'Images sans attribut ALT',
                              f'{len(missing_alt)} image(s) n\'ont pas de texte alternatif.',
                              'Ajoutez des attributs ALT descriptifs à toutes les images importantes.')

    def analyze_content_length(self):
        word_count = self.analyzer.get_content_length()
        if word_count < 300:
            self.add_suggestion('important', 'Contenu trop court',
                              f'Votre page contient seulement {word_count} mots.',
                              'Ajoutez plus de contenu pertinent. Visez au moins 300 mots pour les pages principales.')

    def analyze_links(self):
        links = self.analyzer.get_links()
        if links['broken']:
            self.add_suggestion('critical', 'Liens cassés détectés',
                              f'{len(links["broken"])} liens cassés trouvés.',
                              'Corrigez ou supprimez les liens cassés pour améliorer l\'expérience utilisateur.')
        
        if not links['internal']:
            self.add_suggestion('important', 'Pas de liens internes',
                              'Aucun lien interne n\'a été trouvé.',
                              'Ajoutez des liens internes pour améliorer la navigation et le référencement.')

    def analyze_mobile(self):
        mobile_info = self.analyzer.check_mobile_optimization()
        if not mobile_info['viewport_present']:
            self.add_suggestion('critical', 'Meta viewport manquante',
                              'La balise meta viewport est absente.',
                              'Ajoutez une balise meta viewport pour optimiser l\'affichage mobile.')

    def analyze_ssl(self):
        ssl_info = self.analyzer.check_ssl()
        if not ssl_info['secure']:
            self.add_suggestion('critical', 'HTTPS non activé',
                              'Votre site n\'utilise pas HTTPS.',
                              'Activez HTTPS pour sécuriser votre site et améliorer son référencement.')

    def analyze_performance(self):
        if self.analyzer.load_time > 3:
            self.add_suggestion('important', 'Temps de chargement lent',
                              f'Temps de chargement : {self.analyzer.load_time:.2f} secondes.',
                              'Optimisez les images, minifiez le CSS/JS, et utilisez un CDN pour améliorer la vitesse.')

    def add_suggestion(self, priority, title, problem, solution):
        self.suggestions.append({
            'priority': priority,
            'priority_label': self.priority_levels[priority],
            'title': title,
            'problem': problem,
            'solution': solution
        })

    def get_all_suggestions(self):
        # Effectue toutes les analyses
        self.analyze_title()
        self.analyze_meta_description()
        self.analyze_headings()
        self.analyze_images()
        self.analyze_content_length()
        self.analyze_links()
        self.analyze_mobile()
        self.analyze_ssl()
        self.analyze_performance()

        # Trie les suggestions par priorité
        priority_order = {'critical': 0, 'important': 1, 'moderate': 2, 'minor': 3}
        self.suggestions.sort(key=lambda x: priority_order[x['priority']])
        
        return self.suggestions

    def format_suggestions(self):
        suggestions = self.get_all_suggestions()
        if not suggestions:
            return "Aucune suggestion d'amélioration n'a été trouvée."

        formatted = "SUGGESTIONS D'AMÉLIORATION SEO\n" + "="*50 + "\n\n"
        
        for suggestion in suggestions:
            formatted += f"{suggestion['priority_label']} - {suggestion['title']}\n"
            formatted += f"Problème : {suggestion['problem']}\n"
            formatted += f"Solution : {suggestion['solution']}\n"
            formatted += "-"*50 + "\n"

        return formatted
