import streamlit as st
import pandas as pd
import re
from text_analyzer import TextAnalyzer

# Diccionarios de idiomas
LANGUAGES = {
    "🇪🇸 Español": {
        "title": "📝 Textual Guardian",
        "input_text": "📝 Ingresa tu texto:",
        "placeholder": "Escribe o pega aquí el texto que deseas analizar...\n\nPresiona 'Analizar' o sal del área de texto para ver los resultados.",
        "analyze_button": "🔍 Analizar Texto",
        "legend_title": "🎨 Leyenda de Colores:",
        "specific_counts": "🔤 Conteos Específicos:",
        "marked_text": "🎨 Texto con Errores Marcados:",
        "info_message": "👈 Escribe texto y presiona 'Analizar' o sal del área de texto para ver los resultados",
        "no_problems": "🎉 ¡No se detectaron problemas en tu texto!",
        "total_words": "📊 Total de palabras:",
        "total_sentences": "📝 Total de oraciones:",
        "repeated_words": "🔄 Palabras repetidas:",
        "total_problems": "⚠️ Total de problemas:",
        "count_y": "Cantidad de \"y\":",
        "count_pero": "Cantidad de \"pero\":",
        "count_que": "Cantidad de \"que\":",
        "possible_participles": "Posibles participios:",
        "possible_gerunds": "Posibles gerundios:",
        "participles": "Participios",
        "gerunds": "Gerundios", 
        "problematic_expressions": "Expresiones problemáticas",
        "qualitative_adjectives": "Adjetivos calificativos",
        "repeated_words_label": "Palabras repetidas",
        "incorrect_commas": "Comas antes de 'y'"
    },
    "🇺🇸 English": {
        "title": "📝 Textual Guardian",
        "input_text": "📝 Enter your text:",
        "placeholder": "Write or paste the text you want to analyze here...\n\nPress 'Analyze' or leave the text area to see results.",
        "analyze_button": "🔍 Analyze Text",
        "legend_title": "🎨 Color Legend:",
        "specific_counts": "🔤 Specific Counts:",
        "marked_text": "🎨 Text with Marked Errors:",
        "info_message": "👈 Write text and press 'Analyze' or leave the text area to see results",
        "no_problems": "🎉 No problems detected in your text!",
        "total_words": "📊 Total words:",
        "total_sentences": "📝 Total sentences:",
        "repeated_words": "🔄 Repeated words:",
        "total_problems": "⚠️ Total problems:",
        "count_and": "Count of \"and\":",
        "count_but": "Count of \"but\":",
        "count_that": "Count of \"that\":",
        "possible_participles": "Possible participles:",
        "possible_gerunds": "Possible gerunds:",
        "participles": "Participles",
        "gerunds": "Gerunds",
        "problematic_expressions": "Problematic expressions",
        "qualitative_adjectives": "Qualitative adjectives", 
        "repeated_words_label": "Repeated words",
        "incorrect_commas": "Commas before 'and'"
    }
}

def get_text(key, language="🇪🇸 Español"):
    """Obtiene texto traducido según el idioma seleccionado"""
    return LANGUAGES.get(language, LANGUAGES["🇪🇸 Español"]).get(key, key)

