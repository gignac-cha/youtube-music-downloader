FROM ubuntu

SHELL [ "/bin/bash", "-c" ]

WORKDIR /home/ubuntu

COPY packages ./packages

COPY requirements.txt ./

RUN apt update
RUN apt install -y curl python3 python3-venv ffmpeg
RUN python3 -m venv .venv
ENV PATH="/home/ubuntu/.venv/bin:$PATH"
RUN pip install -r requirements.txt

COPY package.json ./
COPY pnpm-workspace.yaml ./
COPY pnpm-lock.yaml ./

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN source $NVM_DIR/nvm.sh && nvm install 22 && nvm alias default 22 && nvm use 22 && npm install -g pnpm
RUN source $NVM_DIR/nvm.sh && pnpm install --recursive
RUN source $NVM_DIR/nvm.sh && pnpm --filter ui build

EXPOSE 5000

WORKDIR /home/ubuntu/packages/server

CMD [ "python", "server.py" ]
