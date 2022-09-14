# Created by Roberto Moctezuma
# Date: 08/18/2022
# (c) Fractal River, LLC

# We use python:slim as our default base. This provides a good balance between size and functionality (i.e. alpine build is too slim).
# We also not set a version - the implication of this is that the Python version auto-updates.

FROM python:3.8-slim

LABEL Roberto Moctezuma <roberto@fractalriver.com>

# Set the working directory to /app
WORKDIR /app

# If you don't need CURL, remove this line
# RUN apt-get update && \
#     apt-get install curl -y curl wget

# Get requirements
COPY requirements.txt /app

# Install needed packages (requirements.txt), directories and create credentials mount point.
# Please make sure you do NOT put ANY credentials in the image, instead, read them 
# from files in this directory, which will be mounted at runtime.
# The idea of logging to /logs is that the log files will disappear as soon as the container is deleted,
# unless the person running mounts a directory at /app/logs.

RUN pip install -r /app/requirements.txt && \
	mkdir /app/deputy

# We switch to a non-root users to increase security
RUN groupadd -r appuser && \
	useradd -r -g appuser -d /app appuser && \
	chown -R appuser /app 
USER appuser

# Copy the code files and shell script to run them
COPY run.sh /app
COPY deputy /app/deputy

# Run the shell script when the container launches
CMD ["/bin/bash" , "run.sh"]