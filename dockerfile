FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x exec_lexer.sh
RUN chmod +x exec_parser.sh

COPY . .

CMD [ "python", "./pyscript.py" ]
