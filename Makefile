BUMP_PART?=patch

install:
	python3 -m pip install .
	plz install

lint:
	flake8 plz/ tests/
	mypy plz/ tests/

format:
	isort plz/ tests/
	black plz/ tests/

test:
	pytest -svv tests/ -n auto

build:
	rm -rf dist/
	python setup.py sdist bdist_wheel
	rm -rf build/

publish: build
	twine upload dist/* --verbose

bump:
	bumpversion $(BUMP_PART)