FROM project-watertemp

WORKDIR /app

# Install dev tools
RUN apt-get update && \
    apt-get install -y git && \
    apt-get install -y make

# Install zsh
RUN apt-get update && \
    apt-get install -y zsh && \
    apt-get install -y locales && \
    apt-get install -y locales-all && \
    apt-get install -y curl && \
    apt-get install -y wget

ENV ZSH="$_HOME/.oh-my-zsh"

RUN sh -c "$(curl https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" --unattended
