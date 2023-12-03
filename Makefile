build:
	@echo "Building..."
	@python build.py

translate:
	@echo "Translating..."
	@python translate.py || true