# agents/tasks.py
from crewai import Task

from .agents import prompt_enhancer_agent

from agents.agents import prompt_enhancer_agent
from agents.generator import html_generator_agent
from agents.utils import parse_raw_json, save_landing_files, zip_folder, slugify_title


# Tarefa: aprimorar o prompt fornecido pelo usuário
enhance_prompt_task = Task(
    description=(
        "Melhore o prompt fornecido pelo usuário para ser usado na geração de uma landing page. "
        "Você deve adicionar detalhes como público-alvo, cores sugeridas, estrutura da página, "
        "tipo de conteúdo (texto, imagem, botão), tecnologias preferidas (HTML, CSS, JS Vanilla) "
        "e qualquer outro elemento relevante. "
        "Retorne a resposta em formato JSON para facilitar o uso por outros agentes."
    ),
    agent=prompt_enhancer_agent,
    expected_output=(
        "Um JSON bem formatado com as instruções completas e detalhadas da landing page."
    )
)

# Task 2: gerar código
generate_code_task = Task(
    description=(
        "Receba o briefing JSON e gere index.html, css/style.css, js/script.js "
        "conforme as instruções."
    ),
    agent=html_generator_agent,
    expected_output="Bloco ```files ...``` com os três arquivos.",
)

# Exporta a task para ser utilizada na crew
__all__ = ["enhance_prompt_task", "generate_code_task"]