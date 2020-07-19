FROM gitpod/workspace-full

USER gitpod

RUN echo 'unset PIP_USER' >> ~/.bashrc

USER root

RUN  curl -O https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh  && bash Anaconda3-2020.02-Linux-x86_64.sh -b -p ~/anaconda && \
rm Anaconda3-2020.02-Linux-x86_64.sh && \
echo 'export PATH="~/anaconda3/bin:$PATH"' >> ~/.bashrc  && \
source ~/.bashrc && \
conda update conda && \
conda create --name resumefilter python=3.7.6 && \
conda activate resumefilter