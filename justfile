genmodele *MODEL_NAME:
    uv run src/utils/scripts/gen_by_templates/cli.py {{MODEL_NAME}}

alias gm := genmodele

geninits *PATH_MODULE:
    uv run src/utils/scripts/gen_inits/cli.py {{PATH_MODULE}}

alias gi := geninits

coverage:
    coverage run --source=src --omit="tests/system/load/*" -m pytest tests/system
    coverage report
    coverage html

SERVICE := "http://localhost:8000"

locust:
    @curl -s {{SERVICE}} > /dev/null 2>&1 \
      || (python -m src.main > /dev/null 2>&1 & PB_SERVICE_PID=$!; echo "Service not founded. Execute"; sleep 3)
    locust -f tests/system/load/post_events/locustfile.py --host={{SERVICE}}