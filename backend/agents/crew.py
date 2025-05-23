# backend/agents/crew.py
"""
Orquestra a execução completa da crew:

1. enhance_prompt_task  → gera o briefing JSON (raw).
2. generate_code_task   → devolve bloco ```files``` com index.html, css, js.

Depois:
- Converte o JSON bruto em dict.
- Salva os arquivos em output/<slug>/...
- Gera .zip
- Devolve um dicionário simples para a view.
"""

from __future__ import annotations

from pathlib import Path
import datetime as dt

from crewai import Crew

# Tasks
from agents.tasks import enhance_prompt_task, generate_code_task

# Utils
from agents.utils import (
    parse_raw_json,
    slugify_title,
    save_landing_files,
    zip_folder,
)

# ------------------------------------------------------------------------------
# Instância única da crew – pode ser importada por toda a aplicação
# ------------------------------------------------------------------------------
crew = Crew(
    tasks=[
        enhance_prompt_task,   # task index 0
        generate_code_task,    # task index 1
    ],
    verbose=True,
)

# ------------------------------------------------------------------------------
# Função chamada pela API
# ------------------------------------------------------------------------------
def run_crew(user_prompt: str) -> dict:
    """
    Executa a crew e devolve um dicionário serializável por JSON.

    Retorno:
    {
        "briefing": {...},                    # dict do prompt refinado
        "project_dir": "backend/output/...",  # pasta com os arquivos
        "zip_path":    "backend/output/....zip",
        "timestamp":   "2025-05-23T14:30:05Z",
        "token_usage": { ... }
    }
    """
    # 1) Executa as duas tasks
    output = crew.execute({"prompt": user_prompt})  # CrewOutput

    # ------------------------------------------------------------------ #
    # 2) BRIEFING (Task 0)
    # ------------------------------------------------------------------ #
    raw_json = output.tasks_output[0].raw
    briefing = parse_raw_json(raw_json)

    # Usa o campo objective se existir para criar o slug
    objective = (
        briefing.get("landing_page_specs", {})
        .get("objective", "landing-page")
    )
    slug = slugify_title(objective)

    # ------------------------------------------------------------------ #
    # 3) BLOCO ```files``` (Task 1)  → dict {path: content}
    # ------------------------------------------------------------------ #
    files_block = output.tasks_output[1].raw
    files_dict: dict[str, str] = {}
    current_file = None

    for line in files_block.splitlines():
        if line.startswith("```files") or line.startswith("```"):
            continue
        if line.strip() == "```":
            # fecha bloco, ignore
            continue
        if line.endswith(".html") or line.endswith(".css") or line.endswith(".js"):
            # linha com nome do arquivo
            current_file = line.strip()
            files_dict[current_file] = ""
            continue
        if current_file:
            files_dict[current_file] += line + "\n"

    # ------------------------------------------------------------------ #
    # 4) SALVAR + ZIP
    # ------------------------------------------------------------------ #
    project_dir: Path = save_landing_files(slug, files_dict)
    zip_path:    Path = zip_folder(project_dir)

    # ------------------------------------------------------------------ #
    # 5) Pacote final para a view
    # ------------------------------------------------------------------ #
    return {
        "briefing": briefing,
        "project_dir": str(project_dir),
        "zip_path": str(zip_path),
        "timestamp": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "token_usage": dict(output.token_usage),
    }
