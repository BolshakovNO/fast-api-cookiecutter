SHELL = /bin/bash

# TESTS
build_test:
	docker-compose -f docker-compose.yml -f docker-compose.test.yml build test_api

test: build_test
	docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d db
	docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm test_api sh /app/scripts/migrate_db.sh
	docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm test_api
	docker-compose -f docker-compose.yml -f docker-compose.test.yml down

# RUN
build:
	docker-compose -f docker-compose.yml build

run:
	docker-compose -f docker-compose.yml up