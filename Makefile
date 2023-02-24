.PHONY: grafana
grafana:
	docker compose up -d

clean:
	docker compose down --volumes