def main():
    # Configuración de la página
    st.set_page_config(
        page_title="Textual Guardian - Analizador de Redacción Académica",
        page_icon="📝",
        layout="wide"
    )
    
    # CSS personalizado para colores de highlighting y tema oscuro
    st.markdown("""
    <style>
    .participio { background-color: #ffeb3b; color: #000; padding: 2px 4px; border-radius: 3px; font-weight: bold; }
    .gerundio { background-color: #ff9800; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; }
    .expresion-problematica { background-color: #f44336; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; }
    .adjetivo-problematico { background-color: #9c27b0; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; }
    .palabra-repetida { background-color: #2196f3; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; }
    .coma-incorrecta { background-color: #e91e63; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; }
    
    .metric-card {
        background-color: rgba(240, 242, 246, 0.1);
        border: 1px solid rgba(128, 128, 128, 0.3);
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 8px 0;
        color: inherit;
    }
    
    .error-card {
        background-color: rgba(255, 243, 205, 0.1);
        border: 1px solid rgba(255, 193, 7, 0.3);
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin: 8px 0;
        color: inherit;
    }
    
    .success-card {
        background-color: rgba(212, 237, 218, 0.1);
        border: 1px solid rgba(40, 167, 69, 0.3);
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 8px 0;
        color: inherit;
    }
    
    .centered-title {
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        margin-top: 0;
    }
    
    .text-highlight-container {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.3);
        padding: 15px;
        border-radius: 5px;
        line-height: 1.6;
        color: inherit;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Selector de idioma
    col_lang1, col_lang2, col_lang3 = st.columns([1, 2, 1])
    with col_lang2:
        selected_language = st.selectbox(
            "🌐 Language / Idioma:",
            options=list(LANGUAGES.keys()),
            index=0,
            key="language_selector"
        )
    
    # Título principal centrado
    st.markdown(f'<h1 class="centered-title">{get_text("title", selected_language)}</h1>', unsafe_allow_html=True)
    
    # Layout principal en dos columnas
    col1, col2 = st.columns([1, 1])
    
    # COLUMNA IZQUIERDA - Área de texto y leyenda
    with col1:
        st.markdown(f"#### {get_text('input_text', selected_language)}")
        text_input = st.text_area(
            "",
            height=370,
            placeholder=get_text("placeholder", selected_language),
            key="text_input",
            on_change=lambda: st.session_state.update({"trigger_analysis": True})
        )
        
        # Botón de análisis
        analyze_button = st.button(get_text("analyze_button", selected_language), type="primary", use_container_width=True)
        
        # Inicializar session state
        if "trigger_analysis" not in st.session_state:
            st.session_state.trigger_analysis = False
        
        # Determinar si debe hacer análisis
        should_analyze = (
            (text_input and text_input.strip()) and 
            (analyze_button or st.session_state.trigger_analysis)
        )
        
        if should_analyze:
            # Resetear trigger
            st.session_state.trigger_analysis = False
            
            # Crear instancia del analizador con idioma
            analyzer = TextAnalyzer(language=selected_language)
            
            # Realizar análisis
            results = analyzer.analyze_text(text_input)
            
            # Guardar resultados en session state
            st.session_state.analysis_results = results
            st.session_state.analyzed_text = text_input
            st.session_state.analysis_language = selected_language
        
        # Mostrar leyenda si hay resultados
        if ("analysis_results" in st.session_state and 
            "analyzed_text" in st.session_state and 
            st.session_state.analyzed_text == text_input):
            st.markdown(f"##### {get_text('legend_title', selected_language)}")
            display_dynamic_legend(st.session_state.analysis_results, selected_language)
    
    # COLUMNA DERECHA - Análisis
    with col2:
        if ("analysis_results" in st.session_state and 
            "analyzed_text" in st.session_state and 
            text_input and text_input.strip() and
            st.session_state.analyzed_text == text_input):
            
            # Mostrar conteos específicos
            display_specific_counts(st.session_state.analysis_results, selected_language)
            
            # Mostrar texto marcado
            st.markdown(f"##### {get_text('marked_text', selected_language)}")
            marked_text = create_highlighted_text(text_input, st.session_state.analysis_results)
            st.markdown(marked_text, unsafe_allow_html=True)
            
        else:
            st.info(get_text("info_message", selected_language))

def display_dynamic_legend(results, language="🇪🇸 Español"):
    """Muestra leyenda de colores con palabras reales encontradas"""
    
    legend_items = []
    
    # Participios
    if results['participios']:
        participios_text = ', '.join(results['participios'])
        legend_items.append(f'<span class="participio">{get_text("participles", language)}</span>: {participios_text}')
    
    # Gerundios
    if results['gerundios']:
        gerundios_text = ', '.join(results['gerundios'])
        legend_items.append(f'<span class="gerundio">{get_text("gerunds", language)}</span>: {gerundios_text}')
    
    # Expresiones problemáticas
    if results['forbidden_expressions']:
        expresiones_text = ', '.join(results['forbidden_expressions'])
        legend_items.append(f'<span class="expresion-problematica">{get_text("problematic_expressions", language)}</span>: {expresiones_text}')
    
    # Adjetivos problemáticos
    if results['problematic_adjectives']:
        adjetivos_text = ', '.join(results['problematic_adjectives'])
        legend_items.append(f'<span class="adjetivo-problematico">{get_text("qualitative_adjectives", language)}</span>: {adjetivos_text}')
    
    # Palabras repetidas
    if results['repeated_words']:
        repetidas_text = ', '.join(list(results['repeated_words'].keys()))
        legend_items.append(f'<span class="palabra-repetida">{get_text("repeated_words_label", language)}</span>: {repetidas_text}')
    
    # Comas incorrectas
    if results['comma_before_y']:
        comas_text = ', '.join([f'"{item}"' for item in results['comma_before_y']])
        comma_label = get_text("incorrect_commas", language)
        legend_items.append(f'<span class="coma-incorrecta">{comma_label}</span>: {comas_text}')
    
    if legend_items:
        legend_html = '<br>'.join(legend_items)
        st.markdown(f"""
        <div style="margin: 5px 0; padding: 10px; background-color: rgba(128, 128, 128, 0.1); border-radius: 5px;">
            {legend_html}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success(get_text("no_problems", language))

def display_specific_counts(results, language="🇪🇸 Español"):
    """Muestra conteos específicos en formato compacto"""
    
    # Conteos específicos
    word_count = results['word_count']
    sentence_count = results['sentence_count']
    repeated_count = len(results['repeated_words'])
    participios_count = len(results['participios'])
    gerundios_count = len(results['gerundios'])
    expresiones_count = len(results['forbidden_expressions'])
    adjetivos_count = len(results['problematic_adjectives'])
    comas_count = len(results['comma_before_y'])
    
    # Conteos de palabras específicas
    specific_counts = results['specific_word_counts']
    
    # Calcular total de problemas
    total_issues = participios_count + gerundios_count + expresiones_count + adjetivos_count + comas_count
    
    # Conteos específicos compactos
    st.markdown(f"##### {get_text('specific_counts', language)}")
    
    # Obtener conteos específicos según idioma
    if language == "🇺🇸 English":
        count1_label = get_text("count_and", language)
        count1_value = specific_counts.get('and', 0)
        count2_label = get_text("count_but", language) 
        count2_value = specific_counts.get('but', 0)
        count3_label = get_text("count_that", language)
        count3_value = specific_counts.get('that', 0)
    else:
        count1_label = get_text("count_y", language)
        count1_value = specific_counts.get('y', 0)
        count2_label = get_text("count_pero", language)
        count2_value = specific_counts.get('pero', 0)
        count3_label = get_text("count_que", language)
        count3_value = specific_counts.get('que', 0)
    
    st.markdown(f"""
    <div class="metric-card">
        <p><strong>{get_text("total_words", language)}</strong> {word_count}</p>
        <p><strong>{get_text("total_sentences", language)}</strong> {sentence_count}</p>
        <p><strong>{get_text("repeated_words", language)}</strong> {repeated_count}</p>
        <p><strong>{get_text("total_problems", language)}</strong> {total_issues}</p>
        <hr>
        <p><strong>{count1_label}</strong> {count1_value}</p>
        <p><strong>{count2_label}</strong> {count2_value}</p>
        <p><strong>{count3_label}</strong> {count3_value}</p>
        <p><strong>{get_text("possible_participles", language)}</strong> {participios_count}</p>
        <p><strong>{get_text("possible_gerunds", language)}</strong> {gerundios_count}</p>
    </div>
    """, unsafe_allow_html=True)

def display_live_stats(results):
    """Muestra estadísticas en tiempo real"""
    
    # Conteos específicos
    word_count = results['word_count']
    sentence_count = results['sentence_count']
    repeated_count = len(results['repeated_words'])
    participios_count = len(results['participios'])
    gerundios_count = len(results['gerundios'])
    expresiones_count = len(results['forbidden_expressions'])
    adjetivos_count = len(results['problematic_adjectives'])
    comas_count = len(results['comma_before_y'])
    
    # Conteos de palabras específicas
    specific_counts = results['specific_word_counts']
    
    # Calcular total de problemas
    total_issues = participios_count + gerundios_count + expresiones_count + adjetivos_count + comas_count
    
    # Estadísticas principales con tarjetas
    st.markdown(f"""
    <div class="metric-card">
        <h4>📊 Estadísticas Generales</h4>
        <p><strong>Total de palabras:</strong> {word_count}</p>
        <p><strong>Total de oraciones:</strong> {sentence_count}</p>
        <p><strong>Palabras repetidas:</strong> {repeated_count}</p>
        <p><strong>Total de problemas:</strong> {total_issues}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Conteos de palabras específicas
    st.markdown(f"""
    <div class="metric-card">
        <h4>🔤 Conteos Específicos</h4>
        <p><strong>Cantidad de "y" utilizadas:</strong> {specific_counts['y']}</p>
        <p><strong>Cantidad de "pero" utilizadas:</strong> {specific_counts['pero']}</p>
        <p><strong>Cantidad de "que" utilizadas:</strong> {specific_counts['que']}</p>
        <p><strong>Cantidad de "de" utilizadas:</strong> {specific_counts['de']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Conteos específicos por tipo de error
    if total_issues > 0:
        st.markdown("#### ⚠️ Problemas Detectados:")
        
        if participios_count > 0:
            st.markdown(f"""
            <div class="error-card">
                <strong>📋 Cantidad de posibles participios:</strong> {participios_count}<br>
                <small>Palabras: {', '.join(results['participios'])}</small>
            </div>
            """, unsafe_allow_html=True)
        
        if gerundios_count > 0:
            st.markdown(f"""
            <div class="error-card">
                <strong>🔄 Cantidad de posibles gerundios:</strong> {gerundios_count}<br>
                <small>Palabras: {', '.join(results['gerundios'])}</small>
            </div>
            """, unsafe_allow_html=True)
        
        if expresiones_count > 0:
            st.markdown(f"""
            <div class="error-card">
                <strong>⚠️ Expresiones problemáticas:</strong> {expresiones_count}<br>
                <small>Expresiones: {', '.join(results['forbidden_expressions'])}</small>
            </div>
            """, unsafe_allow_html=True)
        
        if adjetivos_count > 0:
            st.markdown(f"""
            <div class="error-card">
                <strong>🏷️ Adjetivos problemáticos:</strong> {adjetivos_count}<br>
                <small>Palabras: {', '.join(results['problematic_adjectives'])}</small>
            </div>
            """, unsafe_allow_html=True)
        
        if comas_count > 0:
            st.markdown(f"""
            <div class="error-card">
                <strong>✏️ Comas incorrectas:</strong> {comas_count}<br>
                <small>Encontradas: {', '.join(results['comma_before_y'])}</small>
            </div>
            """, unsafe_allow_html=True)
        
        if repeated_count > 0:
            st.markdown("#### 🔄 Palabras Repetidas:")
            for word, count in results['repeated_words'].items():
                st.markdown(f"""
                <div class="error-card">
                    <strong>'{word}'</strong> aparece <strong>{count} veces</strong>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="success-card">
            <h4>🎉 ¡Excelente!</h4>
            <p>No se detectaron problemas comunes de redacción en tu texto.</p>
        </div>
        """, unsafe_allow_html=True)

def create_highlighted_text(text, results):
    """Crea texto con highlighting de colores para errores"""
    highlighted_text = text
    
    # Marcar palabras repetidas (primero para que otros colores tomen prioridad)
    for word in results['repeated_words'].keys():
        pattern = r'\b' + re.escape(word) + r'\b'
        highlighted_text = re.sub(
            pattern, 
            f'<span class="palabra-repetida">{word}</span>',
            highlighted_text,
            flags=re.IGNORECASE
        )
    
    # Marcar participios
    for participio in results['participios']:
        pattern = r'\b' + re.escape(participio) + r'\b'
        highlighted_text = re.sub(
            pattern,
            f'<span class="participio">{participio}</span>',
            highlighted_text,
            flags=re.IGNORECASE
        )
    
    # Marcar gerundios
    for gerundio in results['gerundios']:
        pattern = r'\b' + re.escape(gerundio) + r'\b'
        highlighted_text = re.sub(
            pattern,
            f'<span class="gerundio">{gerundio}</span>',
            highlighted_text,
            flags=re.IGNORECASE
        )
    
    # Marcar expresiones problemáticas
    for expression in results['forbidden_expressions']:
        pattern = r'\b' + re.escape(expression) + r'\b'
        highlighted_text = re.sub(
            pattern,
            f'<span class="expresion-problematica">{expression}</span>',
            highlighted_text,
            flags=re.IGNORECASE
        )
    
    # Marcar adjetivos problemáticos
    for adjetivo in results['problematic_adjectives']:
        pattern = r'\b' + re.escape(adjetivo) + r'\b'
        highlighted_text = re.sub(
            pattern,
            f'<span class="adjetivo-problematico">{adjetivo}</span>',
            highlighted_text,
            flags=re.IGNORECASE
        )
    
    # Marcar comas antes de 'y'
    for comma_y in results['comma_before_y']:
        highlighted_text = highlighted_text.replace(
            comma_y,
            f'<span class="coma-incorrecta">{comma_y}</span>'
        )
    
    # Preservar saltos de línea
    highlighted_text = highlighted_text.replace('\n', '<br>')
    
    return f'<div class="text-highlight-container">{highlighted_text}</div>'

if __name__ == "__main__":
    main()