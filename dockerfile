FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x exec_lexer.sh

COPY . .

CMD [ "python", "./pyscript.py" ]
