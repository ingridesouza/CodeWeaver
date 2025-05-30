# backend/agents/agents.py
import os
from dotenv import load_dotenv
from crewai import Agent

load_dotenv()

# Deixe a chave disponível p/ LiteLLM
os.environ["DEEPSEEK_API_KEY"] = os.getenv("DEEPSEEK_API_KEY")
if os.getenv("DEEPSEEK_API_BASE"):
    os.environ["DEEPSEEK_API_BASE"] = os.getenv("DEEPSEEK_API_BASE")

PROMPT_ENHANCER_TXT = """
Você é um engenheiro de prompt experiente.
O usuário forneceu este pedido: **{prompt}**

Melhore o pedido acrescentando:
• Paleta de cores (sugira se faltar)
• Seções principais da página
• Público-alvo
• Tipos de conteúdo (texto, imagens, CTA)
• Tecnologias preferidas (HTML, CSS, JS Vanilla)

Devolva APENAS um JSON bem formatado com todas as instruções completas.
"""

prompt_enhancer_agent = Agent(
    role="Aprimorador de Prompt",
    goal="Refinar o pedido do usuário para gerar uma landing page de alta qualidade.",
    backstory="Especialista em preencher lacunas em instruções vagas.",
    # 👉 basta a STRING com prefixo deepseek/
    llm="deepseek/deepseek-chat",
    prompt=PROMPT_ENHANCER_TXT,
    verbose=True,
    allow_delegation=False,
)

SCRUM_MASTER_TXT = """
Você é um Scrum Master. A partir de um pedido aprimorado, defina as tarefas de
frontend e backend necessárias para cumprir o objetivo. Responda em JSON com os
campos `frontend_task` e `backend_task`.
"""

FRONTEND_DEV_TXT = """
Você é um desenvolvedor Frontend experiente em HTML, CSS e JavaScript puro.
Receberá uma tarefa detalhada do Scrum Master e deverá retornar o código
necessário no formato:

```files
===== index.html =====
<conteúdo>
===== css/style.css =====
<conteúdo>
===== js/script.js =====
<conteúdo>
```
"""

BACKEND_DEV_TXT = """
Você é um desenvolvedor Backend experiente em APIs REST com Django. Receba uma
tarefa e devolva os trechos de código relevantes em formato Markdown.
"""

TESTER_TXT = """
Você é um testador de software. Integre o frontend e o backend gerados e
descreva se encontrou problemas. Responda `APPROVED` se tudo estiver correto ou
liste os bugs encontrados em JSON.
"""

QA_TXT = """
Você é do controle de qualidade. Analise o trabalho final e decida se está
pronto para entrega. Responda `APPROVED` se tudo estiver adequado ou explique os
ajustes necessários.
"""

scrum_master_agent = Agent(
    role="Scrum Master",
    goal="Dividir o pedido aprimorado em tarefas técnicas executáveis",
    backstory="Profissional de gestão ágil responsável por organizar o fluxo",
    llm="deepseek/deepseek-chat",
    prompt=SCRUM_MASTER_TXT,
    verbose=True,
    allow_delegation=False,
)

frontend_dev_agent = Agent(
    role="Desenvolvedor Frontend",
    goal="Implementar a camada de interface do usuário",
    backstory="Especialista em páginas web responsivas sem frameworks",
    llm="deepseek/deepseek-chat",
    prompt=FRONTEND_DEV_TXT,
    verbose=True,
    allow_delegation=False,
)

backend_dev_agent = Agent(
    role="Desenvolvedor Backend",
    goal="Criar a API e a lógica de servidor",
    backstory="Profissional focado em Django REST Framework",
    llm="deepseek/deepseek-chat",
    prompt=BACKEND_DEV_TXT,
    verbose=True,
    allow_delegation=False,
)

tester_agent = Agent(
    role="Testador de Software",
    goal="Garantir que frontend e backend funcionem em conjunto",
    backstory="Especialista em testes manuais e automatizados",
    llm="deepseek/deepseek-chat",
    prompt=TESTER_TXT,
    verbose=True,
    allow_delegation=False,
)

qa_agent = Agent(
    role="Analista de Qualidade",
    goal="Verificar se o produto final atende ao padrão esperado",
    backstory="Responsável pela validação final do projeto",
    llm="deepseek/deepseek-chat",
    prompt=QA_TXT,
    verbose=True,
    allow_delegation=False,
)

__all__ = [
    "prompt_enhancer_agent",
    "scrum_master_agent",
    "frontend_dev_agent",
    "backend_dev_agent",
    "tester_agent",
    "qa_agent",
]
