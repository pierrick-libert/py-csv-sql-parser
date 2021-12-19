# Makefile

all: install launch

launch:
	. env/bin/activate && python3.9 main.py

launch_dry:
	. env/bin/activate && python3.9 main.py --dry-run

clean:
	rm -rf env/

install:
	python3.9 -m venv env
	. env/bin/activate && python3.9  -m pip install --upgrade pip
	. env/bin/activate && pip install -r requirements.txt

lint:
	. env/bin/activate && pylint --fail-under 9.0 --disable=duplicate-code *.py utils/*.py

test:
	. env/bin/activate && python3.9 test.py 

greenkeeping:
	. env/bin/activate && pur -r requirements.txt

shell:
	. env/bin/activate && python3.9 manage.py shell
