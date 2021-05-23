FROM ubuntu:latest
RUN apt update  -y
RUN apt install -y python3
RUN pip install flask
RUN pip install pytest
COPY api.py /
COPY  test_minesweeperapi.py /
ENTRYPOINT pytest -v