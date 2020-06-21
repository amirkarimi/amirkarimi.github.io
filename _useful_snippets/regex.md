---
layout: page
date: 2020-05-10
title: My Useful Regular Expressions
---

## YAML

> The first lines are the regex to find and the last line are the replace expressions.

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
