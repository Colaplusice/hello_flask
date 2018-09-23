#!/usr/bin/env bash

env_name=hello_flask


if [ "$(uname)"=="Darwin" ];
then
export PATH=~/Anacoda/anaconda2/bin:$PATH
export PATH=~/Anacoda/anaconda3/bin:$PATH
echo ". ~/Anacoda/anaconda2/etc/profile.d/conda.sh" >> ~/.bash_profile
conda activate $env_name
    if [ $? == 1  ]; then
        echo env does not exist, will create a new env
        conda create -n $env_name python=3.6.4
        conda activate $env_name
    fi
 # Mac OS X 操作系统

elif [ "$(expr substr $(uname -s) 1 5)"=="Linux" ]; then
# GNU/Linux操作系统
    export PATH=~/anaconda2/bin:$PATH
    export PATH=~/anaconda3/bin:$PATH
    source activate $env_name

    if [ $? == 1  ]; then
    echo env does not exist, will create a new env
    conda create -n $env_name python=3.6.4
    source activate $env_name
    else
    echo env has been created
    fi

pip install -r ././../requirements/requirements.txt pip install -r ././../requirements/requirements.txt

    if [ $? == 0 ]; then
    echo python环境安装完成!
    fi

fi