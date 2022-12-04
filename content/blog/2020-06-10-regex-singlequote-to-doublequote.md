---
category: Useful Snippets
date: 2020-06-10
keywords: useful snippets, regex, yaml, convert
slug: regex-singlequote-to-doublequote
template: post.html
title: Covert Single Quoted YAML to Double Quoted
---

You can use these regular expressions and replacement expressions inside your favorite editor when you need to unify your YAML file to use double quote for all strings.

For example converting:

```yaml
key1: value 1
key2: 'value 2'
key3: 'value "3"'
```

To:

```yaml
key1: "value 1"
key2: "value 2"
key3: "value \"3\""
```

<!--more-->

> The first lines are the regex to find and the last lines are the replace expressions.

### Convert single quoted values to double in YAML

```
:(\s?)'(.*)'

:$1"$2"
```

e.g. `key: 'value'` will be converted to `key: "value"`

### Escape double quotes inside double quoted strings in YAML

```
:(\s?)"(.*)([^\\])"(.*)"

:$1"$2$3\\"$4"
```

Needs to be run multiple times until no match is found.

e.g. `key: "field "name" is empty"` will be converted to `key: "field \"name\" is empty"`
