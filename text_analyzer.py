import re
from collections import Counter
from typing import List, Dict, Set

class TextAnalyzer:
    """
    Analizador de texto para detectar problemas comunes en redacción académica
    """
    
    def __init__(self, language="🇪🇸 Español"):
        self.language = language
        
        if language == "🇺🇸 English":
            # English problematic expressions
            self.forbidden_expressions = [
                "but", "however", "can achieve", "can motivate", "can", "could",
                "pretends", "his", "her", "its", "their"
            ]
            
            # English problematic adjectives
            self.problematic_adjectives = [
                "big", "small", "many", "few", "some", "several", 
                "various", "multiple", "large", "little"
            ]
        else:
            # Spanish problematic expressions (default)
            self.forbidden_expressions = [
                "ya que", "de que", "puesto que", "etc.", "pero",
                "puede lograr", "pueden motivar", "puede", "pueden",
                "pretende", "su", "sus"
            ]
            
            # Spanish problematic adjectives
            self.problematic_adjectives = [
                "grande", "pequeño", "muchos", "pocos", "algunos",
                "varios", "diversas", "múltiples"
            ]
    
    def count_words(self, text: str) -> int:
        """Cuenta el número de palabras en el texto"""
        words = re.findall(r'\b\w+\b', text.lower())
        return len(words)
    
    def find_repeated_words(self, text: str) -> Dict[str, int]:
        """Encuentra palabras repetidas en el texto (más de una vez)"""
        # Extraer solo palabras (sin puntuación)
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filtrar palabras muy comunes que es normal repetir
        common_words = {
            'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
            'de', 'del', 'en', 'con', 'por', 'para', 'a', 'al',
            'se', 'es', 'son', 'y', 'o', 'que', 'no', 'si',
            'como', 'cuando', 'donde', 'este', 'esta', 'estos', 'estas'
        }
        
        # Contar palabras excluyendo las comunes
        filtered_words = [word for word in words if word not in common_words and len(word) > 2]
        word_counts = Counter(filtered_words)
        
        # Retornar solo las que aparecen más de una vez
        return {word: count for word, count in word_counts.items() if count > 1}
    
    def find_participios(self, text: str) -> List[str]:
        """Encuentra participios según el idioma"""
        words = re.findall(r'\b\w+\b', text.lower())
        participios = []
        
        if self.language == "🇺🇸 English":
            # English past participles (usually -ed, but also irregular ones)
            for word in words:
                if (word.endswith('ed') and len(word) > 4):
                    # Exclude common words that aren't problematic
                    if word not in ['based', 'used', 'called', 'named', 'related', 'needed']:
                        participios.append(word)
        else:
            # Spanish participles (-ado, -ido)
            for word in words:
                if word.endswith('ado') or word.endswith('ido'):
                    # Exclude common words that aren't problematic
                    if word not in ['estado', 'lado', 'caso', 'modo', 'todo', 'nido', 'ido']:
                        participios.append(word)
        
        return list(set(participios))  # Eliminar duplicados
    
    def find_gerundios(self, text: str) -> List[str]:
        """Encuentra gerundios según el idioma"""
        words = re.findall(r'\b\w+\b', text.lower())
        gerundios = []
        
        if self.language == "🇺🇸 English":
            # English gerunds (-ing forms)
            for word in words:
                if word.endswith('ing') and len(word) > 4:
                    # Exclude common words that aren't problematic
                    if word not in ['thing', 'nothing', 'something', 'anything', 'everything']:
                        gerundios.append(word)
        else:
            # Spanish gerunds (-ando, -endo)
            for word in words:
                if word.endswith('ando') or word.endswith('endo'):
                    gerundios.append(word)
        
        return list(set(gerundios))  # Eliminar duplicados
    
    def find_forbidden_expressions(self, text: str) -> List[str]:
        """Encuentra expresiones prohibidas según las indicaciones"""
        found_expressions = []
        text_lower = text.lower()
        
        for expression in self.forbidden_expressions:
            # Para expresiones de múltiples palabras, buscar exactamente
            if ' ' in expression:
                if expression in text_lower:
                    found_expressions.append(expression)
            else:
                # Para palabras individuales, usar límites de palabra
                pattern = r'\b' + re.escape(expression) + r'\b'
                if re.search(pattern, text_lower):
                    found_expressions.append(expression)
        
        return found_expressions
    
    def find_problematic_adjectives(self, text: str) -> List[str]:
        """Encuentra adjetivos calificativos problemáticos"""
        words = re.findall(r'\b\w+\b', text.lower())
        found_adjectives = []
        
        for word in words:
            if word in self.problematic_adjectives:
                found_adjectives.append(word)
        
        return list(set(found_adjectives))
    
    def check_comma_before_y(self, text: str) -> List[str]:
        """Detecta comas antes del conectivo según el idioma"""
        if self.language == "🇺🇸 English":
            # Check for commas before 'and'
            pattern = r',\s+and\b'
        else:
            # Check for commas before 'y'
            pattern = r',\s+y\b'
        
        matches = re.finditer(pattern, text, re.IGNORECASE)
        return [match.group() for match in matches]
    
    def count_specific_words(self, text: str) -> Dict[str, int]:
        """Cuenta palabras específicas según el idioma"""
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        if self.language == "🇺🇸 English":
            specific_counts = {
                'and': words.count('and'),
                'but': words.count('but'),
                'that': words.count('that'),
                'the': words.count('the'),
                'of': words.count('of'),
                'in': words.count('in'),
                'with': words.count('with'),
                'for': words.count('for'),
                'to': words.count('to'),
                'by': words.count('by')
            }
        else:
            specific_counts = {
                'y': words.count('y'),
                'pero': words.count('pero'),
                'que': words.count('que'),
                'de': words.count('de'),
                'el': words.count('el'),
                'la': words.count('la'),
                'en': words.count('en'),
                'con': words.count('con'),
                'por': words.count('por'),
                'para': words.count('para')
            }
        
        return specific_counts
    
    def count_sentences(self, text: str) -> int:
        """Cuenta el número de oraciones en el texto"""
        sentences = re.split(r'[.!?]+', text.strip())
        return len([s for s in sentences if s.strip()])
    
    def analyze_text(self, text: str) -> Dict:
        """Realiza un análisis completo del texto"""
        return {
            'word_count': self.count_words(text),
            'sentence_count': self.count_sentences(text),
            'repeated_words': self.find_repeated_words(text),
            'participios': self.find_participios(text),
            'gerundios': self.find_gerundios(text),
            'forbidden_expressions': self.find_forbidden_expressions(text),
            'problematic_adjectives': self.find_problematic_adjectives(text),
            'comma_before_y': self.check_comma_before_y(text),
            'specific_word_counts': self.count_specific_words(text)
        }
