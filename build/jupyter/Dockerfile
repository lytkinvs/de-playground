FROM jupyter/base-notebook:python-3.11

# Copy config file
COPY jupyter_notebook_config.py /home/jovyan/.jupyter/jupyter_notebook_config.py

user root
# Create work directory nd permissions for it
RUN mkdir -p /home/jovyan/work && \
    chown -R jovyan:users /home/jovyan/.jupyter /home/jovyan/work
user jovyan
# Set Docker Working directory
WORKDIR /home/jovyan/work

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

# Open port
EXPOSE 8888

# Start notebook with our configs
CMD ["jupyter", "notebook", "--no-browser"]