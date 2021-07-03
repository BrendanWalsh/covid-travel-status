FROM tiangolo/meinheld-gunicorn-flask:python3.8
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN apt-get update
RUN apt-get install -y parallel jq
RUN /bin/bash covid.sh --install
CMD ["/bin/bash", ".scripts/run-prod.sh"]
