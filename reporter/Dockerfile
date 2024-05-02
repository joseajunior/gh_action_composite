FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_BREAK_SYSTEM_PACKAGES 1

# # Updating Environement
RUN apt-get update
RUN apt-get install wget unzip curl software-properties-common -y

#Setup Python 3.12
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install python3.12 python3.12-dev -y
RUN apt-get install python3-pip -y
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
RUN pip install --upgrade pip

#Install Robot Framework and Requests
RUN pip install robotframework requests

#Copy the test files
COPY ./post.py /post.py
COPY ./report.py /report.py
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

#Run the test
ENTRYPOINT [ "/entrypoint.sh" ]