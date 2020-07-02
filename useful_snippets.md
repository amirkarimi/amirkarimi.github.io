---
layout: page
title: Useful Snippets
permalink: /useful_snippets/
order: 1
---

{% assign useful_snippets = site.useful_snippets | sort: 'date' | reverse %}
{% for useful_snippet in useful_snippets %}
  <a href="{{ useful_snippet.url }}">
    {{ useful_snippet.title }}
  </a>
{% endfor %}

<!-- {% assign groups = site.useful_snippets | group_by: "category" %}
{% for group in groups %}
## {{ group.name }}
{% assign snippets = group.items | sort: 'date' | reverse %}
{% for useful_snippet in snippets %}
<a href="{{ useful_snippet.url }}">{{ useful_snippet.title }}</a>
{% endfor %}
{% endfor %} -->
