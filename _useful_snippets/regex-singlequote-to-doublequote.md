---
layout: page
date: 2020-06-10
category: Useful Regex
title: Covert Single Quoted YAML to Double Quoted
---

When you need to unify your YAML file to use double quote for strings you can use the following regular expressions and the replacement to use on your favorite editor.

<!--more-->

> The first lines are the regex to find and the last lines are the replace expressions.

### Convert single quoted values to double in YAML

```
:(\s?)'(.*)'

:$1"$2"
```

e.g. `key: 'value'` will be converted to `key: "value"`

### Escape doube quotes inside doube quoted strings in YAML

```
:(\s?)"(.*)([^\\])"(.*)"

:$1"$2$3\\"$4"
```

Needs to be run multiple times until no match is found.

e.g. `key: "field "name" is empty"` will be converted to `key: "field \"name\" is empty"`
