FROM ubuntu-latest

#Setup Python 3.11
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install python3.11 python3.11-dev python3.11-distutils -y
RUN apt-get install python3-pip -y
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
RUN pip install --upgrade pip

#Install Robot Framework and Requests
RUN pip install robotframework requests

#Copy the test files
COPY ./post.py /post.py
COPY ./report.py /report.py
COPY ./entrypoint.sh /entrypoint.sh

#Run the test
ENTRYPOINT [ "/entrypoint.sh" ]