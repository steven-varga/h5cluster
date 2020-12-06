# https://packaging.python.org/tutorials/packaging-projects/
.PHONY: clean clean-test clean-pyc clean-build docs help

clean: clean-pyc  ## remove all build, test, coverage and Python artifacts

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

install: clean ## install the package to the active Python's site-packages
	#python3 -m pip install --user --upgrade setuptools wheel
	#python3 setup.py sdist bdist_wheel
	python3 -m pip install .