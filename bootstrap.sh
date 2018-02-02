#!/bin/sh
if test "$(uname)" = "Darwin" ; then
  # MacOS
  install_cmd="brew install"
else
  # Linux
  install_cmd="sudo apt-get install"
fi

$install_cmd git zsh tmux python3 python3-pip
pip3 install npyscreen --user

git clone https://github.com/jxcodetw/dotfiles.git ~/.dotfiles
python3 ~/.dotfiles/install.py
