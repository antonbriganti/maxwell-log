render:
	cp style.css dist/
	cp -r images/ dist/
	./scripts/not-hugo

create:
	./scripts/create-new-entry.sh

deploy:
	$(MAKE) render
	./scripts/deploy.sh

local-server:
	$(MAKE) render
	docker compose up