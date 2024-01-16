# I. Cài đặt Prometheus và Grafana trên K8S bằng Helm

Ở bài lab [2_setup_k8s_with_kubespray](./2_setup_k8s_with_kubespray.md) chúng ta đã cài Rancher có công dụng quản lý các cụm K8S rồi thì cài Prometheus chi nữa ta? Rancher và Prometheus có mục tiêu sử dụng khác nhau:
- **Rancher**: tập trung vào quản lý cụm Kubernetes, cung cấp một giao diện người dùng cho quản lý cụm và đơn giản hóa triển khai ứng dụng.
- **Prometheus**: chủ yếu là một công cụ giám sát và cảnh báo được thiết kế để thu thập và phân tích số liệu chuỗi thời gian, thường được sử dụng kết hợp với Grafana để hiển thị số liệu.

Phần cài đặt sẽ bao gồm: Prometheus, Alert Manager và Grafana.

[Thực hiện ở node control/local]

### Tạo thư mục chứa file cấu hình cài đặt Prometheus

```shell
cd ~/learn-code/k8s/k8s_lab/
mkdir prometheus
cd prometheus
```

### Download helm-chart của Prometheus

```shell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add stable https://charts.helm.sh/stable
helm repo update
helm search repo prometheus |egrep "stack|CHART"
# Pull helm-chart prometheus-community/kube-prometheus-stack về nhé!
helm pull prometheus-community/kube-prometheus-stack --version 55.5.1
tar -xzf kube-prometheus-stack-55.5.1.tgz
cp kube-prometheus-stack/values.yaml values-prometheus.yaml
```

### Cấu hình file values-prometheus.yaml

Enable ingress của **Alert Manager**:
```yaml
alertmanager:
  ingress:
    enabled: true
    ingressClassName: nginx
    hosts:
      - alertmanager.trungle.com
    paths:
    - /
```

Enable ingress của **Grafana**:
```yaml
grafana:
  # Đổi thành password login vào Grafana mà bạn muốn
  adminPassword: sysadmin@123
  ingress:
    enabled: true
    ingressClassName: nginx
    hosts:
      - grafana.trungle.com
    path: 
      - /
```

Enable ingress của **Prometheus**:
```yaml
prometheus:
  ingress:
    enabled: true
    ingressClassName: nginx
    hosts:
      - prometheus.trungle.com
    paths:
      - /
```

Vậy là đã cấu hình xong file helm, nhanh gọn lẹ =))

### Cài đặt lên K8S

Tạo namespace để dễ maintain:
```shell
kubectl create ns monitoring
```

Install thôi!
```shell
helm -n monitoring upgrade --install prometheus-grafana-stack -f values-prometheus.yaml prometheus-community/kube-prometheus-stack
```

