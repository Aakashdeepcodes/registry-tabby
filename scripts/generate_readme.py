import json
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from datetime import datetime, timedelta

try:
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader("."))
    try:
        template = env.get_template("meta/README.tmpl.md")
    except TemplateNotFound:
        print("Error: Template file 'meta/README.tmpl.md' not found.")
        exit(1)

    # Load models.json
    with open("models.json", "r") as f:
        models = json.load(f)

    # Categorize models
    completion_models = [x for x in models if 'prompt_template' in x]
    chat_models = [x for x in models if 'chat_template' in x]
    embedding_models = [x for x in models if not ('chat_template' in x or 'prompt_template' in x)]

    # Render template
    rendered_template = template.render(
        completion_models=completion_models,
        chat_models=chat_models,
        embedding_models=embedding_models
    )

    # Write to README.md
    with open("README.md", "w") as f:
        f.write(rendered_template)
    
    print("README.md successfully generated.")

except FileNotFoundError:
    print("Error: 'models.json' not found. Ensure the file exists in the current directory.")
except json.JSONDecodeError:
    print("Error: Failed to decode JSON. Check 'models.json' for syntax errors.")
except Exception as e:
    print(f"Unexpected error: {e}")
