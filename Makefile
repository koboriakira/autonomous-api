.PHONY: test
test:
	@docker compose exec api python -m pytest
