.PHONY: all
all: help

# --------------------------------------------

.PHONY: setup
setup: ## setup project with dependencies
ifeq (,$(wildcard .init/setup))
	@(which uv > /dev/null 2>&1) || \
	(echo "ubuntu requires uv."; exit 1)
	@if [ ! -d "./scratch" ]; then \
		mkdir -p scratch; \
	fi
	mkdir .init
	touch .init/setup
	uv sync
else
	@echo "Initial setup is already complete. If you are having issues, run:"
	@echo
	@echo "make reset"
	@echo "make setup"
	@echo
endif

# --------------------------------------------

.PHONY: clean
clean: ## Remove cached files and build products
	@echo Cleaning caches and build products
	@find . -type d -name .mypy_cache -exec rm -rf {} \; -prune
	@find . -type d -name __pycache__ -exec rm -rf {} \; -prune
	@echo Cleaning complete

# --------------------------------------------

.PHONY: reset
reset: clean ## clean, then remove .venv .init
	@echo Resetting project state
	rm -rf .venv .init

# --------------------------------------------

.PHONY: upgrade
upgrade: ## upgrade development dependencies
	@echo Upgrading dependencies
	uv sync --upgrade

# --------------------------------------------

.PHONY: help
help: ## Show help
	@echo Please specify a target. Choices are:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk \
	'BEGIN {FS = ":.*?## "}; \
	{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
