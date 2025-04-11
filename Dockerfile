

FROM python
RUN apt update -y
RUN apt install -y python3-pip

WORKDIR /dashbord-anstat

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=127.0.0.1"]