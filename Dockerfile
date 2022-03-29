FROM archlinux:latest

WORKDIR /usr/src/app

COPY . .
RUN pacman -Syu

RUN pacman -S python

RUN pip install --no-cache-dir -r requirements.txt

CMD ["/usr/bin/bash"]