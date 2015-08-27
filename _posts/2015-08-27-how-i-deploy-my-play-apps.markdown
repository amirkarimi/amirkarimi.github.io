---
layout: post
title:  "How I Deploy My Play! Apps"
date:   2015-08-27 21:51
---

I don't use services like Heroku as deployment infrastructure. They are amazing but I have my reasons.

<!--more-->

* I don't use a service or software unless I know how it works
* After I figured out how Heroku works, I have my own small automated deployment system which works fine
* Heroku costs me 10x more than my own automated deployment process
* I prefer to publish the binaries not sources

I also needed to run my own MongoDB instance, in which I was storing the files as well as other data. This way, Heroku costs me about 80$/mo for a service which I could build by myself for about 8$/mo.

When I moved to Scala I was new to Linux as well. Deploying a standalone web application was not an easy task for me, especially with that IIS background.

But I did a very well job IMO :D and finally (after about a year) I [published it on GitHub](https://github.com/AmirKarimi/play-publish). It's not perfect and need some polishing, but it works.