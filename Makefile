PROJECT_ROOT:=.
# Define different requirements files.
PIP_REQUIREMENTS_DIR=$(PROJECT_ROOT)/requirements
PIP_REQUIREMENTS_STYLE:=$(PIP_REQUIREMENTS_DIR)/codestyle.txt
PIP_REQUIREMENTS_DEV:=$(PIP_REQUIREMENTS_DIR)/dev.txt
PIP_REQUIREMENTS_DOC:=$(PIP_REQUIREMENTS_DIR)/documentation.txt

# Inner-dependencies / includes.
$(PIP_REQUIREMENTS_STYLE): $(PIP_REQUIREMENTS_DEV)
$(PIP_REQUIREMENTS_DOC): $(PIP_REQUIREMENTS_DEV)

PIP_REQUIREMENTS_ALL:=$(PIP_REQUIREMENTS_STYLE) $(PIP_REQUIREMENTS_DEV) $(PIP_REQUIREMENTS_DOC)
requirements: $(PIP_REQUIREMENTS_ALL)
requirements_rebuild:
	$(RM) $(PIP_REQUIREMENTS_ALL)
	$(MAKE) requirements

# Compile/build requirements.txt files from .in files, using pip-compile.
$(PIP_REQUIREMENTS_DIR)/%.txt: $(PIP_REQUIREMENTS_DIR)/%.in
	pip-compile $< > $@

.PHONY: requirements requirements_rebuild
