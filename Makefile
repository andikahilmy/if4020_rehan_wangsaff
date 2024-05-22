all: run-server run-client

run-server:
	uvicorn server.main:app --port ${port} --reload

run-client:
	python client/main.py ${port} ${server}

testing:
	pytest test -v

dev: testing run-server run-client