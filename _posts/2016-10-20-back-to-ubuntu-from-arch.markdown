---
layout:     post
title:      "Back to Ubuntu from Arch"
date:       2016-10-20
keywords:	"linux, Arch, ubuntu, open source"
---

Several month ago, I left Ubuntu for Arch. This post is about my experiences and the reasons that led me to move back to Ubuntu.

**Update 2017-01-21**: As the VirtualBox bug, which made me go back to Ubuntu, is resolved, I couldn't resist going back to Arch. This time I tried *i3* instead of a full fledged DE and I'm very happy so far.

<!--more-->

## Why Moving to Arch ##

Arch is one of the most unopinionated distros available. You're not forced (almost even not recommended) to use a specific display manager, desktop environment, terminal, etc. while almost every choice is made available with a very good documentation and community support.

It encourages you to improve your knowledge about Linux, and find out how it works. Most importantly it helps you to be a part of the community. You have to learn how to fix and improve things by yourself.

## Arch Experience ##

The learning experience started from the moment I began installing Arch. I just realized what happens behind the scenes of a graphical installation application. This was the first time I experienced UEFI and learned more about booting an OS. I learned about the ramfs and udev, figured out how the display manager works and many many more.

Actually the Arch Linux is nothing but a good community and an amazing package manager (Pacman), everything else is the product of the open source ecosystem which is not essentially designed to be used by a specific distro. You may install Gnome, Plasma, Xfce, Cinnamon, or whatever you like as your desktop environment. The chance of finding two identical installations of Arch distro with the same fundamental packages is much less than other distros. It sounds very cool and I think Arch is very successful to provide a real freedom experience. Arch is the best available choice for a true open source lover geek.

All these amazing things come with a cost; time and energy. The rolling release development model of the Arch might led you to have a buggy version of an application which might be very important to you. This would be irritating when you have a deadline, where nobody cares about your cool distro, your true freedom and your fantastic customized tiling window manager.

Another issue is stability. I installed Plasma 5 and it was unstable. I really like to have a very advanced desktop environment but it encounters an error almost one time out of ten. It really bothers you after a while.

## Moving Back to Ubuntu ##
Some of the companies I'm working with, are using WebEx for audio conferencing which doesn't support Linux. I couldn't find any way except having a Windows on a virtual machine. VirtualBox is my favorite choice, but [the mic doesn't work on the latest version of VirtualBox (5.1)](https://forums.virtualbox.org/viewtopic.php?f=7&t=78797) which is even [documented](https://wiki.archlinux.org/index.php/VirtualBox#Analog_microphone_not_working_in_guest) in the Arch wiki. It was a shame that I figured out this problem in the middle of a meeting when I was talking and everybody was ignoring me!

I had to downgrade VirtualBox to 5.0 which is really a hard job. Most of the times, you have to downgrade dependencies as well and suddenly some other packages would stop working. I didn't have enough time to handle the situation and finally ended up installing an Ubuntu to be able to attend the meetings.

## Conclusion ##
I really miss Arch and I really enjoy working with cutting edge and geeky distros. But it would get tedious when you learned how the distro works under the hood. Finally, I need to get my works done specially when I don't have enough time to figure out these sort of bugs.

Arch is for the people who are not just consumers, geeks who enjoy fixing problems and hacking things and who get tired of routine and non-challenging environments. It's for DIY-ers. If you're just a consumer and you just use Linux as a fundamental tool for creating other things, or you don't have enough time, then you have better choices than Arch.

## Update 2017-01-21 ##

As the VirtualBox bug, which made me go back to Ubuntu, is resolved, I couldn't resist going back to Arch. This time I tried *i3* instead of a full fledged DE and I'm very happy so far.
