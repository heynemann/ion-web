# Makefile for Ion
SHELL := /bin/bash

# Internal variables.
file_version=0.1.0
root_dir=.
build_dir=${root_dir}/build
src_dir=${root_dir}/ion

tests_dir=${root_dir}/tests
unit_tests_dir=${tests_dir}/unit
functional_tests_dir=${tests_dir}/functional

compile_log_file=${build_dir}/compile.log
unit_log_file=${build_dir}/unit.log
functional_log_file=${build_dir}/functional.log
nocoverage=false

# orchestrator targets

prepare_build: clean

test: prepare_build compile
	@echo "Running tests..."
	@if [ "$(nocoverage)" = "true" ]; then nosetests -d -s --verbose ${tests_dir}; else nosetests -d -s --verbose --with-coverage --cover-package=ion --cover-erase --cover-inclusive ${tests_dir}; fi

all: prepare_build compile test report_success

unit: prepare_build compile run_unit report_success
functional: prepare_build compile run_functional report_success
acceptance: prepare_build compile run_acceptance report_success

clean:
	@find -name *.pyc -delete

# action targets

createdb:
	@python skink_console.py createdb

upgradedb:
	@python skink_console.py upgradedb

report_success:
	@echo "Build succeeded!"

compile:
	@echo "Compiling source code..."
	@python -m compileall ${src_dir}

run_unit: compile
	@echo "Running run_unit tests..."
	@if [ "$(nocoverage)" = "true" ]; then nosetests -d -s --verbose ${unit_tests_dir}; else nosetests -d -s --verbose --with-coverage --cover-package=ion --cover-erase --cover-inclusive ${unit_tests_dir}; fi

run_functional: compile
	@echo "Running run_functional tests..."
	@if [ "$(nocoverage)" = "true" ]; then nosetests -s --verbose ${functional_tests_dir}; else nosetests -s --verbose --with-coverage --cover-package=ion --cover-erase --cover-inclusive ${functional_tests_dir}; fi

doc:
	cd docs && make html
	firefox `pwd`/docs/build/html/index.html &

