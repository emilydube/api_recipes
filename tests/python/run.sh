#!/usr/bin/env bash

API_KEY=$1
API_SECRET=$2
BASE_URL=$3

APP_NAME="api_test"
VIRTUAL_ENV_ROOT=~/.virtualenv
VIRTUAL_ENV_DIR=$VIRTUAL_ENV_ROOT/$APP_NAME
rm -rf $VIRTUAL_ENV_DIR
mkdir -p $VIRTUAL_ENV_ROOT

WHICH_PYTHON=`which python`

virtualenv -p $WHICH_PYTHON --clear $VIRTUAL_ENV_DIR
source $VIRTUAL_ENV_DIR/bin/activate

pip install -r requirements.txt

py.test --key $API_KEY --secret $API_SECRET --baseurl $BASE_URL


