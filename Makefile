.PHONY: cli
cli:
	@docker compose exec api python3 -m app.cli.cli how_to_command --command wc

.PHONY: test
test:
	@docker compose exec api python -m pytest

# モジュールをインストールする
.PHONY: install
install:
	rm dist/autonomous-api-1.0.tar.gz
	@docker compose exec -w /var/www api python setup.py sdist
	@pip install dist/autonomous-api-1.0.tar.gz
