## https://github.com/rljbufny1/ghub_exercise2

- Demonstrates the procedure for hosting the Jupyter Book Github tool, ghub_exercise2, on Ghub.<br>
- See https://theghub.org for more information on the Ghub Science Gateway.<br> 
- See Jupyter Book Zenodo reference: https://doi.org/10.5281/zenodo.2561065 for more information on Jupyter Book.

### Requirements:

#### notebooks directory

Contains the Jupyter Notebooks to be displayed by the Jupyter Book.

#### jupyter-book template directory

The Jupyter Book template directory, jupyter-book, contains the _config.yml and _toc.yml files as well as 
additional files required by the Jupyter Book, index.md and user_manual.md.

This directory also contains a link to the notebooks directory. Use ln -s ../notebooks notebooks to create the link.

#### ghub_exercise2_landing_page.ipynb

The landing page Jupyter Notebook, ghub_exercise2_landing_page.ipynb, contains the calls to build and display the Jupyter Book.

#### middleware directory

The middleware directory contains the invoke script which enables the landing page Jupyter Notebook to be launched on Ghub from the Ghub Dashboard's My Tools component.

### Install and Run the Tool on Ghub for Initial Testing (optional):

#### Launch the Workspace 10 Tool from the Ghub Dashboard's My Tools component and in a xterm terminal window enter:<br />

```
git clone https://github.com/rljbufny1/ghub_exercise2
```
or 
```
wget https://github.com/rljbufny1/ghub_exercise2/releases/download/v1.0.0/ghub_exercise2-src.tar.gz
tar xvzf ghub_exercise2-src.tar.gz
```

#### Install the Utils package per ./setup.py, enter:

```
use -e -r anaconda-7
python -m pip install . --target ./lib
```

#### If required, create an environment per ./environment.yml and install the Utils package per ./setup.py to the created environment, enter:

```
use -e -r anaconda-7
conda env create -f environment.yml --prefix ./env
conda activate ./env
python -m pip install . --target ./lib

```

Note: for initial testing, need to prepend the lib directory to PYTHONPATH for each of the Jupyter Notebooks in the notebooks directory.

#### Launch the Jupyter Notebooks (202210) Tool from the Ghub Dashboard's My Tools component:<br />

Open ghub_exercise2/ghub_exercise2.ipynb.<br />
Click the Appmode button.<br />

### Create New Tool on Ghub:

Follow the instructions on the https://theghub.org/tools/create web page. Enter ghub_exercise2 for the Tool Name. Select the Repository Host, Host GIT repository on Github, Gitlab, etc.. Select the Publishing Option, Jupyter Notebook.  

Note: created tools are launched from the Ghub Dashboard's My Tools component.

### Notes:

Current web browser results:

Safari and FireFox, Jupyter Book aligned properly, image displays and links work.<br>
Chrome and Microsoft Edge, Jupyter Book not aligned properly, image does not display, links do not work.
