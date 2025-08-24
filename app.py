import streamlit as st
import pandas as pd
from text_analyzer import TextAnalyzer

def main():
    # Configuración de la página
    st.set_page_config(
        page_title="Textual Guardian - Analizador de Redacción Académica",
        page_icon="📝",
        layout="wide"
    )
    
    # Título principal
    st.title("📝 Textual Guardian")
    st.subheader("Analizador de Redacción Académica")
    st.markdown("---")
    
    # Descripción
    st.markdown("""
    **Textual Guardian** te ayuda a mejorar tu redacción académica detectando:
    - 🔄 Palabras repetidas
    - 📋 Participios (-ado, -ido)  
    - 🔄 Gerundios (-ando, -endo)
    - ⚠️ Expresiones problemáticas
    - 📊 Estadísticas del texto
    """)
    
    # Área de texto
    text_input = st.text_area(
        "Ingresa tu párrafo para analizar:",
        height=200,
        placeholder="Escribe o pega aquí el texto que deseas analizar..."
    )
    
    # Botón de análisis
    if st.button("🔍 Analizar Texto", type="primary"):
        if text_input.strip():
            # Crear instancia del analizador
            analyzer = TextAnalyzer()
            
            # Realizar análisis
            results = analyzer.analyze_text(text_input)
            
            # Mostrar resultados
            display_results(results, text_input)
        else:
            st.warning("⚠️ Por favor, ingresa un texto para analizar.")

def display_results(results, original_text):
    """Muestra los resultados del análisis"""
    
    # Estadísticas generales
    st.markdown("## 📊 Estadísticas Generales")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Palabras", results['word_count'])
    
    with col2:
        repeated_count = len(results['repeated_words'])
        st.metric("Palabras Repetidas", repeated_count)
    
    with col3:
        issues_count = (
            len(results['participios']) + 
            len(results['gerundios']) + 
            len(results['forbidden_expressions']) +
            len(results['problematic_adjectives']) +
            len(results['comma_before_y'])
        )
        st.metric("Problemas Detectados", issues_count)
    
    st.markdown("---")
    
    # Palabras repetidas
    if results['repeated_words']:
        st.markdown("## 🔄 Palabras Repetidas")
        st.write("Estas palabras aparecen múltiples veces en tu texto:")
        
        # Crear DataFrame para mejor visualización
        repeated_df = pd.DataFrame(
            list(results['repeated_words'].items()),
            columns=['Palabra', 'Repeticiones']
        ).sort_values('Repeticiones', ascending=False)
        
        st.dataframe(repeated_df, use_container_width=True)
        
        with st.expander("💡 Sugerencia"):
            st.info("Utiliza sinónimos para evitar la repetición excesiva de términos dentro del mismo párrafo.")
    
    # Participios
    if results['participios']:
        st.markdown("## 📋 Participios Detectados")
        st.write("Palabras con terminaciones -ado, -ido encontradas:")
        
        participios_text = ", ".join(results['participios'])
        st.warning(f"**{participios_text}**")
        
        with st.expander("💡 Sugerencia"):
            st.info("Evita el uso excesivo de participios. Considera usar formas verbales activas o reestructurar las oraciones.")
    
    # Gerundios
    if results['gerundios']:
        st.markdown("## 🔄 Gerundios Detectados")
        st.write("Palabras con terminaciones -ando, -endo encontradas:")
        
        gerundios_text = ", ".join(results['gerundios'])
        st.warning(f"**{gerundios_text}**")
        
        with st.expander("💡 Sugerencia"):
            st.info("Elimina el uso de gerundios. Utiliza formas verbales más directas y precisas.")
    
    # Expresiones problemáticas
    if results['forbidden_expressions']:
        st.markdown("## ⚠️ Expresiones Problemáticas")
        st.write("Se encontraron estas expresiones que deberías evitar:")
        
        for expression in results['forbidden_expressions']:
            st.error(f"**'{expression}'**")
        
        with st.expander("💡 Sugerencias de reemplazo"):
            suggestions = {
                "ya que": "debido a que, dado que, porque",
                "puesto que": "dado que, considerando que",
                "etc.": "tales como, entre otros, y otros vinculados",
                "pero": "sin embargo, no obstante, aunque",
                "puede": "permite, facilita, logra",
                "pueden": "permiten, facilitan, logran",
                "pretende": "busca, requiere, tiene como objetivo"
            }
            
            for expr in results['forbidden_expressions']:
                if expr in suggestions:
                    st.info(f"**'{expr}'** → {suggestions[expr]}")
    
    # Adjetivos problemáticos
    if results['problematic_adjectives']:
        st.markdown("## 🏷️ Adjetivos Calificativos Problemáticos")
        st.write("Adjetivos que deberías evitar en redacción académica:")
        
        adjectives_text = ", ".join(results['problematic_adjectives'])
        st.warning(f"**{adjectives_text}**")
        
        with st.expander("💡 Sugerencia"):
            st.info("Evita adjetivos calificativos vagos. Usa términos más específicos y precisos.")
    
    # Comas antes de 'y'
    if results['comma_before_y']:
        st.markdown("## ✏️ Puntuación Incorrecta")
        st.write("Se encontraron comas antes del conectivo 'y':")
        
        for comma_y in results['comma_before_y']:
            st.warning(f"**'{comma_y}'**")
        
        with st.expander("💡 Sugerencia"):
            st.info("No coloques coma antes del conectivo 'y', excepto en casos muy específicos.")
    
    # Si no hay problemas
    if issues_count == 0 and not results['repeated_words']:
        st.success("🎉 ¡Excelente! No se detectaron problemas comunes de redacción en tu texto.")
    
    # Texto marcado (opcional)
    with st.expander("📄 Ver texto con marcas"):
        marked_text = mark_text_issues(original_text, results)
        st.markdown(marked_text, unsafe_allow_html=True)

def mark_text_issues(text, results):
    """Marca visualmente los problemas en el texto"""
    marked_text = text
    
    # Marcar participios
    for participio in results['participios']:
        marked_text = marked_text.replace(
            participio, 
            f'<span style="background-color: #ffeb3b; padding: 2px;">{participio}</span>'
        )
    
    # Marcar gerundios  
    for gerundio in results['gerundios']:
        marked_text = marked_text.replace(
            gerundio,
            f'<span style="background-color: #ff9800; padding: 2px;">{gerundio}</span>'
        )
    
    # Marcar expresiones problemáticas
    for expression in results['forbidden_expressions']:
        marked_text = marked_text.replace(
            expression,
            f'<span style="background-color: #f44336; color: white; padding: 2px;">{expression}</span>'
        )
    
    return marked_text

if __name__ == "__main__":
    main()
