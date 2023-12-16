# A Dockerfile must begin with a FROM instruction, which 
# specifies the Parent Image from which we are building.

# Syntax: FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]
# platform, name and tag are opt, the builder assumes a latest tag by default

#The specified user is used for RUN instructions.

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

#use the minimal-jupyter-notebook image from the Jupyter Docker repository as a template
FROM jupyter/minimal-notebook AS jupyter_min_nb_sage_default

# Switch to root user for installing system-wide packages
USER root

# Install SageMath
RUN apt-get update && apt-get install -y sagemath sagemath-doc sagemath-jupyter

# Install dockerspawner, nativeauthenticator
# hadolint ignore=DL3013
RUN python3 -m pip install --no-cache-dir \
    dockerspawner \
    jupyterhub-nativeauthenticator \
    jupyterhub-samlauthenticator \
    oauthenticator

# Create the notebook directory
RUN mkdir /home/jovyan/notebooks

# Set the permissions for the notebook directory
RUN chmod 700 /home/jovyan/notebooks

USER jovyan