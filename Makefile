all: run-server run-client

run-server:
	uvicorn server.main:app --port ${port} --reload --ws-ping-timeout 3600

run-client:
	python client/main.py ${server}

testing:
	pytest test -v

dev: testing run-server run-client

clean:
	rm -rf keys/*