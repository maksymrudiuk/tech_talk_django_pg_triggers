PROJECT=tech_talk_django_pg_triggers
COMPOSE=docker-compose.yml

ifeq (shell, $(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(lastword $(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

.PHONY: setup
setup: export DOCKER_BUILDKIT := 1
setup: export COMPOSE_DOCKER_CLI_BUILD=1

.PHONY: up
up: setup
	@docker compose -f $(COMPOSE) -p $(PROJECT) up -d

.PHONY: stop
stop:
	@docker compose -f $(COMPOSE) -p $(PROJECT) stop

.PHONY: rebuild
rebuild: setup
	@docker compose -f $(COMPOSE) -p $(PROJECT) down
	@docker compose -f $(COMPOSE) -p $(PROJECT) pull --include-deps
	@docker compose -f $(COMPOSE) -p $(PROJECT) build

.PHONY: shell
shell:
	@docker compose -f $(COMPOSE) -p $(PROJECT) exec $(RUN_ARGS) /bin/bash