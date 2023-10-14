 docker build -t script-container .

 docker run -it -v "$(pwd)":/app script-container


 //server 
 docker build -t script-container .
docker run -it -p 5000:5000 -v "$(pwd)":/app script-container
