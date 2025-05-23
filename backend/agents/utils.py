# backend/agents/utils.py
"""
Funções utilitárias para:
1. Transformar o bloco ```json ... ``` em dicionário Python.
2. Gerar um slug seguro para nomear pastas/arquivos.
3. Salvar os arquivos da landing em output/<slug>/...
4. Compactar a pasta gerada em um .zip.
"""

import json
import os
import shutil
import zipfile
from pathlib import Path



# slugify seguro (usa python-slugify se existir — pip install python-slugify)
try:
    from slugify import slugify as _slugify
except ImportError:
    import re
    def _slugify(text: str) -> str:
        text = re.sub(r"[^\w\s-]", "", text).strip().lower()
        return re.sub(r"[-\s]+", "-", text)


# --------------------------------------------------------------------------------------
# 1) Parse do bloco raw
# --------------------------------------------------------------------------------------
def parse_raw_json(raw_block: str) -> dict:
    """
    Recebe uma string que normalmente vem assim:

        ```json
        { ... }
        ```

    Remove as cercas ``` e devolve json.loads(dict).
    """
    raw = raw_block.strip()

    # remove cercas ```json ... ``` ou ``` ...
    if raw.startswith("```"):
        raw = raw.split("```json", 1)[-1] if "```json" in raw else raw[3:]
        raw = raw.rsplit("```", 1)[0]

    return json.loads(raw)


# --------------------------------------------------------------------------------------
# 2) Slug
# --------------------------------------------------------------------------------------
def slugify_title(title: str, fallback: str = "landing") -> str:
    """
    Transforma o título em um slug seguro para pasta/arquivo.
    Se o resultado ficar vazio, usa fallback.
    """
    slug = _slugify(title)
    return slug or fallback


# --------------------------------------------------------------------------------------
# 3) Salvar arquivos
# --------------------------------------------------------------------------------------
def save_landing_files(slug: str, files: dict) -> Path:
    """
    files = {
        "index.html": "<html>...</html>",
        "css/style.css": "...",
        "js/script.js": "..."
    }

    Cria a estrutura em output/<slug>/…  e devolve o Path da pasta.
    """
    base_dir = Path("output") / slug
    for rel_path, content in files.items():
        dest = base_dir / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content.lstrip("\n"), encoding="utf-8")

    return base_dir


# --------------------------------------------------------------------------------------
# 4) Zip
# --------------------------------------------------------------------------------------
def zip_folder(folder: Path) -> Path:
    """
    Compacta a pasta <folder> para <folder>.zip (no mesmo nível)
    e retorna o Path do .zip.
    """
    zip_path = folder.with_suffix(".zip")

    # remove zip antigo se existir
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in folder.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(folder.parent))

    return zip_path
