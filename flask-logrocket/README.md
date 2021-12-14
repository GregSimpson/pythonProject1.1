
## https://blog.logrocket.com/build-deploy-flask-app-using-docker/

to run this locally:


`cd flask-logrocket/flask_docker/app

pip install -r requirements.txt
`
then either of these work:
python hello.py
or
python view.py

Open a browser to : localhost:5000


to run in docker I have tried these things (with no luck)
##1. these cmds clean up any existing images

    * docker-compose stop  

    * docker-compose rm -f  

    * docker image prune -a -f  

    * docker network prune -f  

    * docker system prune -a -f  

    * ###-- rm all docker images  

    * docker image rm $(docker image ls -a -q)  
    
----------------------------
##2. build a new image
    * cd flask-logrocket/flask_docker
    * docker image build -t flask_docker .

----------------------------
##3a. run using the Dockerfile 
    * docker run -p 5000:5000 -d flask_docker



##3b. run using the Dockerfile  
    * cd flask-logrocket/_docker  

    * run any of these
    *  * docker-compose up -d --build
    *  * docker-compose up -d --build --remove-orphans  
    *  * docker-compose up -d

----------------------------
##4. see what is running  

docker ps  

----------------------------
##5. set the starting app  

  * start either of these in Dockerfile  

  * *  CMD ["./app/view.py" ]  

  *  * CMD ["./app/hello.py" ]

----------------------------
##6. open the browser
  *  * http://172.26.0.2:5000
  * maybe this one - depending on what was started from the Dockerfile
  * *  http://172.26.0.2:5000/about/


  
