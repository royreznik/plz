install:
	python3 -m pip install -e .
	python3 -m pip install -r dev-requirements.in # TODO: remove this when control dev deps in plz

lint:
	flake8 plz/ tests/

format:
	isort plz/ tests/
	black plz/ tests/

test:
	pytest -svv tests/