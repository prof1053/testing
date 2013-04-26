# -*- makefile -*-

# definitions
PROJECT       = testing
HOST          = 127.0.0.1
PORT          = 8000


PROJECT_TEST_TARGETS=core

# constants
PYTHONPATH = .:..
PYTHON     = python

MANAGE=cd $(PROJECT) && PYTHONPATH=$(PYTHONPATH) DJANGO_SETTINGS_MODULE=$(PROJECT).settings django-admin.py

# end

run:
	$(MAKE) clean
	$(MANAGE) runserver $(HOST):$(PORT)

syncdb:
	$(MAKE) clean
	$(MANAGE) syncdb --noinput
	$(MAKE) manage -e CMD="migrate"

fresh_syncdb:
	-rm dev.db
	$(MANAGE) syncdb --noinput
	$(MAKE) manage -e CMD="migrate"
	@echo Loading initial fixtures...
	$(MANAGE) loaddata base_initial_data.json
	@echo Done

test:
	$(MAKE) clean
	TESTING=1 $(MANAGE) test $(TEST_OPTIONS) $(PROJECT_TEST_TARGETS)

clean:
	@echo Cleaning up *.pyc files
	-find . | grep '.pyc$$' | xargs -I {} rm {}

migrate:
ifndef APP_NAME
	@echo Please, specify -e APP_NAME=appname argument
else
	@echo Starting of migration of $(APP_NAME)
	-$(MANAGE) schemamigration $(APP_NAME) --auto
	$(MANAGE) migrate $(APP_NAME)
	@echo Done
endif

manage:
ifndef CMD
	@echo Please, specify CMD argument to execute Django management command
else
	$(MANAGE)  $(CMD)
endif

shell:
	$(MAKE) clean
	$(MANAGE) shell_plus
