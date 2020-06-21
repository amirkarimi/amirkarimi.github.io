---
layout: post
title:  "How to run 32-bit Andorid SDK on 64-bit Arch Linux"
date:   2015-11-29 18:30
---

Andorid SDK is a 32-bit application and needs some extra works to run on a 64-bit Arch Linux.

<!--more-->

Instead of installing from AUR, I downloaded standalone Andorid SDK. Android Studion couldn't run adb which I finally realized that it's a 32-bit application and can't run on my 64-bit system. On Ubuntu it will be solved by installing `ia32-lib` package but it seems that there is no easy alternative for Arch currently.

There are two ways to run a 32-bit application on a 64-bit Arch system:

1. Installing `lib32-*` package from the multilib repository
2. Creating a 32-bit chroot

I prefer the first one which seems easier. I [enabled multilib repository](https://wiki.archlinux.org/index.php/Multilib) but what 32-bit packages required by adb? I took a look at the following AUR package PKGBUILD files:

* [android-sdk](https://aur.archlinux.org/packages/android-sdk/)
* [android-sdk-platform-tools](https://aur.archlinux.org/packages/android-sdk-platform-tools/)
* [android-sdk-build-tools](https://aur.archlinux.org/packages/android-sdk-build-tools/)

And installed all 32-bit dependencies mentioned in them:

```text
# pacman -S lib32-alsa-lib lib32-openal lib32-libstdc++5 lib32-libxv \
    lib32-mesa lib32-sdl lib32-fontconfig lib32-libpulse \
    lib32-gcc-libs lib32-zlib lib32-ncurses swt
```

Then I was able to start developing my Android app.