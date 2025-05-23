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
from datetime import datetime

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


def _run_crewai_flow(user_prompt: str):
    """
    Tenta executar com .execute(); se não existir, usa .kickoff().
    Devolve:
        - raw_json (saída da task 0)
        - files_block (saída da task 1)
        - token_usage (dict ou {})
    """
    try:
        # nova API (>= 0.12)
        out = crew.execute({"prompt": user_prompt})
        raw_json    = out.tasks_output[0].raw
        files_block = out.tasks_output[1].raw
        token_usage = dict(out.token_usage) if hasattr(out, "token_usage") else {}
    except AttributeError:
        # caiu aqui? então estamos na API antiga (<= 0.11)
        out_list = crew.kickoff(inputs={"prompt": user_prompt})
        raw_json    = out_list[0]["raw"]
        files_block = out_list[1]["raw"]
        token_usage = {}          # não disponível nessa versão
    return raw_json, files_block, token_usage

# ------------------------------------------------------------------------------
# Função chamada pela API
# ------------------------------------------------------------------------------
def run_crew(user_prompt: str) -> dict:
    """Executa a crew de ponta a ponta e devolve dados prontos p/ API."""
    # 1) roda as tasks (independente da versão)
    raw_json, files_block, token_usage = _run_crewai_flow(user_prompt)

    # 2) briefing -----------------------------------------------------
    briefing = parse_raw_json(raw_json)
    objective = briefing.get("landing_page_specs", {}).get("objective", "landing-page")
    slug      = slugify_title(objective)

    # 3) converte bloco ```files``` em dict ---------------------------
    files: dict[str, str] = {}
    current = None
    for line in files_block.splitlines():
        if line.startswith("```"):
            continue
        if line.endswith((".html", ".css", ".js")):
            current = line.strip()
            files[current] = ""
        elif current:
            files[current] += line + "\n"

    # 4) salva + zip --------------------------------------------------
    project_dir = save_landing_files(slug, files)
    zip_path    = zip_folder(project_dir)

    # 5) resposta final ----------------------------------------------
    return {
        "briefing":    briefing,
        "project_dir": str(project_dir),
        "zip_path":    str(zip_path),
        "timestamp":   datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "token_usage": token_usage,
    }