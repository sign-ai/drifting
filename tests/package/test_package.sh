rm -rf venv_test
~/.pyenv/versions/3.9.10/bin/python -m virtualenv venv_test
pip install drifting

python -m "import drifting"
