#FROM ubuntu:24.04
# switching back to 22.04 due to 24.04 does not allow pip install as root
# will switch back to 24.04 after testing virtualenv with uv
FROM ubuntu:22.04
ARG USERNAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=1000
ENV WORKDIR=/IxNetwork

LABEL "maintainer"="Daddy Knows IxNetwork"
LABEL org.opencontainers.image.source=https://github.com/daddy-knows-ixNetwork/IxNetwork
LABEL org.opencontainers.image.description="Daddy's IxNetwork dev-container"

# ubuntu 22.04 requires creating ubuntu user
# will remove when switching to 24.04
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME
#

ENV TZ America/Los_Angeles

ARG DEBIAN_FRONTEND=noninteractive

RUN set -ex && \
    apt update && \
    apt install -y \
    sudo \
    vim \
    git \
    curl \
    build-essential \
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libxml2-dev \
    libxmlsec1-dev \
    llvm \
    make \
    tk-dev \
    wget \
    xz-utils \
    zlib1g-dev \
    apt-transport-https \
    jq \
    unzip \
    iputils-ping \
    dnsutils \
    traceroute \
    iproute2 \
    psmisc \
    pre-commit \
    python3 \
    python-is-python3 \
    python3-setuptools \
    python3-pip \
    python3-tk && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# set environmental variables
#USER $USERNAME
#ENV HOME "/home/${USERNAME}"


ENV LC_ALL "C.UTF-8"
ENV LANG "en_US.UTF-8"

# uv
#RUN set -ex && \
#    curl -LsSf https://astral.sh/uv/install.sh | sh


# ohmybash
#RUN set -ex && \
#    cd ${HOME} && \
#    cp .bashrc .bashrc_copy && \
#    bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)" && \
#    cat .bashrc_copy >> .bashrc && \
#    rm .bashrc_copy

# kubectl cli
#RUN set -ex && \
#    bash -c "curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg" && \
#    bash -c "echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list" && \
#    sudo apt update && \
#    sudo apt install -y kubectl && \
#    echo 'alias k=kubectl' >> ~/.bashrc

# inherited from ubuntu 22.04 ssh rsa does not work for pakcer-provisioner-ansible; let's add temporary workaround
#RUN set -ex && \
#    echo '    PubkeyAcceptedKeyTypes +ssh-rsa' | sudo tee -a /etc/ssh/ssh_config && \
#    echo '    HostKeyAlgorithms +ssh-rsa' | sudo tee -a /etc/ssh/ssh_config
#sudo usermod -aG docker ${USERNAME} && \
#sudo usermod -aG root ${USERNAME}

#RUN sudo rm -rf /var/lib/apt/lists/*
#RUN sudo apt clean


# https://downloads.ixiacom.com/support/downloads_and_updates/public/IxNetwork/11.00-Update1/11.00.2407.67/IxNetworkAPI11.00.2407.37Linux64.bin.tgz
COPY IxNetworkAPI11.00.2407.37Linux64.bin /IxNetwork/IxNetworkAPI11.00.2407.37Linux64.bin
RUN bash /IxNetwork/IxNetworkAPI11.00.2407.37Linux64.bin -i silent && \
    pip install --no-cache-dir -r /opt/ixia/ixnetwork/11.00.2407.37/lib/PythonApi/requirements.txt

USER $USERNAME
ENV HOME "/home/${USERNAME}"

WORKDIR ${WORKDIR}
