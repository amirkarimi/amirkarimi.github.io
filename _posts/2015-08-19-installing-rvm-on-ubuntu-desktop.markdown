---
layout: post
title:  "Installing RVM on Ubuntu Desktop"
date:   2015-08-19 16:14
---

RVM installation is [clearly described at rvm.io](https://rvm.io/rvm/install){:target="_blank"}, but I've always had problem loading the Ruby after installing RVM.

<!--more-->

I use the default installation script:

{% highlight bash %}

curl -sSL https://get.rvm.io | bash -s stable --ruby

{% endhighlight %}

But ruby is not available at the terminal (Gnome Terminal).

The problem is that the installer will change `~/.profile` and not `~/.bashrc`. In Bash shell, `~/.profile` or `~/.bash_profile` will be loaded When the terminal is running as a login shell, otherwise `~/.bashrc` will be executed. 

![Gnome Terminal Preferences](/assets/images/run_as_login_terminal_screenshot.png){: .center-image }

So there are two options:

* Check "Run as login terminal" option of the terminal profile (as shown in the picture)
* Copy the startup codes from `~/.profile` to `~/.bashrc`.
