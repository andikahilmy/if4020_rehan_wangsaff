all: run-server run-client

run-server:
	python server/main.py ${port}

run-client:
	python client/main.py ${port} ${server}

testing:
	pytest test -v

dev: testing run-server run-client