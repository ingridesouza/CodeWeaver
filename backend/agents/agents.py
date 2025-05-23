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

__all__ = ["prompt_enhancer_agent"]
