from __future__ import annotations

from typing import Any
from jinja2 import Template


def render_markdown_report(title: str, summary_md: str, stats: dict[str, Any], models: list[str]) -> str:
    tpl = Template(
        "# {{ title }}\n\n"
        "## Executive Summary\n\n"
        "{{ summary_md }}\n\n"
        "## Scorecards (Averages)\n\n"
        "{% for crit, val in stats.criteria_avg.items() %}- {{ crit }}: {{ '%.3f'|format(val) }}\n{% endfor %}\n"
        "\n## Models Tested\n\n"
        "{% for m in models %}- {{ m }}\n{% endfor %}\n"
    )
    return tpl.render(title=title, summary_md=summary_md, stats=stats, models=models)


def render_pdf_from_html(html: str) -> bytes | None:
    try:
        from weasyprint import HTML  # type: ignore
    except Exception:
        return None
    pdf = HTML(string=html).write_pdf()
    return pdf
