#onde você orquestra os agentes e tarefas com Crew() e executa a lógica central.
# agents/crew.py

from crewai import Crew
from agents.agents import prompt_enhancer_agent
from agents.tasks import enhance_prompt_task


# Cria a crew com apenas o primeiro agente por enquanto
crew = Crew(
    agents=[prompt_enhancer_agent],
    tasks=[enhance_prompt_task],
    verbose=True  # Exibe detalhes do processo no terminal
)

def run_crew(prompt: str) -> str:
    """Executa a crew com o prompt do usuário."""
    print("\n🚀 Executando CrewAI com prompt do usuário...")
    result = crew.run({"prompt": prompt})
    return result
