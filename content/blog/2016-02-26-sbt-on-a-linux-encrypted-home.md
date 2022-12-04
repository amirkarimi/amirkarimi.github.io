---
date: 2016-02-26
keywords: sbt, linux, encrypted home, scala, File name too long, java.lang.NoSuchMethodError
slug: sbt-on-a-linux-encrypted-home
template: post.html
title: Running SBT on a Linux encrypted home
---

If you use Linux and encrypt your home folder, you may get the following error when compiling a SBT project:

```text
[error] File name too long
[error] one error found
[error] (compile:compile) Compilation failed
```

<!--more-->

When your home folder is encrypted, the file names are also encrypted and the encrypted file names [would be longer than the original ones](http://unix.stackexchange.com/questions/32795/what-is-the-maximum-allowed-filename-and-folder-size-with-ecryptfs). On the other hand, default maximum file name length for Scala compiler is 255 which is OK when the file names are unencrypted.

Fortunately it's easily possible to change the default max file name length for Scala compiler by putting the following command in `~/.sbt/0.13/local.sbt` file (for sbt 0.13.x);

```sbt
scalacOptions ++= Seq("-Xmax-classfile-name","100")
```

It sets the maximum class file name length to 100 which after encryption will not exceed the maximum limit. SBT will pick this setting for all projects for the current user.

### Slick 3.0 weird error ###
I've found out this workaround [here](http://stackoverflow.com/questions/28565837/filename-too-long-sbt/32862972#32862972) and set `max-classfile-name` to **72** which is the recommended value in the answer. But I got the weird `java.lang.NoSuchMethodError: slick.driver.JdbcProfile$API.schemaActionExtensionMethods` error. It took me several hours to find out that the reason for the error is because Slick 3.0 jar contains a file with a length greater than 72 which was [mentioned](http://stackoverflow.com/questions/28565837/filename-too-long-sbt/32862972#comment58076434_32862972) in the SO comments but I didn't notice.
