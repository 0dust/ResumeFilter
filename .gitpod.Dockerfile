FROM gitpod/workspace-full

USER gitpod

RUN echo 'unset PIP_USER' >> ~/.bashrc

USER root

RUN  curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh  && bash Anaconda3-2019.03-Linux-x86_64.sh -b -p ~/anaconda && \
rm Anaconda3-2019.03-Linux-x86_64.sh && \
echo 'export PATH="~/anaconda/bin:$PATH"' >> ~/.bash_profile  && \
conda update conda && \
conda create --name resumefilter python=3.7.6 && \
conda activate resumefilter