#!/usr/bin/env python3

import npyscreen, curses
import random
import os

TITLE = "JxCode's dotfiles installer"
BASE_DIR = '~/.dotfiles'

def abspath(path):
    return os.path.expanduser(path)

def pathExists(path):
    return os.path.exists(abspath(path))

class InstallGit():
    name = 'git config'
    ignore = False
    email = 'jxcode.tw@gmail.com'
    username = 'jxcodetw'

    use_default = True
    def start():
        if InstallGit.ignore: return
        os.system('ln -sf {}/gitconfig ~/.gitconfig >> ~/.dotfiles/log 2>&1'.format(BASE_DIR))
        if not InstallGit.use_default:
            content = '[user]\n'
            content += '\temail = {}\n'.format(InstallGit.email)
            content += '\tname = {}'.format(InstallGit.username)
            with open(abspath('~/.gitconfig'), 'w') as f:
                f.write(content)

    def installed():
        return pathExists('~/.gitconfig')

class InstallTmux():
    name = 'tmux'
    ignore = False
    def start():
        if InstallTmux.ignore: return
        os.system('ln -sf {}/tmux.conf ~/.tmux.conf >> ~/.dotfiles/log 2>&1'.format(BASE_DIR))

    def installed():
        return pathExists('~/.tmux.conf')

class InstallVim():
    name = 'vim'
    ignore = False
    def start():
        if InstallVim.ignore: return
        os.system('ln -sf {}/vim ~/.vim >> ~/.dotfiles/log 2>&1'.format(BASE_DIR))
        os.system('ln -sf {}/vim/vimrc ~/.vimrc >> ~/.dotfiles/log 2>&1'.format(BASE_DIR))
        os.system('git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim >> ~/.dotfiles/log 2>&1')
        
    def installed():
        return pathExists('~/.vim')

class InstallPowerlineFont():
    name = 'powerline font'
    ignore = False
    def start():
        if InstallPowerlineFont.ignore: return
        os.system('rm -rf /tmp/fonts >> ~/.dotfiles/log 2>&1')
        os.system('git clone https://github.com/powerline/fonts.git /tmp/fonts >> ~/.dotfiles/log 2>&1')
        os.system('/tmp/fonts/install.sh >> ~/.dotfiles/log 2>&1')

    def installed():
        return pathExists('~/Library/Fonts') or pathExists('~/.local/share/fonts')

class InstallZsh():
    name = 'zsh'
    ignore = False
    def start():
        if InstallZsh.ignore: return

        os.system('wget 2>/dev/null --no-check-certificate http://install.ohmyz.sh -O - | sh >> ~/.dotfiles/log 2>&1')
        os.system('rm ~/.zshrc >> ~/.dotfiles/log 2>&1')
        os.system('ln -sf {}/zshrc ~/.zshrc >> ~/.dotfiles/log 2>&1'.format(BASE_DIR))

    def installed():
        return pathExists('~/.zshrc')

steps = []
steps.append(InstallGit)
steps.append(InstallTmux)
steps.append(InstallVim)
steps.append(InstallZsh)
steps.append(InstallPowerlineFont)

