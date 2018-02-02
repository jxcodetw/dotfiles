#!/bin/sh
if test "$(uname)" = "Darwin" ; then
  # MacOS
  install_cmd="brew install"
  pip=""
else
  # Linux
  install_cmd="sudo apt-get install"
  pip="python3-pip"
fi

$install_cmd git zsh tmux python3 $pip
pip3 install npyscreen --user

git clone https://github.com/jxcodetw/dotfiles.git ~/.dotfiles
python3 ~/.dotfiles/install.py
