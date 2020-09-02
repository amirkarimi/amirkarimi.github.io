---
layout:		post
date:     2020-06-20
title:    List AWS Users Without MFA
category: Useful Snippets
keywords:	useful snippets, aws, boto3, AWS IAM, script
---

Lists users who haven't enabled MFA on their AWS accounts.

<!--more-->

```python
import boto3

iam = boto3.resource('iam')

for user in iam.users.all():
  has_any = any(user.mfa_devices.all())
  if not has_any:
    print(user.name)
```
