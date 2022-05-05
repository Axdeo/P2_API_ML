FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests && pip3 install jsonschema==3.2.0
ADD prediction_test.py /home/prediction_test.py
WORKDIR /test/
ENV LOG 1
VOLUME /test/
CMD python3 /home/prediction_test.py
