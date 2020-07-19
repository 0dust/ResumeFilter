FROM gitpod/workspace-full

USER gitpod

RUN echo 'unset PIP_USER' >> ~/.bashrc

USER root

RUN  apt-get install -y python3-tk && curl -O https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh  && bash Anaconda3-2020.02-Linux-x86_64.sh -b -p /opt/conda && \
rm Anaconda3-2020.02-Linux-x86_64.sh && \
ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
echo "conda activate base" >> ~/.bashrc && \
echo "Set disable_coredump false" >> /etc/sudo.conf && \
sudo -s source ~/.bashrc

RUN . /opt/conda/etc/profile.d/conda.sh && \
conda create --name resumefilter python=3.7.6 && \
conda activate resumefilter