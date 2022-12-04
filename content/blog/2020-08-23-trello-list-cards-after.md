---
category: Useful Snippets
date: 2020-08-23
keywords: useful snippets, trello, javascript, browser
slug: trello-list-cards-after
template: post.html
title: List Trello Cards After a Specific One
---

List the cards contents after a given card content inside the browser. Useful to generate a quick report from your Trello board.

<!--more-->

This example lists all the cards placed after then one with "End of June" title.

Open the developer tool in your browser and type in:

```javascript
$(":contains('End of June')")
    .parent("a.list-card")
    .nextAll("a.list-card")
    .find(".list-card-title")
    .toArray()
    .map(a => a.innerText)
```

To build a bullet list:

```javascript
items = $(":contains('End of June')")
    .parent("a.list-card")
    .nextAll("a.list-card")
    .find(".list-card-title")
    .toArray()
    .map(a => a.innerText);

console.log("- " + items.join("\n- "))
```
