To build the image and run it follow the steps below:
  1. Download or pull the files from the current repository into a folder on your machine
  2. make sure you have the docker engine running by using "docker --version" command
  3. in the same folder where you have the Dockerfile and docker-compose.yaml run "docker build -t <name of the app>" .
  4. verify the image by running "docker images" and see that your image is there
  5. modify the docker-compose.yaml file to use the image you have build by editing the "image:" line and adding your built image.
