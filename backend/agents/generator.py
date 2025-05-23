# backend/agents/generator.py
"""
Agente que transforma o briefing JSON em três arquivos:
index.html, css/style.css e js/script.js
"""

from crewai import Agent

GEN_PROMPT = """
Você é um desenvolvedor frontend especialista em HTML5, CSS3 e JavaScript puro.
Receberá um JSON com o briefing completo de uma landing page.
Gere **três arquivos**:
1. index.html
2. css/style.css
3. js/script.js

Regras:
- Use classes semanticamente claras.
- Linke o CSS e JS no HTML.
- Inclua seções conforme 'structure'.
- Use as cores do 'color_palette'.
- Responsivo (Flexbox ou Grid).
- Sem frameworks.

Responda NO FORMATO:

```files
===== index.html =====
<conteúdo HTML>
===== css/style.css =====
<conteúdo CSS>
===== js/script.js =====
<conteúdo JS>
""".strip()

html_generator_agent = Agent(
role="Gerador de Código",
goal="Transformar o briefing JSON em arquivos HTML, CSS e JS prontos para uso.",
backstory=(
"Engenheiro de Front-End com experiência em páginas de alta conversão, "
"focado em código limpo, acessível e responsivo sem dependências externas."
),
# 👉 Basta a string com prefixo deepseek/
llm="deepseek/deepseek-chat",
prompt=GEN_PROMPT,
verbose=True,
allow_delegation=False,
)

all = ["html_generator_agent"]