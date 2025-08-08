# Disable token and password
c.NotebookApp.token = ''
c.NotebookApp.password = ''

# Set Jupyter working directory
c.NotebookApp.notebook_dir = '/home/jovyan/work'

# Disable trash (delete - forever)
c.FileContentsManager.delete_to_trash = False