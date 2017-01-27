---
layout:     post
title:      "Comparing Scala Editors"
date:       2017-01-27
keywords:	"Scala, editor, IDE, Scala IDEs, Integrated development environment, comparison"
---

Choosing the best editor/IDE for your favorite programming language is not as easy as it seems to be. Obviously, that's not the case if you work with the main-stream technologies or if you don't consider yourself a geek programmer!

Right now, Scala is my favorite language and fortunately, contrary to what most developers think, there are a good number of available choices as editor/IDE. This post is about my experiences of using these tools.

<!--more-->

## Scala IDE ##

Although based on Eclipse, it has the best balance of performance and stability. There might be some false positives, hiccups and rare bugs but even in big projects you will get a good performance and correctness compared to other IDEs.

The editor itself, is not so powerful. For example the block selection is medieval, its dark theme is not completely dark, the configuration will be lost when changing the workspace, unstable addons, etc.

Finally, its weakness is that it's Eclipse!

## IntelliJ IDEA ##

Most developers, consider IntelliJ as the best Scala IDE. It might be the best Java IDE but its Scala support is not as efficient as Scala IDE (Eclipse). It's really a good IDE; its editor, UI and almost everything is great but its Scala presentation compiler sometimes takes seconds to load an auto-complete list in a relatively large project. [They rewrote the compiler to integrate with their platform](https://twitter.com/fommil/status/783927587043217408) and it is not as efficient as the standard/community one.

Another issue with IntelliJ is that you'll finally have to purchase the Ultimate edition to be able to handle all your works inside the IDE. Even Less/Sass support requires the Ultimate version. It's not completely free and open source.

## Emacs (ENSIME) ##

It's not an editor war; I just prefer Emacs over Vi because:

* [ENSIME](http://ensime.org/) provides the [richest Scala support](http://ensime.github.io/editors/) in Emacs
* Emacs supports almost every language and framework, you can customize it as much as you like and build your own version; I like super powerful tools
* It feels more modern than Vi
* [Real programmers use Emacs!](https://xkcd.com/378/)

As you might know, Emacs have a different world compared to modern editors. Everything is different; saving, opening, cut-copy-past, etc. it might be very hard to guess the shortcuts even for the simplest tasks. Fortunately, almost everything supports Emacs keybindings, even bash and zsh but still there are some programs with poor keyboard support; they make you use mouse. In such cases you prefer to use an Emacs package which will do the job and you'll end up living in Emacs. I'm not sure if it's a bad thing though!

It gives you the best performance ever as a Scala IDE! I feel that Scala IDE and ENSIME have many things in common under the hood but ENSIME is slightly faster, less resource hungry and of course, more hackable. ENSIME is also not perfect. It stops responding once in a while, either without using CPU or sometimes with too much CPU usage. The good news is that you can easily stop the operation using `Ctrl-G` and continue editing or restart the ENSIME without having to restart the editor. The editor is really stable and you'll enjoy writing code if you rely on yourself more than what IDEs offer out-of-box. You just need to think a little bit different, you'll find a package for almost everything in Emacs. You'll also learn to automate everything more and more and it's a real joy. Eventually, you'll find yourself with more tools than what your previous full-featured IDE offers.

The most interesting part is that writing code in Emacs (or Vim) gives you the feeling of being a real hacker/geek and it's worth more than anything!

## Atom (ENSIME) ##

Atom itself is a good editor; not as geeky as Emacs/Vi but there is no learning curve. It's build on top of web technologies and doesn't feel like a bare-metal native editor. Besides, Atom support in ENSIME is not as great as Emacs. There are more bugs and strange ENSIME behaviors in Atom. For instance, sometimes it sounds like ENSIME is not running but it's not true!

If you're OK with ENSIME but you don't like the extra-geeky editors like Emacs/Vi, Atom is a good choice for you.

## Others ##

I didn't try other options: Vi, Sublime and Visual Studio Code. Because:

* Vi is almost like Emacs from ENSIME point of view although with less features. I just told why I prefered Emacs
* Sublime is not open source and it's not very active recently, though it's a great editor
* Visual Studio Code is a Microsoft product and I don't expect a good support from the open source community. More over, it has many things in common with Atom. For instance, it's based on [Electron](http://electron.atom.io/) like Atom.

## Conclusion ##

You have more options than what you probably think when it comes to Scala IDEs. Most of developers come from a cosy, polished and modern world of IDEs and tools but they need to go deeper to find out that those well-known products are not necessarily the best options for them. Specially when you live in an open source ecosystem you'll eventually find the best thing which works best just for you. Try and enjoy!
