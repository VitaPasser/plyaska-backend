genmodele MODEL_NAME:
    uv run src/utils/scripts/gen_by_templates/cli.py {{MODEL_NAME}}

alias gm := genmodele

geninits PATH_MODULE:
    uv run src/utils/scripts/gen_inits/cli.py {{PATH_MODULE}}

alias gi := geninits