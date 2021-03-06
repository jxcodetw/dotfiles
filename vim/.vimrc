" Basic Settings
set nu " show line number
set laststatus=2
set history=700
set undolevels=700
set nocompatible
set encoding=utf-8
set termencoding=utf-8
set fileencoding=utf-8
set fileencodings=utf-8,big5
set backspace=indent,eol,start " make backspace work
set pastetoggle=<F5>
set timeoutlen=1000 ttimeoutlen=0 " eliminating ESC delay
set cursorline
set listchars=tab:>-,trail:~,extends:>,precedes:<,space:.
let mapleader=","
let maplocalleader=","
cmap wt w !sudo tee % >/dev/null

" better search
set hlsearch
set incsearch
set ignorecase
set smartcase

" Disable backup and swap files
set nobackup
set nowritebackup
set noswapfile

" scaffold
au BufNewFile *.c 0r ~/.vim/scaffold/scaffold.c

" Folding
set foldmethod=syntax
set foldlevel=3
set foldnestmax=3

" Always tab
set autoindent
set noexpandtab
set copyindent
set preserveindent
set tabstop=4
set shiftwidth=4

" Plugin
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'gmarik/Vundle.vim'
Plugin 'itchyny/lightline.vim'
Plugin 'jiangmiao/auto-pairs'
Plugin 'scrooloose/nerdtree'
Plugin 'tomasiser/vim-code-dark'
call vundle#end()

syntax on
set t_Co=256 " 256 color
colorscheme codedark
hi Normal guibg=NONE ctermbg=NONE

let g:lightline = { 'colorscheme': 'wombat',}
