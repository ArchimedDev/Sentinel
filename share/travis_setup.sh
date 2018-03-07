#!/bin/bash
set -evx

mkdir ~/.archimedcore

# safety check
if [ ! -f ~/.archimedcore/.archimed.conf ]; then
  cp share/archimed.conf.example ~/.archimedcore/archimed.conf
fi
