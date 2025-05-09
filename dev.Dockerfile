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

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" --unattended
