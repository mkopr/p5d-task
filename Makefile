API_COMPOSE=-f ./docker-compose.yml

lint:
	@echo "Linting & fixing locally changed files"
	find . -name "*.py" | xargs black --config=pyproject.toml; \
	find . -name "*.py" | xargs flake8; \
	find . -name "*.py" | xargs mypy; \


build: #build the project
	docker-compose ${API_COMPOSE} build --no-cache

up: # starts the project
	docker-compose ${API_COMPOSE} up -d

up-b: # build and starts the project
	docker-compose ${API_COMPOSE} up -d --build

down: # stops the project
	@docker-compose ${API_COMPOSE} down

down-v: # stops the project and removes containers
	@docker-compose ${API_COMPOSE} down -v

test: # run tests
	@docker-compose ${API_COMPOSE} run web pytest -vvvv

logs: # shows logs
	docker-compose ${API_COMPOSE} logs -f --tail="100"
