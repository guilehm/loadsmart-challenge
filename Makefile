test:
	flake8
	isort .
	py.test -v
