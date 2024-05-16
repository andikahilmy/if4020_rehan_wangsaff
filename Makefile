run-server:
	uvicorn server.main:app --reload

run-client:
	python client/main.py

testing:
	pytest test