

run:
	@docker compose down
	@docker compose up

run_localy:
	@docker compose down
	@docker compose up mongo rabbitmq