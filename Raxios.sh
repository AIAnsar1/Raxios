#!/usr/bin/env bash


set -e

# For Linux
InstallDepedenciesLinux()
{
  sudo apt update
  sudo apt install -y wget build-essential libssl-dev zlib1g-dev \
        libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev \
        libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev \
        tk-dev libffi-dev liblzma-dev
}

# For MacOS With Brew
InstallDependenciesMacOS()
{
    brew update
    brew install openssl readline sqlite3 xz zlib
}

# For Install Python Latest Stable Version
InstallPython()
{
    PYTHON_VERSION=$(curl -s https://www.python.org/ftp/python/ | grep 'href' | tail -1 | awk -F'"' '{print $2}' | sed 's|/||')
    wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz
    tar -xvf Python-$PYTHON_VERSION.tgz
    cd Python-$PYTHON_VERSION
    ./configure --enable-optimizations
    make -j$(nproc)
    sudo make altinstall
    cd ..
    rm -rf Python-$PYTHON_VERSION Python-$PYTHON_VERSION.tgz
}

# For PIP Python Package Manager
InstallPip()
{
    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3.10 get-pip.py
    rm get-pip.py
}

# For Installing Project Depedencies
InstallProjectDependencies()
{
    pip install lxml tqdm requests bs4 scrapy google_trans_new
}



# Base Block
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Installing in Linux..."
    InstallDepedenciesLinux
    InstallPython
    InstallPip
    InstallProjectDependencies
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Installing in macOS..."
    InstallDependenciesMacOS
    InstallPython
    InstallPip
    InstallProjectDependencies
elif [[ "$OSTYPE" == "msys" ]]; then
    echo "Installing in Windows (With WSL)..."
    InstallDepedenciesLinux
    InstallPython
    InstallPip
    InstallProjectDependencies
else
    echo "Unknown ОС: $OSTYPE. The script only supports Linux, macOS & Windows with WSL."
    exit 1
fi


echo "Python And Dependencies For Project Iqro Tool Installing SuccessFully"