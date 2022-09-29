install:
	python3 -m pip install -e .
	python3 -m pip install -r dev-requirements.in # TODO: remove this when control dev deps in plz

test:
	pytest -svv tests/