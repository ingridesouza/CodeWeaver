# agents/agents.py

import os
from crewai import Agent
from langchain.llms import OpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do modelo DeepSeek (compatível com API da OpenAI)
llm = OpenAI(
    model_name="deepseek-chat",
    temperature=0.5,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE")
)

# Template para o agente aprimorador de prompt
prompt_enhancer_template = PromptTemplate(
    input_variables=["prompt"],
    template="""
Você é um engenheiro de prompt experiente. O usuário forneceu este pedido:
"{prompt}"

Melhore esse prompt detalhando as seguintes informações, caso estejam ausentes:
- Paleta de cores desejada (sugira se não for especificada)
- Seções principais da landing page
- Público-alvo
- Tipo de conteúdo a ser exibido (texto, imagens, CTA)
- Frameworks ou tecnologias preferidas (HTML, CSS, JS Vanilla)

Retorne a versão aprimorada do prompt no formato JSON.
"""
)

# Definição do agente
prompt_enhancer_agent = Agent(
    role="Aprimorador de Prompt",
    goal="Refinar o pedido do usuário para gerar uma landing page com qualidade",
    backstory="Especialista em identificar e preencher lacunas em instruções vagas.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    prompt_template=prompt_enhancer_template
)

# Exporta o agente para uso em outros arquivos
__all__ = ["prompt_enhancer_agent"]
