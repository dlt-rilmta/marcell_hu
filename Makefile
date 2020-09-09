mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))

# ----------

all: usage

# always update according to targets below :)
usage:
	@echo
	@echo "You can..."
	@echo

# ----------

venv:
	# rm -rf venv
	# python3 -m venv venv
	venv/bin/pip install Cython
	venv/bin/pip install -r requirements.txt
	for req in */requirements.txt ; do venv/bin/pip install -r $${req} ; done
.PHONY: venv

# ----------------------
# Docker related targets
# ----------------------

VERSION = $$(grep -E "__version__\s*=\s*'[^']+'" __init__.py | sed  -r "s/__version__ = '([^']+)'/\1/")

## build docker image
dbuild:
	docker build -t mtaril/marcell_hu:latest -t mtaril/marcell_hu:$(VERSION) .
.PHONY: dbuild


## build docker test image
dbuildtest:
	docker build -t mtaril/marcell_hu:test .
.PHONY: dbuildtest


## run docker container in background, without volume mapping
drun:
	@make -s dstop
	@myport=$$(./docker/freeportfinder.sh) ; \
		if [ -z "$${myport}" ] ; then echo 'ERROR: no free port' ; exit 1 ; fi ; \
		docker run --name marcell_hu -p $${myport}:5000 --rm -d mtaril/marcell_hu:latest ; \
		echo "OK: marcell_hu container run on port $${myport}" ;
.PHONY: drun


# connect marcell_hu container that is already running
dconnect:
	@if [ "$$(docker container ls -f name=marcell_hu -q)" ] ; then \
		docker exec -it marcell_hu /bin/sh ; \
	else \
		echo 'no running marcell_hu container' ; \
	fi
.PHONY: dconnect


# test the test image
dtest: # dbuildtest
	@cd tests/ && ./dtest.sh
.PHONY: dtest



## stop running marcell_hu container
dstop:
	@if [ "$$(docker container ls -f name=marcell_hu -q)" ] ; then \
		docker container stop marcell_hu ; \
	else \
		echo 'no running marcell_hu container' ; \
	fi
.PHONY: dstop


## show images and containers
dls:
	@echo 'IMAGES:'
	@docker image ls
	@echo
	@echo 'CONTAINERS:'
	@docker container ls
.PHONY: dls


## delete unnecessary containers and images
dclean:
	@docker container prune -f
	@docker image prune -f
.PHONY: dclean
