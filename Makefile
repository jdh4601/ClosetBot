SHELL := /bin/bash

API_URL ?= http://localhost:8000/api/v1
BACKEND_CONTAINER ?= fasion-backend

.PHONY: up
up:
	@docker compose up -d redis backend worker

.PHONY: wait-ready
wait-ready:
	@bash scripts/wait_ready.sh $(API_URL)/health/ready 180

.PHONY: smoke
smoke:
	@docker exec -it $(BACKEND_CONTAINER) python dev_smoke_test.py

.PHONY: submit
submit:
	@if [ -z "$(BRAND)" ] || [ -z "$(INFL)" ]; then \
		echo "Usage: make submit BRAND=<brand> INFL=<infl1,infl2,...>"; \
		exit 1; \
	fi
	@API_URL=$(API_URL) bash scripts/submit_and_poll.sh $(BRAND) $(INFL)

.PHONY: down
down:
	@docker compose down
