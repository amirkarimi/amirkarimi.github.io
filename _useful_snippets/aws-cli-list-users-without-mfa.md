---
layout: page
date: 2020-06-20
category: AWS
title: List AWS Users Without MFA
---

Lists users who didn't enable MFA.

<!--more-->

```python
import boto3

iam = boto3.resource('iam')

for user in iam.users.all():
  has_any = any(user.mfa_devices.all())
  if not has_any:
    print(user.name)
```
