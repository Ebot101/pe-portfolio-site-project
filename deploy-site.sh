#!/bin/bash

cd "pe-portfolio-site-project"
echo "$PWD"

git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate
pip install -r requirements.txt


if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "Python virtual environment is active."
else
    echo "Python virtual environment is not active."
fi

systemctl restart myportfolio

systemctl status myportfolio
