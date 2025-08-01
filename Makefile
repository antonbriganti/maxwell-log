create-post:
	./scripts/create-new-entry.sh

clean:
	rm -rf dist/*

render:
	$(MAKE) clean
	cp -r public/* dist/
	./scripts/not-hugo

deploy:
	$(MAKE) render
	./scripts/deploy.sh

local-server:
	$(MAKE) render
	docker compose up

word-count:
	find md -name "*.md" -type f -exec python3 scripts/word-counter.py {} \; | sort

update-not-hugo:
	git clone https://github.com/antonbriganti/not-hugo.git
	cd not-hugo && go build
	mv ./not-hugo/not-hugo ./scripts/
	cd ..
	rm -rf not-hugo/