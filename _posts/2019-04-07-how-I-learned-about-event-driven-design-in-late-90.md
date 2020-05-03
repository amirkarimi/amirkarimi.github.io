---
layout:     post
title:      "How I learned about event-driven design in the late 90's"
date:       2019-04-07 18:50
keywords:   "event-driven, reactive programming, keyboard, hardware design, assembly x86, late 90's, distributed systems, event sourcing"
---

The event-driven design has already been around for a while. Like many other trendy patterns, it's far older than what we think. Before the web era, it was quite normal to design stand-alone desktop applications using this design. But it is even older than that. It has already been used massively since the mainframe era (and probably even before).

This is the story of how I learned about event-driven design without even knowing what it's called in the late 90s when I was just getting started to learn how computers work.

<!--more-->

You might have noticed how many pins are connecting your keyboard to a computer? Though it's hard to see the pins on a USB port it was more visible on [PS/2 connectors](https://en.wikipedia.org/wiki/PS/2_port). Either way, it's definitely not enough to deliver the state of all the keys simultaneously. For a keyboard with 110 keys in 6 rows, we need about 25 pins (6 rows x 19 columns) to be able to transfer the whole keyboard status simultaneously.

![Source: Wikipedia](https://upload.wikimedia.org/wikipedia/commons/f/f2/FunctionalCircuitDiagramOfKeyboardNumPadScanningProcedure-small.gif)

Then how is it possible to play a video game by pressing and holding a couple of keys all together? They need to be very responsive and accurate otherwise the gaming experience would be awful.

I was trying to understand how the keyboard driver works in the late 90s. So I thought if it has to be real-time, responsive and accurate we probably need a big flag number created out of ~110 bits (as much as the number of keys on a keyboard). This number can represent the whole keyboard state as each bit represents a key. 0 means the key is up and 1 means pressed.

I figured out whatever comes from the keyboard can be read from the I/O port number `0x60`. This is not a TCP port or something like that. This is so low level that there's a [CPU instruction](https://stackoverflow.com/questions/3215878/what-are-in-out-instructions-in-x86-used-for) for that called `IN` (`OUT` for writing data to an I/O port). Reading from an I/O port in Assembly is like:

{% highlight asm %}
IN AL, 60h
{% endhighlight %}

But it was only 8 bits. I checked the other numbers around (~75-85) but none of them were sending any data when I was pressing the keys. That was the moment I got introduced to the idea of **even-driven design**. 

I realized that the keyboard sends two types of signals. One when a key is pressed and another one when it's released. I found my idea of 110 big flag number really stupid! It simply could be done as a stream of events and the OS or applications can create the real-time state of the whole keys at their side. Keeping one bit for indicating whether the key is up or down, it leaves us with 7 bits which means 127 keys using only one byte.

There's [a single-chip microcontroller](https://en.wikipedia.org/wiki/Intel_MCS-48) in the keyboard that scans the keys and sends the signals to the PC. Nowadays it still works exactly the same way except it sends the data through Bluetooth or a USB port which is standardized to work with not only keyboard but almost everything. 

Modern PCs don't have any PS/2 connectors. Less modern ones remained compatible by emulating the USB Keyboards and Mice as PS/2 devices. This is called USB Legacy Support which you might have seen on your PC BIOS settings. Although even the legacy support itself has become obsolete.

You can try it on your *nix machine right now. Although not directly from IO ports, you can read the signals from your keyboard input device driver under `/dev/input/`. In my case it's like:

{% highlight bash %}
$ cat /dev/input/by-id/usb-Metadot_-_Das_Keyboard_Das_Keyboard-event-kbd
{% endhighlight %}

You will see two separate events when a key is pressed or released.

Communicating through events and building the state remotely, instead of reflecting the whole state, is the idea behind the event-driven design. Whether it's a hack or an elegant design, the same approach is being used to replicate a database or share the state in a distributed system. The increased latency of transmitting the events increases the chance of getting conflicts in a distributed environment and resolving them is not as easy as the keyboard state, yet this is the safest and easiest solution available.

*Image Sources: [Wikipedia](https://en.wikipedia.org/wiki/Computer_keyboard)*
