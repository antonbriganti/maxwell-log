update-not-hugo:
	git clone https://github.com/antonbriganti/not-hugo.git
	cd not-hugo && go build
	mv ./not-hugo/not-hugo ./scripts/
	cd ..
	rm -rf not-hugo/

render:
	$(MAKE) clean
	cp style.css dist/
	cp -r images/ dist/
	./scripts/not-hugo

create:
	./scripts/create-new-entry.sh

clean:
	rm -rf dist/*

deploy:
	$(MAKE) render
	./scripts/deploy.sh

local-server:
	$(MAKE) render
	docker compose up