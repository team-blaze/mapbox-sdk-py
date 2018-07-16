FILENAME  	   = dist/$(shell ls dist/)

setup:
	rm -Rf virtualenv
	virtualenv virtualenv
	./virtualenv/bin/pip install -r requirements.txt

build:
	rm -Rf dist
	python setup.py sdist

publish:
	echo "Publishing to Gemfury:" $(FILENAME)
	curl -F package=@$(FILENAME) https://4xJNWRhcwpzS9pAg4ay6@push.fury.io/blazedevices/
