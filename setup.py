#!/bin/env python2

from subprocess import call

call(["pip", "install", "-r", "requirements.txt"])
call(["./download-crypto-sdk.sh"])
