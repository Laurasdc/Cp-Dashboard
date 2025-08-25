import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from math import sqrt

st.set_page_config(
    page_title="Dashboard Profissional - Análise de Dados",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* Cor de fundo principal */
    .stApp {
        background-color: #1a1a2e;
        color: #e0e0e0;
        font-family: 'Roboto', sans-serif;
    }

    /* Título principal */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #00e5ff; /* Ciano vibrante */
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 1px 1px 10px rgba(0, 229, 255, 0.5);
    }

    /* Títulos de seção */
    .section-header {
        font-size: 2rem;
        color: #ff8c00; /* Laranja escuro */
        border-bottom: 3px solid #ff8c00;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    /* Cards de métricas */
    .metric-card {
        background-color: #2c2c54; /* Roxo escuro */
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #4a4a70;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        margin: 0.5rem 0;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: scale(1.03);
    }

    /* Estilo da barra lateral */
    .css-1d391kg { /* Classe do Streamlit para a sidebar */
        background-image: linear-gradient(180deg, #1a1a2e, #2c2c54);
    }
    .css-1d391kg .stSelectbox [data-baseweb="select"] {
        background-color: #2c2c54;
        color: #e0e0e0;
    }

    /* Estilizando os elementos de métrica do Streamlit */
    [data-testid="stMetric"] {
        background-color: #2c2c54;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #4a4a70;
    }
    [data-testid="stMetric"] > div {
        border-radius: 10px;
    }

    /* Mudar a cor do texto das métricas */
    [data-testid="stMetricValue"] {
        color: #00e5ff;
    }
    [data-testid="stMetricLabel"] {
        color: #ff8c00;
    }

    /* Rodapé */
    .footer {
        text-align: center;
        color: #888;
        padding: 1rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# --- O RESTANTE DO SEU CÓDIGO PERMANECE O MESMO ---

def confidence_interval(data, confidence=0.95):
    """Calcula intervalo de confiança para a média"""
    n = len(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    se = std / sqrt(n)
    
    if n >= 30:
        z_score = 1.96 if confidence == 0.95 else 2.576 
        margin_error = z_score * se
    else:
        t_values = {0.95: 2.0, 0.99: 2.6}  
        t_score = t_values.get(confidence, 2.0)
        margin_error = t_score * se
    
    return mean - margin_error, mean + margin_error

def t_test_independent(group1, group2):
    """Teste t para duas amostras independentes"""
    n1, n2 = len(group1), len(group2)
    mean1, mean2 = np.mean(group1), np.mean(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    
    pooled_se = sqrt(var1/n1 + var2/n2)
    
    t_stat = (mean1 - mean2) / pooled_se
    
    df = n1 + n2 - 2
    
    if abs(t_stat) > 2.576:
        p_value = 0.001
    elif abs(t_stat) > 1.96:
        p_value = 0.05
    elif abs(t_stat) > 1.645:
        p_value = 0.1
    else:
        p_value = 0.2
    
    return t_stat, p_value

@st.cache_data
def load_data():
    try:
        df = pd.read_excel('df_selecionado.xlsx')
        df['Data_Pedido'] = pd.to_datetime(df['Data_Pedido'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

st.sidebar.title("🧭 Navegação")
page = st.sidebar.selectbox(
    "Escolha uma seção:",
    ["🏠 Home", "🎓 Formação e Experiência", "💼 Skills", "📊 Análise de Dados"]
)

df = load_data()

if page == "🏠 Home":
    st.markdown('<h1 class="main-header">Dashboard Profissional</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.image("https://via.placeholder.com/300x300/00e5ff/1a1a2e?text=Sua+Foto", 
                 width=300, caption="Laura Souza de Carvalho")
    
    st.markdown('<h2 class="section-header">Sobre Mim</h2>', unsafe_allow_html=True)
    
    st.write("""
    Estudante de Engenharia de Software (4º semestre) apaixonada por tecnologia. 
    Experiência em desenvolvimento de sistemas com PHP, Laravel, Python e JavaScript. 
    Busco desafios que unam aprendizado e inovação.
    """)
    
    st.markdown('<h2 class="section-header">Objetivo Profissional</h2>', unsafe_allow_html=True)
    
    st.write("""
    Busco oportunidades para aplicar minhas habilidades em desenvolvimento de sistemas e análise de dados, gerando soluções inovadoras e impacto positivo. 
    Tenho interesse em projetos que envolvam:
    💻 Desenvolvimento de sistemas e automação
    📊 Dashboards interativos e visualização de dados
    📈 Análise de dados e modelagem preditiva
    🚀 Soluções inovadoras e data-driven
    """)

elif page == "🎓 Formação e Experiência":
    st.markdown('<h1 class="main-header">Formação e Experiência</h1>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">Formação Acadêmica</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎓 Graduação
        **Curso:** Engenharia de Software  
        **Instituição:** FIAP
        **Período:** 2024 - 2027
        **Principais Disciplinas:**
        - Agile Methodology with Squad Framework
        - AR/VR Modelling and Simulation
        - Data Science & Statistical Computing
        - Database Design
        - Domain Driven Design – Java
        - Dynamic Programming
        - Network Architect Solutions
        """)
    
    with col2:
        st.markdown("""
        ### 📜 Certificações
        - **Formação Aprenda a programar em JavaScript com foco no back-end** - Alura (02/2025)
        - **Formação Desenvolva aplicações Web em JavaScript com tarefas concorrentes e orientadas a objetos** - Alura (02/2025)
        - **Desenvolvimento Web Avançado com PHP, Laravel e Vue.js** - Udemy (01/2025)
        - **Formação Laravel: crie aplicações web em PHP** - Alura (11/2024)
        - **Formação PHP Web: crie aplicações web em PHP** - Alura (11/2024)
        - **Laravel: criando uma aplicação com MVC** - Alura (10/2024)o]
        """)
    
    st.markdown('<h2 class="section-header">Experiência Profissional</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 💼 Estágio em Desenvolvimento de Sistemas
    **Empresa:** Secretaria do Verde e Meio Ambiente  
    **Período:** 09/2024 - 08/2025  

    **Principais Responsabilidades:**
    - Desenvolvimento de sistemas internos e automação de processos
    - Implementação de funcionalidades em PHP, Laravel e JavaScript
    - Criação de dashboards e relatórios para análise de dados
    - Suporte à equipe na otimização de processos e soluções tecnológicas
    """)

elif page == "💼 Skills":
    st.markdown('<h1 class="main-header">Skills e Competências</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h2 class="section-header">Tecnologias</h2>', unsafe_allow_html=True)
        
        skills_tech = {
            "Python": 90,
            "Laravel": 85,
            "PHP": 85,
            "Java": 70,
            "SQL": 60,
        }
        
        for skill, level in skills_tech.items():
            st.write(f"**{skill}**")
            st.progress(level) 
            st.write("")
    
    with col2:
        st.markdown('<h2 class="section-header">Soft Skills</h2>', unsafe_allow_html=True)
        
        soft_skills = [
            "🧠 Pensamento Analítico",
            "📊 Interpretação de Dados",
            "🎯 Resolução de Problemas",
            "📈 Visão de Negócios",
            "🤝 Trabalho em Equipe",
            "📝 Comunicação Técnica",
            "⏰ Gestão de Tempo",
            "🔍 Atenção aos Detalhes"
        ]
        
        for skill in soft_skills:
            st.write(f"✅ {skill}")
    
    st.markdown('<h2 class="section-header">Ferramentas e Frameworks</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Análise de Dados:**
        - Pandas
        - NumPy
        - SciPy
        - Scikit-learn
        """)
    
    with col2:
        st.markdown("""
        **Visualização:**
        - Plotly
        - Matplotlib
        - Seaborn
        - Streamlit
        """)
    
    with col3:
        st.markdown("""
        **Desenvolvimento:**
        - Jupyter Notebook
        - VS Code
        - Git/GitHub
        - Docker
        """)

elif page == "📊 Análise de Dados":
    st.markdown('<h1 class="main-header">Análise de Dados - E-commerce</h1>', unsafe_allow_html=True)
    
    if df is not None:
        st.markdown('<h2 class="section-header">1. Apresentação dos Dados</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Registros", f"{len(df):,}")
        
        with col2:
            st.metric("Colunas", len(df.columns))
        
        with col3:
            valid_dates = df['Data_Pedido'].dropna()
            if len(valid_dates) > 0:
                st.metric("Período", f"{valid_dates.dt.year.min()} - {valid_dates.dt.year.max()}")
            else:
                st.metric("Período", "N/A")
        
        with col4:
            total_revenue = df['Valor_Pedido_BRL'].sum()
            if pd.notna(total_revenue):
                st.metric("Receita Total (BRL)", f"R$ {total_revenue:,.2f}")
            else:
                st.metric("Receita Total (BRL)", "N/A")

        st.write("""
        **Descrição do Dataset:**
        Este conjunto de dados contém informações sobre pedidos de e-commerce, incluindo dados de vendas, 
        logística, produtos e clientes. Os dados abrangem diferentes canais de venda, tipos de envio, 
        categorias de produtos e informações geográficas.
        """)

        st.markdown('<h3>Tipos de Variáveis:</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Variáveis Numéricas:**")
            numeric_vars = df.select_dtypes(include=[np.number]).columns.tolist()
            for var in numeric_vars:
                st.write(f"• {var}")
        
        with col2:
            st.write("**Variáveis Categóricas:**")
            categorical_vars = df.select_dtypes(include=['object', 'bool']).columns.tolist()
            for var in categorical_vars[:10]:  # Limitar para não ocupar muito espaço
                st.write(f"• {var}")
            if len(categorical_vars) > 10:
                st.write(f"... e mais {len(categorical_vars) - 10} variáveis")
        
        st.markdown('<h3>Principais Perguntas de Análise:</h3>', unsafe_allow_html=True)
        st.write("""
        1. **Qual a distribuição dos valores de pedidos e como ela se comporta estatisticamente?**
        2. **Existe diferença significativa entre vendas B2B e B2C?**
        3. **Como os diferentes canais de venda performam em termos de receita?**
        4. **Qual a correlação entre quantidade de itens e valor do pedido?**
        """)
        
        st.markdown('<h2 class="section-header">2. Análise Descritiva</h2>', unsafe_allow_html=True)

        valores_limpos = df['Valor_Pedido_BRL'].dropna()
        
        if len(valores_limpos) > 0:
            valor_stats = valores_limpos.describe()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Medidas de Tendência Central:**")
                st.write(f"Média: R$ {valor_stats['mean']:.2f}")
                st.write(f"Mediana: R$ {valor_stats['50%']:.2f}")
                moda = valores_limpos.mode()
                if len(moda) > 0:
                    st.write(f"Moda: R$ {moda.iloc[0]:.2f}")
                else:
                    st.write("Moda: N/A")
            
            with col2:
                st.markdown("**Medidas de Dispersão:**")
                st.write(f"Desvio Padrão: R$ {valor_stats['std']:.2f}")
                st.write(f"Variância: R$ {valores_limpos.var():.2f}")
                st.write(f"Amplitude: R$ {valor_stats['max'] - valor_stats['min']:.2f}")
            
            with col3:
                st.markdown("**Quartis:**")
                st.write(f"Q1: R$ {valor_stats['25%']:.2f}")
                st.write(f"Q2 (Mediana): R$ {valor_stats['50%']:.2f}")
                st.write(f"Q3: R$ {valor_stats['75%']:.2f}")
            
            # Gráficos com tema escuro do Plotly
            plotly_template = "plotly_dark"

            fig_hist = px.histogram(
                valores_limpos, 
                nbins=50,
                title='Distribuição dos Valores de Pedidos (BRL)',
                labels={'value': 'Valor do Pedido (BRL)', 'count': 'Frequência'},
                template=plotly_template
            )
            fig_hist.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_hist, use_container_width=True)
            
            fig_box = px.box(
                y=valores_limpos,
                title='Box Plot - Valores de Pedidos (BRL)',
                template=plotly_template
            )
            fig_box.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_box, use_container_width=True)
        
        st.markdown('<h3>Análise de Correlação</h3>', unsafe_allow_html=True)

        numeric_cols = ['Qty', 'Valor_Pedido', 'Valor_Pedido_BRL']
        available_cols = [col for col in numeric_cols if col in df.columns]
        
        if len(available_cols) >= 2:
            correlation_data = df[available_cols].corr()
            
            fig_corr = px.imshow(
                correlation_data,
                text_auto=True,
                aspect="auto",
                title="Matriz de Correlação - Variáveis Numéricas",
                template=plotly_template,
                color_continuous_scale='Tealrose' # Esquema de cores que combina com o tema
            )
            fig_corr.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_corr, use_container_width=True)
        
        st.markdown('<h3>Análise por Categorias</h3>', unsafe_allow_html=True)
        
        # Vendas por canal
        if 'Sales Channel' in df.columns and 'Valor_Pedido_BRL' in df.columns:
            sales_by_channel = df.groupby('Sales Channel')['Valor_Pedido_BRL'].agg(['sum', 'mean', 'count']).reset_index()
            sales_by_channel.columns = ['Canal', 'Receita Total', 'Ticket Médio', 'Quantidade']
            
            fig_channel = px.bar(
                sales_by_channel,
                x='Canal',
                y='Receita Total',
                title='Receita Total por Canal de Vendas',
                template=plotly_template,
                color_discrete_sequence=['#ff8c00']
            )
            fig_channel.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_channel, use_container_width=True)
        
        # Comparação B2B vs B2C
        if 'Venda_B2B' in df.columns and 'Valor_Pedido_BRL' in df.columns:
            b2b_comparison = df.groupby('Venda_B2B')['Valor_Pedido_BRL'].agg(['mean', 'std', 'count']).reset_index()
            b2b_comparison['Tipo'] = b2b_comparison['Venda_B2B'].map({True: 'B2B', False: 'B2C'})
            
            fig_b2b = px.bar(
                b2b_comparison,
                x='Tipo',
                y='mean',
                error_y='std',
                title='Valor Médio de Pedidos: B2B vs B2C',
                labels={'mean': 'Valor Médio (BRL)', 'std': 'Desvio Padrão'},
                template=plotly_template,
                color='Tipo',
                color_discrete_map={'B2B': '#00e5ff', 'B2C': '#ff8c00'}
            )
            fig_b2b.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_b2b, use_container_width=True)
        
        # Análise estatística avançada
        st.markdown('<h2 class="section-header">3. Intervalos de Confiança e Testes de Hipótese</h2>', unsafe_allow_html=True)
        
        if len(valores_limpos) > 0:
            st.markdown('<h3>3.1 Intervalo de Confiança para Valor Médio de Pedidos</h3>', unsafe_allow_html=True)
            
            n = len(valores_limpos)
            mean_val = valores_limpos.mean()
            ic_lower, ic_upper = confidence_interval(valores_limpos, 0.95)
            
            st.write(f"""
            **Justificativa para Intervalo de Confiança:**
            Utilizamos um intervalo de confiança de 95% para a média dos valores de pedidos, pois:
            - Temos uma amostra grande (n = {n:,})
            - A distribuição é aproximadamente normal (pelo Teorema Central do Limite)
            - Queremos estimar o valor médio populacional com 95% de confiança
            """)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Limite Inferior", f"R$ {ic_lower:.2f}")
            
            with col2:
                st.metric("Média Amostral", f"R$ {mean_val:.2f}")
            
            with col3:
                st.metric("Limite Superior", f"R$ {ic_upper:.2f}")
            
            st.write(f"""
            **Interpretação:** Com 95% de confiança, o valor médio populacional dos pedidos está entre 
            R$ {ic_lower:.2f} e R$ {ic_upper:.2f}.
            """)
        
        # Teste de hipótese: B2B vs B2C
        if 'Venda_B2B' in df.columns and 'Valor_Pedido_BRL' in df.columns:
            st.markdown('<h3>3.2 Teste de Hipótese: Diferença entre Vendas B2B e B2C</h3>', unsafe_allow_html=True)
            
            b2b_values = df[df['Venda_B2B'] == True]['Valor_Pedido_BRL'].dropna()
            b2c_values = df[df['Venda_B2B'] == False]['Valor_Pedido_BRL'].dropna()
            
            if len(b2b_values) > 0 and len(b2c_values) > 0:
                st.write(f"""
                **Hipóteses:**
                - H₀: μ_B2B = μ_B2C (não há diferença entre as médias)
                - H₁: μ_B2B ≠ μ_B2C (há diferença entre as médias)
                
                **Justificativa do Teste:**
                Utilizamos o teste t de Student para duas amostras independentes porque:
                - Queremos comparar as médias de dois grupos independentes
                - As amostras são grandes (B2B: {len(b2b_values):,}, B2C: {len(b2c_values):,})
                - Assumimos distribuições aproximadamente normais
                """)
                
                t_stat, p_value = t_test_independent(b2b_values, b2c_values)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Estatística t", f"{t_stat:.4f}")
                
                with col2:
                    st.metric("p-valor (aprox.)", f"{p_value:.3f}")
                
                with col3:
                    st.metric("Média B2B", f"R$ {b2b_values.mean():.2f}")
                
                with col4:
                    st.metric("Média B2C", f"R$ {b2c_values.mean():.2f}")
                
                alpha = 0.05
                if p_value < alpha:
                    resultado = "Rejeitamos H₀"
                    interpretacao = "Há evidência estatística significativa de diferença entre as médias dos grupos B2B e B2C."
                else:
                    resultado = "Não rejeitamos H₀"
                    interpretacao = "Não há evidência estatística suficiente para afirmar que existe diferença entre as médias dos grupos B2B e B2C."
                
                st.write(f"""
                **Resultado:** {resultado} (α = 0.05)
                
                **Interpretação:** {interpretacao}
                
                **Conclusão Prática:** {"As vendas B2B apresentam valor médio significativamente diferente das vendas B2C, " +
                 "sugerindo estratégias de precificação distintas para cada segmento." if p_value < alpha else
                 "Não há diferença estatisticamente significativa entre os valores médios de pedidos B2B e B2C, " +
                 "indicando que ambos os segmentos têm comportamento similar de compra."}
                """)
                
                fig_comparison = go.Figure()
                
                fig_comparison.add_trace(go.Histogram(
                    x=b2b_values, name='B2B', opacity=0.7, nbinsx=30, marker_color='#00e5ff'
                ))
                
                fig_comparison.add_trace(go.Histogram(
                    x=b2c_values, name='B2C', opacity=0.7, nbinsx=30, marker_color='#ff8c00'
                ))
                
                fig_comparison.update_layout(
                    title='Distribuição dos Valores de Pedidos: B2B vs B2C',
                    xaxis_title='Valor do Pedido (BRL)',
                    yaxis_title='Frequência',
                    barmode='overlay',
                    height=400,
                    template=plotly_template,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Teste adicional: Correlação entre Quantidade e Valor
        if 'Qty' in df.columns and 'Valor_Pedido_BRL' in df.columns:
            st.markdown('<h3>3.3 Análise de Correlação: Quantidade vs Valor do Pedido</h3>', unsafe_allow_html=True)
            
            corr_data = df[['Qty', 'Valor_Pedido_BRL']].dropna()
            
            if len(corr_data) > 1:
                correlation_coef = np.corrcoef(corr_data['Qty'], corr_data['Valor_Pedido_BRL'])[0, 1]
                
                st.write(f"""
                **Análise de Correlação de Pearson:**
                - H₀: ρ = 0 (não há correlação linear)
                - H₁: ρ ≠ 0 (há correlação linear)
                """)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Coeficiente de Correlação", f"{correlation_coef:.4f}")
                
                with col2:
                    if abs(correlation_coef) > 0.5:
                        significancia = "Significativa"
                    else:
                        significancia = "Não significativa"
                    st.metric("Interpretação", significancia)
                
                if abs(correlation_coef) < 0.3:
                    forca = "fraca"
                elif abs(correlation_coef) < 0.7:
                    forca = "moderada"
                else:
                    forca = "forte"
                
                direcao = "positiva" if correlation_coef > 0 else "negativa"
                
                st.write(f"""
                **Interpretação:** Existe uma correlação {forca} {direcao} (r = {correlation_coef:.4f}) entre a quantidade 
                de itens e o valor do pedido.
                """)
                
                sample_size = min(5000, len(corr_data))
                sample_data = corr_data.sample(n=sample_size)
                
                fig_scatter = px.scatter(
                    sample_data,
                    x='Qty',
                    y='Valor_Pedido_BRL',
                    title=f'Correlação entre Quantidade e Valor do Pedido (r = {correlation_coef:.3f})',
                    labels={'Qty': 'Quantidade de Itens', 'Valor_Pedido_BRL': 'Valor do Pedido (BRL)'},
                    trendline='ols',
                    template=plotly_template,
                    color_discrete_sequence=['#00e5ff']
                )
                fig_scatter.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_scatter, use_container_width=True)
    
    else:
        st.error("Não foi possível carregar os dados. Verifique se o arquivo 'df_selecionado.xlsx' está disponível.")

# Rodapé
st.markdown("---")
st.markdown("""
<div class='footer'>
    <p>Dashboard desenvolvido com Streamlit | © 2024 - Análise de Dados Profissional</p>
</div>
""", unsafe_allow_html=True)