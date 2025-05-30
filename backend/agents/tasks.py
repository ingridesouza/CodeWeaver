# agents/tasks.py
# ele define a tarefa que conecta o prompt com esse agente.

from crewai import Task
from .agents import prompt_enhancer_agent

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

# Exporta a task para ser utilizada na crew
__all__ = ["enhance_prompt_task"]
