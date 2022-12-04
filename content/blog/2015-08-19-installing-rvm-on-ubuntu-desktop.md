---
date: 2015-08-19
slug: installing-rvm-on-ubuntu-desktop
template: post.html
title: Installing RVM on Ubuntu Desktop
---

RVM installation is [clearly described at rvm.io](https://rvm.io/rvm/install){:target="_blank"}, but I've always had problem loading the Ruby after installing RVM.

<!--more-->

I use the default installation script:

```bash

curl -sSL https://get.rvm.io | bash -s stable --ruby

```

But ruby is not available at the terminal (Gnome Terminal).

The problem is that the installer only updates `~/.profile` not `~/.bashrc`. In Bash shell, `~/.profile` or `~/.bash_profile` will be loaded only when the terminal is running as a login shell, otherwise just `~/.bashrc` will be loaded.

![Gnome Terminal Preferences](/assets/img/run_as_login_terminal_screenshot.png){: .center-image }

So there are two options:

* Copy (move) the startup codes from `~/.profile` to `~/.bashrc`
* Check "Run as login terminal" option of the terminal profile (as shown in the picture)

It [seems](http://askubuntu.com/a/337477/190988) that the second one is not recommended!
