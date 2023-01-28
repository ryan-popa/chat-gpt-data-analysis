build:
	docker build -t chat-gpt-analysis .

run:
	echo 'App will start running on http://localhost:8501/' && \
	docker run --rm -p 8501:8501 --env-file=secrets.env -it -v ${PWD}:/app chat-gpt-analysis