class Installer(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN",  MainForm, name=TITLE)
        self.addForm("QuickInstall", QuickInstallForm, name=TITLE + ' - Quick Install')
        self.addForm("CustomInstall", CustomInstallForm, name=TITLE + ' - Custom Install')
    
    def change_form(self, name):
        self.switchForm(name)
        self.resetHistory()

class MainForm(npyscreen.FormBaseNew):
    def create(self):
        self.btn_quick = self.add(npyscreen.MiniButton, name='Quick Install', value_changed_callback=self.btn_quick_press)
        self.btn_custom = self.add(npyscreen.MiniButton, name='Custom Install', value_changed_callback=self.btn_custom_press)
        self.btn_exit = self.add(npyscreen.MiniButton, name='Exit Installer', value_changed_callback=self.btn_exit_press)

    def btn_quick_press(self, *args, **kwargs):
        if self.btn_quick.value:
            self.parentApp.change_form('QuickInstall')

    def btn_custom_press(self, *args, **kwargs):
        if self.btn_custom.value:
            self.parentApp.change_form('CustomInstall')

    def btn_exit_press(self, *args, **kwargs):
        if self.btn_exit.value:
            self.parentApp.switchForm(None)
    
class QuickInstallForm(npyscreen.FormBaseNew):

    def create(self):
        self.add(npyscreen.TitleText, name = "Progress:", value= "", editable=False)
        names = list(map(lambda x: x.name, steps))
        self.listing = self.add(npyscreen.MultiSelect, max_height=len(steps) + 1, value=[], values=names, editable=False)
        self.progress = self.add(npyscreen.Slider, max_height=2, name='progress', value=0, editable=False)
        self.add(npyscreen.FixedText, name='', editable=False)
        self.btn_install = self.add(npyscreen.MiniButton, name='Installing ... Please Wait', value_changed_callback=self.btn_install_press)

    def btn_install_press(self, *args, **kwargs):
        self.parentApp.switchForm(None)

    def pre_edit_loop(self, *args, **kwargs):
        num = len(steps)
        for i in range(num):
            steps[i].start()
            self.listing.value.append(i)
            self.listing.values = list(map(lambda x:  CustomInstallForm.installed_symbol(x.installed()) + ' ' + x.name, steps))
            self.listing.display()
            self.progress.value = int(((i+1.0)/num) * 100)
            self.progress.display()
        self.btn_install.name = 'Installation Complete'

    

class CustomInstallForm(npyscreen.FormBaseNew):
    installed = False
    def installed_symbol(b):
        if b:
            return '[Installed]'
        return     '[ Not yet ]'

    def create(self):
        self.add(npyscreen.TitleText, name='git config:', editable=False)
        self.gitusername = self.add(npyscreen.TitleText, name='Username', value=InstallGit.username)
        self.gitemail = self.add(npyscreen.TitleText, name='Email', value=InstallGit.email)
        self.add(npyscreen.FixedText, name='', editable=False)
        self.info = self.add(npyscreen.TitleText, name = "Options:", value= "", editable=False)
        names = list(map(lambda x:  CustomInstallForm.installed_symbol(x.installed()) + ' ' + x.name, steps))
        self.listing = self.add(npyscreen.MultiSelect, max_height=len(steps) + 1, value=list(range(len(steps))), values=names, editable=True)
        self.progress = self.add(npyscreen.Slider, max_height=2, name='progress', value=0, editable=False)
        self.add(npyscreen.FixedText, name='', editable=False)
        self.btn_install = self.add(npyscreen.MiniButton, name='Install', value_changed_callback=self.btn_install_press)

    def btn_install_press(self, *args, **kwargs):
        if self.btn_install.value:
            if InstallGit.username != self.gitusername.value or InstallGit.email != self.gitemail.value:
                InstallGit.use_default=False
                InstallGit.username = self.gitusername.value
                InstallGit.email = self.gitemail.value
            self.info.name = 'Progress:'
            self.info.display()
            for i, s in enumerate(steps):
                if not i in self.listing.value:
                    s.ignore = True
            num = len(steps)
            self.listing.value = []
            self.listing.editable=False
            for i in range(num):
                os.system('echo log > ~/.dotfiles/log')
                steps[i].start()
                self.listing.value.append(i)
                self.listing.values = list(map(lambda x:  CustomInstallForm.installed_symbol(x.installed()) + ' ' + x.name, steps))
                self.listing.display()
                self.progress.value = int(((i+1.0)/num) * 100)
                self.progress.display()
            self.btn_install.name = 'Exit'
            npyscreen.notify_confirm('All config have been isntalled to your computer.\nYou can find installation log at ~/.dotfiles/log', 'Installation Complete')
            self.parentApp.switchForm(None)

def main():
    ins = Installer()
    ins.run()

if __name__ == '__main__':
    main()
