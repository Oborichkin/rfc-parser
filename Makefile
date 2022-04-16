PROJECT_NAME = RfcParser

.PHONY = test build push clean hooks

install: venv hooks examples

test: venv examples
	$(VENV)/pytest --cov=$(PROJECT_NAME) --cov-report=html --cov-report=term tests/

hooks: venv
	$(VENV)/pre-commit install

examples: data/rfc3261.txt data/rfc2119.txt data/rfc2327.txt

data/rfc3261.txt:
	curl \
		-o rfc3261.txt.fetched \
		-L "https://www.ietf.org/rfc/rfc3261.txt" 
	echo "d513777f77fea01a4de9c0a2d9d6713cb53b8231f1b7a2ab56705f8d51b066dc *rfc3261.txt.fetched" \
		| sha256sum --check - \
		&& mv rfc3261.txt.fetched data/rfc3261.txt

data/rfc2119.txt:
	curl \
		-o rfc2119.txt.fetched \
		-L "https://www.ietf.org/rfc/rfc2119.txt"
	echo "3c2ceb7bfc84cd34720f4a5271338ab9d8280d34bdd1eb250c64306202f2ed8b *rfc2119.txt.fetched" \
		| sha256sum --check - \
		&& mv rfc2119.txt.fetched data/rfc2119.txt

data/rfc2327.txt:
	curl \
		-o rfc2327.txt.fetched \
		-L "https://www.ietf.org/rfc/rfc2327.txt"
	echo "a063265b3e357e84b9b624da27846af3c6e7643483640e0e39c048218429d5ad *rfc2327.txt.fetched" \
		| sha256sum --check - \
		&& mv rfc2327.txt.fetched data/rfc2327.txt

build: venv clean
	$(VENV)/python setup.py sdist bdist_wheel

sphinx: venv
	. $(VENV)/activate && cd docs && $(MAKE) html

clean:
	rm -rf build dist *.egg-info

include Makefile.venv
Makefile.venv:
	curl \
		-o Makefile.fetched \
		-L "https://github.com/sio/Makefile.venv/raw/v2020.08.14/Makefile.venv"
	echo "5afbcf51a82f629cd65ff23185acde90ebe4dec889ef80bbdc12562fbd0b2611 *Makefile.fetched" \
		| sha256sum --check - \
		&& mv Makefile.fetched Makefile.venv
