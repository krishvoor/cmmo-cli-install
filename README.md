## Installing Cost Management Metrics Operator via Cli

Instead of using OpenShift Container Platform web console to install and operator, we can install CMMO from OperatorHub from CLI. This README assumes you have valid KUBECONFIG or cluster-admin privileges

### Creating an OperatorGroup, Namespace & Subscription

Will create a Namespace, OperatorGroup & associate Subscription to deployed operator:

```
$ 
$ oc cluster-info
$ oc create -f operator_group.yml
$ oc project costmanagement-metrics-operator 
$ oc get OperatorGroup
$ oc get subscriptions
$ oc get installPlan
$
```

### Creating a secret for respective user
This section assumes you have account & relevant access in
https://console.redhat.com/

```
$ 
$ oc create -f secret.yaml
$
```

### Creating a CostManagementMetricsConfig CRD

```
$
$ oc create -f CostManagementMetricsConfig.yml
$ oc get CostManagementMetricsConfig 
$
```