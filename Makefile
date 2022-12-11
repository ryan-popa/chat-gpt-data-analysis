build:
	docker build -t chat-gpt-data-analysis .

run:
	source secrets.env && \
	echo 'App will start running on http://localhost:8501/' && \
	docker run --rm -p 8501:8501 -it -v ${PWD}:/app chat-gpt-data-analysis
