from crewai import Task

from .agents import (
    prompt_enhancer_agent,
    scrum_master_agent,
    frontend_dev_agent,
    backend_dev_agent,
    tester_agent,
    qa_agent,
)

# 1) Enhance the original user prompt
enhance_prompt_task = Task(
    description="Melhore o prompt fornecido pelo usuário.",
    agent=prompt_enhancer_agent,
    expected_output="Prompt aprimorado ou JSON com detalhes da aplicação.",
)

# 2) Plan technical tasks
plan_tasks_task = Task(
    description="Analise o prompt aprimorado e defina as tarefas de frontend e backend em JSON.",
    agent=scrum_master_agent,
    expected_output="JSON com frontend_task e backend_task",
)

# 3) Frontend implementation
frontend_task = Task(
    description="Implemente a parte de frontend conforme indicado.",
    agent=frontend_dev_agent,
    expected_output="Bloco de arquivos com HTML, CSS e JS",
)

# 4) Backend implementation
backend_task = Task(
    description="Implemente a API ou lógica backend solicitada.",
    agent=backend_dev_agent,
    expected_output="Trechos de código backend",
)

# 5) Test the integrated result
tester_task = Task(
    description="Teste o frontend e backend integrados e reporte problemas.",
    agent=tester_agent,
    expected_output="APPROVED ou lista de bugs",
)

# 6) Final QA validation
qa_task = Task(
    description="Avalie a qualidade final do projeto e aprove ou dê feedback.",
    agent=qa_agent,
    expected_output="APPROVED ou feedback",
)

__all__ = [
    "enhance_prompt_task",
    "plan_tasks_task",
    "frontend_task",
    "backend_task",
    "tester_task",
    "qa_task",
]
