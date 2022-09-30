BUMP_PART?=patch

install:
	python3 -m pip install -e .
	python3 -m pip install -r dev-requirements.in # TODO: remove this when control dev deps in plz

lint:
	flake8 plz/ tests/
	mypy plz/ tests/

format:
	isort plz/ tests/
	black plz/ tests/

test:
	pytest -svv tests/

build:
	rm -rf dist/
	python setup.py sdist bdist_wheel
	rm -rf build/

publish: build
	twine upload dist/* --verbose

bump:
	bumpversion $(BUMP_PART)