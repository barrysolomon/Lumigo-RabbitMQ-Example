# README for RabbitMQ Kubernetes Setup with Lumigo Tracing

This setup creates several pods that host a RabbitMQ conversation between two Kubernetes pods: a producer and a consumer. The producer sends messages to a RabbitMQ service, and the consumer reads and displays them.

## Prerequisites:

- Kubernetes cluster
- `kubectl` command-line tool
- Docker
- Access to a container registry
- Lumigo 

## Setup:

### 0. Personalize:

Do a global search/replace <span style="color:red">**&lt;your-registry-path&gt;**</span> with your target registry name.  Should be 9 results in the following files for this project:
  k8/rabbitmq-producer.yaml 
  k8/rabbitmq-consumer.yaml 
  README.md

Search/Replace <span style="color:red">**&lt;your-lumigo-token&gt;**</span> in this README.md with your Lumigo token found from the Lumigo UI under Settings->Tracing in the Lumigo UI

### 1. Install the Lumigo Kubernetes operator on your cluster via Helm if not already done so.  

```bash
helm repo add lumigo https://lumigo-io.github.io/lumigo-kubernetes-operator
helm install lumigo lumigo/lumigo-operator --namespace lumigo-system --create-namespace
```
#### See https://docs.lumigo.io/docs/lumigo-kubernetes-operator for more information

### 2. Create a Namespace:

Create a namespace called `rabbitmq`:

```bash
kubectl create namespace rabbitmq
```

### 7. Add Lumigo token secret:

```bash
kubectl create secret generic --namespace rabbitmq lumigo-credentials --from-literal token=<your-lumigo-token>
```

You can view the token to validate by running the following:

```bash
kubectl get secret lumigo-credentials -n rabbitmq -o json  | jq -r '.data.token' | base64 -d
```

### 3. Add Lumigo operator to target namespace

```bash
echo '{
      "apiVersion": "operator.lumigo.io/v1alpha1",
      "kind": "Lumigo",
      "metadata": {
        "name": "lumigo"
      },
      "spec": {
        "lumigoToken": {
          "secretRef": {
            "name": "lumigo-credentials",
            "key": "token"
          } 
        }
      }
    }' | kubectl apply -f - --namespace rabbitmq
```

For the Microsoft Windows command line you should to run the folllowing command
```bash
kubectl apply -f k8/lumigo.yaml -n rabbitmq
```

### 4. Deploy RabbitMQ:

To deploy RabbitMQ as a service within the `rabbitmq` namespace:

```bash
kubectl apply -f k8/rabbitmq-setup.yaml -n rabbitmq
```

### 5. Build Docker Images:

#### Producer Image Build
```bash
pushd src/producer
docker build -t <your-registry-path>/rabbitmq-producer:latest .
docker push <your-registry-path>/rabbitmq-producer:latest
popd
```

#### Consumer Image Build
```bash
pushd src/consumer
docker build -t <your-registry-path>/rabbitmq-consumer:latest .
docker push <your-registry-path>/rabbitmq-consumer:latest
popd
```

---

### 6. Deploy Producer and Consumer:

#### Deploy the producer:

```bash
kubectl apply -f k8/rabbitmq-producer.yaml -n rabbitmq
```

#### Deploy the consumer:

```bash
kubectl apply -f k8/rabbitmq-consumer.yaml -n rabbitmq
```

### 7. Add Lumigo token secret:

```bash
kubectl create secret generic --namespace rabbitmq lumigo-credentials --from-literal token=<your-lumigo-token>
```

You can view the token to validate by running the following:

```bash
kubectl get secret lumigo-credentials -n rabbitmq -o json  | jq -r ".data.token" | base64 -d
```

---

## Usage:

The producer sends messages every 5 seconds to the RabbitMQ service. The consumer consumes and displays them. 

To view logs from the producer:

```bash
kubectl logs -l app=rabbitmq-producer -n rabbitmq
```

To view logs from the consumer:

```bash
kubectl logs -l app=rabbitmq-consumer -n rabbitmq
```

## Cleanup:

To remove all the deployed resources:

```bash
kubectl delete -f k8/rabbitmq-setup.yaml -n rabbitmq
kubectl delete -f k8/rabbitmq-producer.yaml -n rabbitmq
kubectl delete -f k8/rabbitmq-consumer.yaml -n rabbitmq
kubectl delete namespace rabbitmq
```

---

### Validation Commands (in no particular order)
```bash
kubectl get pods -n rabbitmq

kubectl describe pod -l app=rabbitmq-producer -n rabbitmq
kubectl describe pod -l app=rabbitmq-consumer -n rabbitmq

kubectl logs -l app=rabbitmq-producer -n rabbitmq
kubectl logs -l app=rabbitmq-consumer -n rabbitmq
```