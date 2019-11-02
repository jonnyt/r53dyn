# r53-dyn

Update AWS Route 53 A record based on current public IP.  Mostly an exercise for me to learn a little python and docker.

Requires the following environmental vars:

* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* AWS_HOSTED_ZONE_ID
* AWS_A_RECORD_NAME

## Build

```shell
docker build --rm -f "Dockerfile" -t r53-dyn:latest .

# run to watch stdout
docker run r53-dyn

# normally run detached
docker run -d r53-dyn

# hop into the container
docker exec -it [containerId] /bin/bash
```

## Push

```shell
DOCKER_ID_USER=jonathont
sudo docker login
sudo docker tag r53dyn $DOCKER_ID_USER/r53dyn
sudo docker push $DOCKER_ID_USER/r53dyn
```

## Notes on using python

* use CMD["python","-u","scriptname.py"], the -u allows us to see output
