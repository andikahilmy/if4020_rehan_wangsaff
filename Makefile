all: run-server run-client

run-server:
	uvicorn server.main:app --reload

run-client:
	python client/main.py

testing:
	pytest test -v

dev: testing run-server run-client