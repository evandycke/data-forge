from __future__ import annotations

import json

from scripts.bootstrap_source_db import bootstrap_source_db
from pipelines.runners import run_all_pipelines


def main() -> None:
    bootstrap_source_db()
    result = run_all_pipelines()
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
