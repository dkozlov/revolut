FOLDERS   := db server

.PHONY: build test push

all: build test push

	@echo "$@ finished!"

build:

	@echo "Build has started..."

	for FOLDER in ${FOLDERS}; do \
		echo "Build $${FOLDER} docker image..."; \
		cd $${FOLDER}; \
		make build; \
		cd ..; \
	done

	@echo "Build has finished!"

test:

	@echo "Tests has started..."

	mkdir -p tests
	for FOLDER in ${FOLDERS}; do \
		echo "Test $${FOLDER} docker image..."; \
		cd $${FOLDER}; \
		make test; \
		cp -r tests/reports ../tests/. ;\
		cd ..; \
	done

	@echo "Tests have finished!"

push:

	@echo "Push has started..."

	for FOLDER in ${FOLDERS}; do \
		echo "Push $${FOLDER} docker image..."; \
		cd $${FOLDER}; \
		make push; \
		cd ..; \
	done

	@echo "Push has finished!"