Kết quả như vầy là thành công nha:

    Release "prometheus-grafana-stack" does not exist. Installing it now.
    NAME: prometheus-grafana-stack
    LAST DEPLOYED: Wed Jan  3 11:33:48 2024
    NAMESPACE: monitoring
    STATUS: deployed
    REVISION: 1
    NOTES:
    kube-prometheus-stack has been installed. Check its status by running:
    kubectl --namespace monitoring get pods -l "release=prometheus-grafana-stack"

    Visit https://github.com/prometheus-operator/kube-prometheus for instructions on how to create & configure Alertmanager and Prometheus instances using the Operator.

    trungle@tpp-lab-058:~/learn-code/k8s/k8s_lab/prometheus$ kubectl -n monitoring get all
    NAME                                                               READY   STATUS    RESTARTS   AGE
    pod/alertmanager-prometheus-grafana-stack-k-alertmanager-0         2/2     Running   0          59s
    pod/prometheus-grafana-stack-7cd56fcc89-qtlxs                      3/3     Running   0          69s
    pod/prometheus-grafana-stack-k-operator-85d8b858d8-jxc4b           1/1     Running   0          69s
    pod/prometheus-grafana-stack-kube-state-metrics-865955f67b-4g8hr   1/1     Running   0          69s
    pod/prometheus-grafana-stack-prometheus-node-exporter-c5s5g        1/1     Running   0          69s
    pod/prometheus-grafana-stack-prometheus-node-exporter-x9xlv        1/1     Running   0          69s
    pod/prometheus-prometheus-grafana-stack-k-prometheus-0             1/2     Running   0          58s

    NAME                                                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
    service/alertmanager-operated                               ClusterIP   None            <none>        9093/TCP,9094/TCP,9094/UDP   59s
    service/prometheus-grafana-stack                            ClusterIP   10.233.42.8     <none>        80/TCP                       69s
    service/prometheus-grafana-stack-k-alertmanager             ClusterIP   10.233.45.145   <none>        9093/TCP,8080/TCP            69s
    service/prometheus-grafana-stack-k-operator                 ClusterIP   10.233.44.71    <none>        443/TCP                      69s
    service/prometheus-grafana-stack-k-prometheus               ClusterIP   10.233.16.62    <none>        9090/TCP,8080/TCP            69s
    service/prometheus-grafana-stack-kube-state-metrics         ClusterIP   10.233.51.119   <none>        8080/TCP                     69s
    service/prometheus-grafana-stack-prometheus-node-exporter   ClusterIP   10.233.5.143    <none>        9100/TCP                     69s
    service/prometheus-operated                                 ClusterIP   None            <none>        9090/TCP                     58s

    NAME                                                               DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
    daemonset.apps/prometheus-grafana-stack-prometheus-node-exporter   2         2         2       2            2           kubernetes.io/os=linux   69s

    NAME                                                          READY   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/prometheus-grafana-stack                      1/1     1            1           69s
    deployment.apps/prometheus-grafana-stack-k-operator           1/1     1            1           69s
    deployment.apps/prometheus-grafana-stack-kube-state-metrics   1/1     1            1           69s

    NAME                                                                     DESIRED   CURRENT   READY   AGE
    replicaset.apps/prometheus-grafana-stack-7cd56fcc89                      1         1         1       69s
    replicaset.apps/prometheus-grafana-stack-k-operator-85d8b858d8           1         1         1       69s
    replicaset.apps/prometheus-grafana-stack-kube-state-metrics-865955f67b   1         1         1       69s

    NAME                                                                    READY   AGE
    statefulset.apps/alertmanager-prometheus-grafana-stack-k-alertmanager   1/1     59s
    statefulset.apps/prometheus-prometheus-grafana-stack-k-prometheus       0/1     58s

### Kiểm tra truy cập từ Client

[Thực hiện trên local/control]

Để có thể truy cập vào Prometheus thông qua domain ingress đã tạo thì cần khai báo host trong file hosts ở máy Client:
```shell
sudo nano /etc/hosts

# Khai báo IP và host của 3 ứng dụng này vào
192.168.61.127 grafana.trungle.com
192.168.61.127 alertmanager.trungle.com
192.168.61.127 prometheus.trungle.com
```

Xong rồi thì truy cập xem thử có được hem?

<p align="center"><img src="./images/8_monitoring_with_prometheus_and_grafana/prometheus_domain.png" alt="Prometheus Monitoring"></p>

Grafana có sẵn rất nhiều bộ template dashbaord visually. Ví dụ bạn muốn tạo dashboard để monitoring các Node trong K8S thì có thể tham khảo: https://grafana.com/grafana/dashboards/15759-kubernetes-views-nodes/

Để cài template dashboard này vào Grafana:

