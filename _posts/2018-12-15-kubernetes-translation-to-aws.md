---
layout:     post
title:      "Kubernetes translated to AWS"
date:       2018-12-15 17:52
keywords:    "Kubernetes, k8s, AWS, ECS, cloud, docker, comparison"
---

I use analogy whenever I need to explain something in the clearest and fastest possible way. Gaining knowledge in an abstract manner is hard and costly. Using existing knowledge as a foundation speeds up the learning process and prevents misunderstandings. When a C# developer, for instance, asks me what's `flatMap` in Scala, I'll ask if they know what's `SelectMany`? If they do, explaining how `flatMap` works on non-list types would be far faster and easier.

Now let's do this with Kubernetes and AWS. Let's see what are the Kubernetes components closest equivalents in AWS.

The point is that an analogy doesn't provide a deep understanding of a new concept, but it provides the foundation to speed up the learning process. So don't expect a conclusive 1:1 mapping from Kubernetes elements to AWS ones.

<!--more-->

## Node

_AWS equivalent: **[EC2](https://aws.amazon.com/ec2/)**_

[Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/) in K8s are basically machines, either virtual or physical. 

## Pod

_AWS equivalent: **[EC2](https://aws.amazon.com/ec2/)** or **[ECS Task](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html#welcome-task-sched)**_

A [Pod](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/) is simply the smallest compute unit in Kubernetes. Think of a Docker container.

## Deployment

_AWS equivalent: **[ASG](https://docs.aws.amazon.com/autoscaling/ec2/userguide/AutoScalingGroup.html)** or **[ECS Task definition](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)**_

A [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) object describes the desired state for Pods and ReplicaSets. As an example, you can specify a docker image and the number of replicas you want to be run within your cluster in a Deployment object and apply it. Kubernetes will take care of the rest.

## Service

_AWS equivalent: **[NLB](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html)** or/and **[CLB](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/introduction.html)**_

A [Serivce](https://kubernetes.io/docs/concepts/services-networking/service/) sits in front of the Pods and route the traffic to them. Service in k8s is far more abstract and capable than anything available in AWS at the moment. It can also utilize AWS (or other clouds) load balancers to expose the applications.

## Volume

_AWS equivalent: **[ELB](https://aws.amazon.com/ebs/)**_

[Volume](https://kubernetes.io/docs/concepts/storage/volumes/) in k8s is very similar to Docker volumes in terms of interface but it's more abstract. For example, you can use AWS EBS as a volume back-end in k8s.

## Namespace

_AWS equivalent: **[VPC](https://aws.amazon.com/vpc/)**_

K8s allows defining multiple virtual clusters backed by the same physical cluster using [Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/).

## Summary

There are two paths we can map the Kubernetes components to AWS ones through:

1. **EC2**: Each VM runs an instance of the application
2. **ECS**: Runs the applications as Docker containers and distribute the load among EC2 instances in the cluster

{: class="center" }
| K8s component | AWS (EC2 Path)| AWS (ECS Path) |
|---------------|---------------|----------------|
|Node           |EC2|EC2|
|Pod            |EC2|Task|
|Deployment     |Auto scaling group|Task Definition|
|Service        |Load balancer|Load balancer|
|Volume         |EBS|EBS|
|Namespace      |VPC|ECS Cluster|
