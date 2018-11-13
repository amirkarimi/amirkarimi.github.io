---
layout:     post
title:      "Chromium to Firefox Experience"
date:       2018-11-13 14:50 TODO
keywords:	"Chrome, Firefox, migrate to Firefox, Chrome vs Firefox, Chromium, multiple profiles, browser performance, browser RAM usage, Gnome, Linux"
---

A while ago, I decided to give Firefox a try. Here I'm going to share why and how it happened. Also I'll share how I configured my work and personal browser profiles on my Gnome desktop.

![Screenshot of Firefox profile launchers](/assets/images/2018-11-13-chrome-ff-screen-shot.png){: .center-image }

<!--more-->

As I use my personal laptop at work, I have a separate browser profile for work. After all, 99% of non-development works happen inside the browser.

It's been long enough that I don't remember when I started using Chromium exactly but it's been my favorite browser for a long time. Chromium is quite similar to Chrome so I'm not going to compare them. One of the most valuable features of Chromium/Chrome is its seamless sync and integration. Not only between your machines but also your phone. Also the form and password autocompletions stay out of your way.

Obviously the biggest issue with Chromium/Chrome is its RAM usage. But I'm also experiencing some performance issues. Specially during the start up time or when switching profiles. Having lots of tabs open and keep the session saved, makes it even worse. After releasing Firefox Quantum I started thinking to move to Firefox as it was noticeably faster. Not only start up time but also page rendering and everything else. It also has a better support of those weird corporate ancient websites which still using Flash or any other infamous tool.

Finally, I decided to give it a try. As the first step, I moved my passwords to LastPass so that I can share them between the browsers in case I wanted to switch back. Also setup a sync account on FF and migrated the browser history from Chromium.

Now not only the browsing experience got much better but also the whole system works smoother. The RAM usage has gone down significantly and the swap is less engaged (although it was fast enough because of SSD). Moreover, switching profiles has never been smoother.

I had two problems with Firefox though. Dark theme control rendering and not being able to switch tabs with mouse scroll wheel. Firefox renders the controls as native OS components so with a dark them you won't be able to see the text on a textbox with an explicit light background for instance. Fortunately, Firefox is customizable enough that there are a couple of [workarounds](https://www.reddit.com/r/Ubuntu/comments/8su4lm/fix_firefox_dark_text_input_on_ubuntu_18_when/). Finally, the only thing that I missed is switching between tabs using mouse wheel. Although it could be enabled by addons, seems that the latest version doesn't provide the required API. Again [nothing is impossible](https://forum.manjaro.org/t/howto-enable-tab-switching-in-firefox-using-mouse-wheel/39954).

## Multiple Profiles

Now let's see how I'm switching between profiles in Firefox.

First of all, you need to create a new profile. You can navigate to `about:profiles`, click on `Create New Profile` and follow the instruction. But there's no default GUI for switching profiles in the toolbar or menu. Instead, you can launch a profile in a new browser by running `firefox -p <profile-name>`.

If you're using Gnome, you can make it easier to launch a specific profile directly from the desktop by updating the Firefox launcher file at `/usr/share/applications/firefox.desktop`. Define two new actions by adding the following lines at the end of the file:

```plan
[Desktop Action default-profile]
Name=Open Default Profile
Exec=firefox -p default

[Desktop Action work-profile]
Name=Open Cake Profile
Exec=firefox -p work
```

Then update the line starting with `Actions=` from this:

```plan
Actions=new-window;new-private-window;
```

to 

```plan
Actions=new-window;new-private-window;default-profile;work-profile;
```

Now restart Gnome shell (by pressing `ALT + F2` and executing `r`) and you'll be able to launch your profile directly from the desktop. Those action items will appear on context menu when you right click on Firefox launcher. I just tested it on Gnome 3.30.1 but I guess it works for almost all desktops environments.
