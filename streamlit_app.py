import streamlit as st
import pandas as pd
import re
from text_analyzer import TextAnalyzer

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
    
    # Título principal centrado
    st.markdown('<h1 class="centered-title">📝 Textual Guardian</h1>', unsafe_allow_html=True)
    
    # Layout principal en dos columnas
    col1, col2 = st.columns([1, 1])
    
    # COLUMNA IZQUIERDA - Área de texto y leyenda
    with col1:
        st.markdown("#### 📝 Ingresa tu texto:")
        text_input = st.text_area(
            "",
            height=400,
            placeholder="Escribe o pega aquí el texto que deseas analizar...\n\nEl análisis se actualiza automáticamente mientras escribes.",
            key="text_input"
        )
        
        if text_input and text_input.strip():
            # Crear instancia del analizador
            analyzer = TextAnalyzer()
            
            # Realizar análisis
            results = analyzer.analyze_text(text_input)
            
            # Mostrar leyenda de colores con palabras reales debajo del párrafo
            st.markdown("##### 🎨 Leyenda de Colores:")
            display_dynamic_legend(results)
    
    # COLUMNA DERECHA - Análisis
    with col2:
        if text_input and text_input.strip():
            # Mostrar conteos específicos
            display_specific_counts(results)
            
            # Mostrar texto marcado
            st.markdown("##### 🎨 Texto con Errores Marcados:")
            marked_text = create_highlighted_text(text_input, results)
            st.markdown(marked_text, unsafe_allow_html=True)
            
        else:
            st.info("👈 Escribe algo en el área de texto para ver el análisis en tiempo real")

def display_dynamic_legend(results):
    """Muestra leyenda de colores con palabras reales encontradas"""
    
    legend_items = []
    
    # Participios
    if results['participios']:
        participios_text = ', '.join(results['participios'])
        legend_items.append(f'<span class="participio">Participios</span>: {participios_text}')
    
    # Gerundios
    if results['gerundios']:
        gerundios_text = ', '.join(results['gerundios'])
        legend_items.append(f'<span class="gerundio">Gerundios</span>: {gerundios_text}')
    
    # Expresiones problemáticas
    if results['forbidden_expressions']:
        expresiones_text = ', '.join(results['forbidden_expressions'])
        legend_items.append(f'<span class="expresion-problematica">Expresiones problemáticas</span>: {expresiones_text}')
    
    # Adjetivos problemáticos
    if results['problematic_adjectives']:
        adjetivos_text = ', '.join(results['problematic_adjectives'])
        legend_items.append(f'<span class="adjetivo-problematico">Adjetivos calificativos</span>: {adjetivos_text}')
    
    # Palabras repetidas
    if results['repeated_words']:
        repetidas_text = ', '.join(list(results['repeated_words'].keys()))
        legend_items.append(f'<span class="palabra-repetida">Palabras repetidas</span>: {repetidas_text}')
    
    # Comas incorrectas
    if results['comma_before_y']:
        comas_text = ', '.join([f'"{item}"' for item in results['comma_before_y']])
        legend_items.append(f'<span class="coma-incorrecta">Comas antes de \'y\'</span>: {comas_text}')
    
    if legend_items:
        legend_html = '<br>'.join(legend_items)
        st.markdown(f"""
        <div style="margin: 5px 0; padding: 10px; background-color: rgba(128, 128, 128, 0.1); border-radius: 5px;">
            {legend_html}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("🎉 ¡No se detectaron problemas en tu texto!")

def display_specific_counts(results):
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
    st.markdown("##### 🔤 Conteos Específicos:")
    st.markdown(f"""
    <div class="metric-card">
        <p><strong>📊 Total de palabras:</strong> {word_count}</p>
        <p><strong>📝 Total de oraciones:</strong> {sentence_count}</p>
        <p><strong>🔄 Palabras repetidas:</strong> {repeated_count}</p>
        <p><strong>⚠️ Total de problemas:</strong> {total_issues}</p>
        <hr>
        <p><strong>Cantidad de "y":</strong> {specific_counts['y']}</p>
        <p><strong>Cantidad de "pero":</strong> {specific_counts['pero']}</p>
        <p><strong>Cantidad de "que":</strong> {specific_counts['que']}</p>
        <p><strong>Posibles participios:</strong> {participios_count}</p>
        <p><strong>Posibles gerundios:</strong> {gerundios_count}</p>
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