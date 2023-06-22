#!/bin/bash

## Set number of characters for password
character_count=14

function gen_pass() {
    openssl rand -base64 $character_count
}

function main() {
    if [[ $character_count -lt 0 ]]; then
        echo "[ERROR] Password character count cannot be less than 0."
        exit 1
    else
        _pwd=$(gen_pass)

        echo "Strong Redis password: ${_pwd}"
    fi
}

main

exit $?
