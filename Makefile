# MythicMind — top-level convenience targets.
#
# The two lenses are independent; each target maps to a command verified to run
# on the reference environment (Python 3.11, .NET SDK 9.0.101).

PY       ?= python
DOTNET   ?= dotnet
FIXTURES  = examples/fixtures
ENCOUNTERS = examples/encounters

.PHONY: all py py-json dotnet dotnet-run replay clean help

help:
	@echo "MythicMind targets:"
