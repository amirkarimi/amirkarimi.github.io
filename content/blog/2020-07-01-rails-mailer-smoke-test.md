---
category: Useful Snippets
date: 2020-07-01
keywords: useful snippets, rails, mailer, active mailer, smoke test, bash
slug: rails-mailer-smoke-test
template: post.html
title: Rails Mailer Smoke Test
---

Use this code snippet when you need to see the generated HTML by active mailer in the browser.

<!--more-->

```bash
rails runner 'puts MyMailer.welcome_email("email@email.com", "Subject").body.to_s' | \
  awk '/<!DOCTYPE.*/,EOF' > test.html && \
  xdg-open test.html
```

* `MyMailer.welcome_email` and its parameters should be changed to match your code
* Read about [Action Mailer](https://guides.rubyonrails.org/action_mailer_basics.html#walkthrough-to-generating-a-mailer) if you're not already familiar with
* `awk` command is used to omit the Rails `runner` logs
* Replace `xdg-open` with `open` in MacOS
