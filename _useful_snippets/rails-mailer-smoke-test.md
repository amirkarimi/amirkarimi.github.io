---
layout: page
date: 2020-07-01
title: Rails Mailer Smoke Test
category: Rails
keywords: rails, mailer, active mailer, smoke test, bash
---

When you need to see the generated HTML by active mailer in your browser you can run the following code:

<!--more-->

```bash
rails runner 'puts MyMailer.welcome_email("email@email.com", "Subject").body.to_s' | \
  awk '/<!DOCTYPE.*/,EOF' > test.html && \
  xdg-open test.html
```

* `MyMailer.welcome_email` and its parameters should be changed to match your code
* Read about [Action Mailer](https://guides.rubyonrails.org/action_mailer_basics.html#walkthrough-to-generating-a-mailer) if you're not already familiar with
* `awk` command is used to leave out the Rails `runner` logs
* Replace `xdg-open` with `open` for MacOS
