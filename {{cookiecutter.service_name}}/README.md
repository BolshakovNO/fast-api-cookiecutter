# Issues
- [ ] Ansible deploy

# Service template

```commandline
python -m pip install cookiecutter
python -m cookiecutter ../$SERVICE_NAME
```

# Tests

```commandline
python3 -m venv venv
. venv/bin/activate

export $(cat .env | grep -v "#" | xargs)
docker-compose up -d "${SERVICE_NAME}_db}"
./scripts/migrate_db.sh

python -m pytest tests
```