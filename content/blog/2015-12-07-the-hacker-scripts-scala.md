---
date: 2015-12-07
slug: the-hacker-scripts-scala
template: post.html
title: The hacker scripts in Scala
---

You may have read or heard about [that amazing true story about a hacker scripts](https://github.com/NARKOZ/hacker-scripts) which inspired hackers who enjoy living inside the terminal!

<!--more-->

Those scripts are implemented in other languages by the community as well. So I implemented the [coffee machine script](https://github.com/NARKOZ/hacker-scripts/blob/master/scala/fucking-coffee.scala) using [Ammonite-Shell](http://lihaoyi.github.io/Ammonite/#GettingAmmonite-Shell) in Scala. It really feels like a scripting language but without losing type safety!

Here is some points about Ammonite:

* It's super easy to [install](http://lihaoyi.github.io/Ammonite/#GettingAmmonite-Shell)
* If you know Scala you know Ammonite-Shell
* To run your Scala script file from bash you must import `ammonite.ops.ImplicitWd._`
* If you need help you can join [Ammonite Gitter channel](https://gitter.im/lihaoyi/Ammonite)

Let's implement other scripts...