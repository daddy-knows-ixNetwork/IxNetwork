#FROM ubuntu:24.04
# switching back to 22.04 due to 24.04 does not allow pip install as root
# will switch back to 24.04 after testing virtualenv with uv
FROM ubuntu:22.04
# ubuntu 22.04 requires creating ubuntu user
# will remove when switching to 24.04
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
    python3-tk \
    tcl tcltls tcllib tcl-dev tclx  && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

RUN rm -rf /var/lib/apt/lists/*
RUN apt clean

USER $USERNAME
ENV HOME "/home/${USERNAME}"
ENV LC_ALL "C.UTF-8"
ENV LANG "en_US.UTF-8"

# pyenv
ENV PYENV_ROOT "${HOME}/.pyenv"
ENV PATH "${HOME}/.pyenv/shims:${HOME}/.pyenv/bin:${PATH}"
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc
RUN echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
#
RUN set -ex && \
    curl https://pyenv.run | bash && \
    pyenv install 3.14 && \
    pyenv global 3.14 && \
    pip install --upgrade pip

RUN set -ex && \
    # ansible, uv, pre-commit
    pip install \
    ansible \
    uv \
    pre-commit \
    jupyterlab

# kubectl cli
#RUN set -ex && \
#    bash -c "curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg" && \
#    bash -c "echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list" && \
#    sudo apt update && \
#    sudo apt install -y kubectl && \
#    echo 'alias k=kubectl' >> ~/.bashrc

# inherited from ubuntu 22.04 ssh rsa does not work for pakcer-provisioner-ansible; let's add temporary workaround
RUN set -ex && \
    echo '    PubkeyAcceptedKeyTypes +ssh-rsa' | sudo tee -a /etc/ssh/ssh_config && \
    echo '    HostKeyAlgorithms +ssh-rsa' | sudo tee -a /etc/ssh/ssh_config
#sudo usermod -aG docker ${USERNAME} && \
#sudo usermod -aG root ${USERNAME}

# By default, pip install the requirements from 26.0 that's the same requirements.txt for the 11.xx release
ADD IxNetworkAPI26.0.2601.6PI.tar.gz /opt/
# RUN pip install -r /opt/ixia/ixnetwork/26.0.2601.6/lib/PythonApi/requirements.txt
ADD IxNetworkAPI11.10.2508.10PI.tar.gz /opt/
ADD IxNetworkAPI11.00.2504.10PI.tar.gz /opt/
# different requirements.txt for 10.00
ADD IxNetworkAPI10.00.2312.4PI.tar.gz /opt/

RUN set -ex && \
    uv venv /opt/ixia/venv/venv26.00 &&\
    . /opt/ixia/venv/venv26.00/bin/activate &&\
    uv pip install -r /opt/ixia/ixnetwork/26.0.2601.6/lib/PythonApi/requirements.txt &&\
    uv pip install --upgrade ixnetwork-restpy &&\
    deactivate &&\
    uv venv /opt/ixia/venv/venv11.10 &&\
    . /opt/ixia/venv/venv11.10/bin/activate &&\
    uv pip install -r /opt/ixia/ixnetwork/11.10.2508.10/lib/PythonApi/requirements.txt &&\
    uv pip install --upgrade ixnetwork-restpy &&\
    deactivate &&\
    uv venv /opt/ixia/venv/venv11.00 &&\
    . /opt/ixia/venv/venv11.00/bin/activate &&\
    uv pip install -r /opt/ixia/ixnetwork/11.00.2504.10/lib/PythonApi/requirements.txt &&\
    uv pip install --upgrade ixnetwork-restpy &&\
    deactivate &&\
    uv venv /opt/ixia/venv/venv10.00 &&\
    . /opt/ixia/venv/venv10.00/bin/activate &&\
    uv pip install -r /opt/ixia/ixnetwork/10.00.2312.4/lib/PythonApi/requirements.txt &&\
    uv pip install --upgrade ixnetwork-restpy &&\
    deactivate

# ohmybash
RUN set -ex && \
    cd ${HOME} && \
    cp .bashrc .bashrc_copy && \
    bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)" && \
    cat .bashrc_copy >> .bashrc && \
    rm .bashrc_copy && \
    sed -i 's/spack_env\$python_venv/spack_env\$HL_VERSION \$python_venv/g' ~/.oh-my-bash/themes/font/font.theme.sh

WORKDIR ${WORKDIR}