1. Truy cập vào Grafana: [grafana.trungle.com](http://grafana.trungle.com/)
2. Vào phần Dashboard ([Home > Dasboard](http://grafana.trungle.com/dashboards)) -> Chọn button **New** -> Chọn **Import**
3. Nhập ID Dashboard template (ở đây là 15759) vào -> chọn **Load** -> Chọn **Import**

Sau khi import, bạn sẽ thấy UI xịn xò như sau:
<p align="center"><img src="./images/8_monitoring_with_prometheus_and_grafana/grafana_dashboard.png" alt="Grafana Dashboard"></p>


# II. Giám sát service trên K8S bằng Prometheus và Grafana

Bây giờ, chúng ta sẽ thử monitoring các thông số của MongoDB database được cài đặt trên K8S.

Các bước thực hiện:
- Tải helm-chart của MongoDB và Mongodb Exporter
- Cấu hình file values.yaml
- Install bằng helm
- Cấu hình Prometheus lấy metrics từ Mongo Exporter
- Tạo dashboard Grafana

### Tải helm-chart

Tìm repo của mongodb:

    trungle@tpp-lab-058:~/learn-code/k8s/k8s_lab/prometheus$ helm search repo mongodb
    NAME                                                    CHART VERSION   APP VERSION     DESCRIPTION                                       
    prometheus-community/prometheus-mongodb-exporter        3.5.0           0.40.0          A Prometheus exporter for MongoDB metrics         
    stable/mongodb                                          7.8.10          4.2.4           DEPRECATED NoSQL document-oriented database tha...
    stable/mongodb-replicaset                               3.17.2          3.6             DEPRECATED - NoSQL document-oriented database t...
    stable/prometheus-mongodb-exporter                      2.8.1           v0.10.0         DEPRECATED A Prometheus exporter for MongoDB me...
    stable/unifi                                            0.10.2          5.12.35         DEPRECATED - Ubiquiti Network's Unifi Controller 

Pull helm-chart:
```shell
helm pull stable/mongodb
helm pull prometheus-community/prometheus-mongodb-exporter
tar -xzf mongodb-7.8.10.tgz
tar -xzf prometheus-mongodb-exporter-3.5.0.tgz
cp mongodb/values.yaml values-mongodb.yaml
cp prometheus-mongodb-exporter/values.yaml values-mongodb-exporter.yaml
```

### Cấu hình các file values.yaml

**values-mongodb.yaml**: Database mình sẽ thực hiện expose port để truy cập thay vì dùng domain ingress như service web khác.
```yaml
mongodbUsername: admin
mongodbPassword: admin
mongodbDatabase: dev
service:
  type: NodePort
  nodePort: 32717
```

**values-mongodb-exporter.yaml**: Thông tin MongoDB dựa vào config ở trên.
```yaml
mongodb:
  uri: "mongodb://admin:admin@mongodb:32717/dev" #mongodb là service name của MongoDB database

serviceMonitor:
  additionalLabels:
    release: prometheus-grafana-stack #relase name của prometheus

service:
  labels: {}
  annotations: {}
  port: 9216
  # type: ClusterIP
  type: NodePort
  nodePort: 32106
  portName: metrics
```

### Cài đặt

```shell
kubectl create ns mongodb
helm -n mongodb upgrade --install mongodb -f values-mongodb.yaml stable/mongodb
helm -n mongodb upgrade --install exporter -f values-mongodb-exporter.yaml prometheus-community/prometheus-mongodb-exporter
```

    trungle@tpp-lab-058:~/learn-code/k8s/k8s_lab/prometheus$ kubectl get all -n mongodb
    NAME                                                        READY   STATUS    RESTARTS   AGE
    pod/exporter-prometheus-mongodb-exporter-75fd68545c-69s7r   1/1     Running   0          17m
    pod/mongodb-5d8f8b6566-sgkq2                                1/1     Running   0          145m

    NAME                                           TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)           AGE
    service/exporter-prometheus-mongodb-exporter   NodePort   10.233.52.147   <none>        9216:32106/TCP    17m
    service/mongodb                                NodePort   10.233.38.237   <none>        27017:32717/TCP   156m

    NAME                                                   READY   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/exporter-prometheus-mongodb-exporter   1/1     1            1           17m
    deployment.apps/mongodb                                1/1     1            1           156m

    NAME                                                              DESIRED   CURRENT   READY   AGE
    replicaset.apps/exporter-prometheus-mongodb-exporter-75fd68545c   1         1         1       17m
    replicaset.apps/mongodb-5d8f8b6566                                1         1         1       145m
    replicaset.apps/mongodb-b4c74d95f                                 0         0         0       156m

Truy cập http://192.168.61.127:32106/metrics sẽ thấy metrics của MongoDB.
<p align="center"><img src="./images/8_monitoring_with_prometheus_and_grafana/mongodb_exporter_metrics.png" alt="MongoDB Exporter Metrics"></p>

### Update prometheus

**values-prometheus.yaml**
```yaml
    additionalScrapeConfigs:
    - job_name: 'mongodb'
      scrape_interval: 5s
      static_configs:
      - targets: ['192.168.61.127:32106']
```

Upgrade prometheus:
```shell
helm -n monitoring upgrade --install prometheus-grafana-stack -f values-prometheus.yaml prometheus-community/kube-prometheus-stack
```

