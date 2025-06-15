import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from typing import Any, Mapping

# allow dataclass based vars
from .vars import vars_to_dict

env = Environment(
    loader=FileSystemLoader(os.path.dirname(__file__)),
    trim_blocks=True,
    lstrip_blocks=True)

def get_prompt_template(template_name: str):
    """Return a Jinja2 Template object for the given prompt name.

    Parameters
    ----------
    template_name : str
        Base name of the template without extension. For example, passing
        ``"breadth"`` will load ``breadth.md`` under the same directory.

    Returns
    -------
    jinja2.Template
        Compiled Jinja2 template which can be rendered with variables.
    """
    try:
        return env.get_template(f"{template_name}.md")
    except Exception as exc:
        raise ValueError(
            f"Template '{template_name}' not found or invalid: {exc}."
        ) from exc

def apply_template(
    template_name: str,
    variables: Any | None = None
) -> str:
    """Render a prompt template with runtime variables.

    This is a thin wrapper around :pyfunc:`get_prompt_template` that also
    injects some common default variables such as ``CURRENT_TIME``.

    Examples
    --------
    >>> apply_template("breadth", ARTICLE_CHUNK="示例段落")
    '...'
    """

    if variables is not None:
        rendered_vars = vars_to_dict(variables)
    else:
        raise ValueError("No variables provided.")

    template = get_prompt_template(template_name)

    # Default variables that are always available inside prompts unless overridden
    rendered_vars.setdefault("CURRENT_TIME", datetime.now().isoformat())

    return template.render(**rendered_vars)
