
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

1) 
cd flask-logrocket/flask_docker
docker image build -t flask_docker .
docker run -p 5000:5000 -d flask_docker

then open the browser - mine fails

cd flask-logrocket/_docker
 -- I ran all of these:
docker-compose up -d --build
docker-compose up -d --build --remove-orphans
docker-compose up -d
docker ps



