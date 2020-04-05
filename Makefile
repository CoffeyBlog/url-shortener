
init:
	python -m virtualenv env

install:
	./env/Scripts/python -m pip install -r requirements.txt

run:
	./env/Scripts/python app.py
