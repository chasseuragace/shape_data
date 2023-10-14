 docker build -t script-container .

 docker run -it -v "$(pwd)":/app script-container