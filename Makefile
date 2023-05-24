.PHONY: cli
test:
	@docker compose exec api python -m app.cli.main healthcheck

.PHONY: test
test:
	@docker compose exec api python -m pytest

# モジュールをインストールする
.PHONY: install
install:
	rm dist/autonomous-api-1.0.tar.gz
	@docker compose exec -w /var/www api python setup.py sdist
	@pip install dist/autonomous-api-1.0.tar.gz
