---
layout: post
date: 2020-08-23
title: List Trello Cards After a Specific One
category: Useful Snippets
keywords: useful snippets, trello, javascript, browser
---

List all card titles after the one contains "End of June" inside the browser.

<!--more-->

Open the developer tool in your browser and type in:

```javascript
$(":contains('End of June')").parent("a.list-card").nextAll("a.list-card").find(".list-card-title").toArray().map(a => a.innerText)
```

To build a bullet list:

```javascript
items = $(":contains('End of June')").parent("a.list-card").nextAll("a.list-card").find(".list-card-title").toArray().map(a => a.innerText);

console.log("- " + items.join("\n- "))
```
