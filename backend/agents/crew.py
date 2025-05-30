"""Orquestração das tarefas dos agentes."""
from __future__ import annotations
import datetime
from crewai import Crew

from agents.tasks import (
    enhance_prompt_task,
    plan_tasks_task,
    frontend_task,
    backend_task,
    tester_task,
    qa_task,
)
from agents.utils import (
    parse_raw_json,
    slugify_title,
    save_landing_files,
    zip_folder,
)

# ---------------------------------------------------------------------------
# Instância da Crew com todas as tarefas
# ---------------------------------------------------------------------------
crew = Crew(
    tasks=[
        enhance_prompt_task,  # 0
        plan_tasks_task,      # 1
        frontend_task,        # 2
        backend_task,         # 3
        tester_task,          # 4
        qa_task,              # 5
    ],
    verbose=True,
)


def _run_crewai_flow(prompt: str, feedback: str | None = None):
    """Executa a crew e devolve as saídas brutas de cada tarefa."""
    payload = {"prompt": prompt}
    if feedback:
        payload["feedback"] = feedback

    try:
        out = crew.execute(payload)
        outputs = [t.raw for t in out.tasks_output]
        token_usage = dict(out.token_usage) if hasattr(out, "token_usage") else {}
    except AttributeError:
        out_list = crew.kickoff(inputs=payload)
        outputs = [step["raw"] for step in out_list]
        token_usage = {}
    return outputs, token_usage


def run_crew(user_prompt: str, max_retries: int = 1) -> dict:
    """Roda o fluxo completo com pequena lógica de retry se o QA reprovar."""
    feedback = None
    attempts = 0
    outputs = []
    token_usage = {}
    while attempts <= max_retries:
        outputs, token_usage = _run_crewai_flow(user_prompt, feedback)
        qa_output = outputs[5]
        if "APPROVED" in qa_output.upper():
            break
        feedback = qa_output
        attempts += 1

    # Parse briefing and gerar zip com arquivos do frontend
    raw_briefing = outputs[0]
    files_block = outputs[2]

    briefing = parse_raw_json(raw_briefing)
    objective = briefing.get("landing_page_specs", {}).get("objective", "project")
    slug = slugify_title(objective)

    # converter bloco ```files``` em dict
    files = {}
    current = None
    for line in files_block.splitlines():
        if line.startswith("```"):
            continue
        if line.endswith((".html", ".css", ".js")):
            current = line.strip()
            files[current] = ""
        elif current:
            files[current] += line + "\n"

    project_dir = save_landing_files(slug, files)
    zip_path = zip_folder(project_dir)

    return {
        "briefing": briefing,
        "project_dir": str(project_dir),
        "zip_path": str(zip_path),
        "qa_output": qa_output,
        "token_usage": token_usage,
        "attempts": attempts + 1,
        "timestamp": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
