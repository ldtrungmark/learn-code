# I. Giới thiệu
Metrics Server là một thành phần của Kubernetes (K8s) được sử dụng để thu thập và cung cấp các thông tin liên quan đến tài nguyên (resource metrics) của các Pods và Nodes trong cluster. Nó cung cấp các thông số như CPU và memory usage, số lượng các containers chạy, và nhiều thông tin khác.

Mục đích chính của metrics-server là để hỗ trợ Kubernetes Horizontal Pod Autoscaler (HPA). HPA sử dụng các thông số thu thập từ metrics-server để quyết định khi nào cần phải scale up hoặc scale down số lượng replicas của một Pod để đảm bảo rằng ứng dụng luôn có đủ tài nguyên.

# II. Cài đặt Metrics Server

[Thực hiện ở node control/local]

Trước khi cài đặt, kiểm tra xem cụm K8S có metrics-server chưa nào?

    trungle@tpp-lab-058:~$ kubectl top nodes
    error: Metrics API not available

### Downlod Helm Chart metrics-server
```cmd
cd k8s/k8s_lab
mkdir metrics-server
cd metrics-server
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm pull metrics-server/metrics-server
tar -xzf metrics-server-3.11.0.tgz
```

### Install với Helm Charts

Giờ copy file values.yaml ra để chỉnh sửa một tý khi install không gặp bug này nhé: https://stackoverflow.com/questions/68648198/metrics-service-in-kubernetes-not-working

```shell
cp metrics-server/values.yaml values-metrics-server.yaml
nano values-metrics-server.yaml
```
Thêm **- --kubelet-insecure-tls=true** vào phần **defaultArgs** rồi lưu lại.

Giờ cài đặt thôi:
```shell
helm upgrade --install metrics-server -n kube-system -f values-metrics-server.yaml metrics-server/metrics-server
```

### Kiểm tra

    trungle@tpp-lab-058:~/learn-code/k8s/k8s_lab/metrics-server$ kubectl get pods -n kube-system | grep metrics-server
    metrics-server-df7bb99cb-8pzpd    1/1     Running   0              77m

    trungle@tpp-lab-058:~/learn-code/k8s/k8s_lab/metrics-server$ kubectl top nodes
    NAME     CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
    master   177m         9%     1519Mi          48%       
    worker   159m         8%     1952Mi          57%    

    trungle@tpp-lab-058:~/learn-code/k8s/k8s_lab/metrics-server$ kubectl top pods
    NAME                  CPU(cores)   MEMORY(bytes)   
    pod-longhorn-delete   1m           0Mi             
    pod-longhorn-retain   1m           0Mi

Vậy là cài đặt thành công rồi đó! 🤯


# III. Autoscaling trong K8S

Phạm vi bài viết này chỉ giới thiệu qua Autoscaling có 2 loại HPA và VPA. Sau đó là phầm thực nghiệm xem HPA nó như nào?

Để tìm hiểu kỹ hơn về 2 loại autoscaling này thì xem bài viết này: https://viblo.asia/p/kubernetes-series-bai-16-automatic-scaling-pod-va-cluster-YWOZrGyRlQ0#_vertical-pod-autoscaling-14


## 1. Horizontal Pod Autoscaler (HPA):

Mô tả: HPA là một chức năng của Kubernetes cho phép tự động điều chỉnh số lượng Pod của một Deployment, StatefulSet hoặc ReplicaSet dựa trên các metric như CPU và memory usage.

Cách thức hoạt động: 
- Khi metric như CPU load vượt quá hoặc thấp hơn ngưỡng được đặt trước, HPA sẽ điều chỉnh số lượng Pods.
- Nếu metric thấp hơn ngưỡng, HPA giảm số lượng Pods; ngược lại, nếu metric cao hơn ngưỡng, HPA tăng số lượng Pods.
    
Sử dụng khi: Đối với nguyên tắc điều chỉnh ngang, khi muốn duy trì hiệu suất và tối ưu hóa tài nguyên.

Ví dụ: khi ngưỡng Memory trong pod > 70% thì tạo thêm pod mới cho application.

## 2. Vertical Pod Autoscaler (VPA):

Mô tả: VPA là một chức năng của Kubernetes giúp điều chỉnh kích thước của các container bên trong một Pod dựa trên các metric như CPU và memory usage.
    
Cách thức hoạt động:
- Khi metric vượt quá hoặc thấp hơn ngưỡng được đặt trước, VPA điều chỉnh kích thước (resource requests và limits) của các container trong Pod.
- Nếu metric thấp hơn ngưỡng, VPA giảm kích thước; ngược lại, nếu metric cao hơn ngưỡng, VPA tăng kích thước.
    
Sử dụng khi: Đối với nguyên tắc điều chỉnh dọc, khi muốn tối ưu hóa sử dụng tài nguyên trong các container.

Ví dụ: Model AI train sử dụng 70% memory thì tăng memory cho pod (train model không thể tách nhiều pod nên dùng cách VPA là hợp lý nhất).


## 3. Cấu hình Autoscaling với HPA

Ý tưởng thực nghiệm là:
- Tạo một Deployment gồm: 1 Pod chạy Apache và 1 Service trỏ tới Pod đó.
- Cấu hình HPA cho Deployment:
    + Khi CPU của Pod >= 50% => tăng Pod chạy ứng dụng.
    + Khi CPU của Pod < 50% => giảm Pod chạy ứng dụng.

[Thực hiện trên node control/local]

### Deploy ứng dụng Apache

Tạo thư mục chứa source code demo:
```shell
cd k8s/k8s_lab
mkdir hpa-demo
cd hpa-demo
```
Tạo file **php-apache.yaml** cho Deployment:

    apiVersion: apps/v1
    kind: Deployment
    metadata:
        name: php-apache
        namespace: hpa-demo
    spec:
    selector:
        matchLabels:
            run: php-apache
    replicas: 1
    template:
        metadata:
            labels:
                run: php-apache
        spec:
        containers:
        - name: php-apache
            image: k8s.gcr.io/hpa-example
            ports:
            - containerPort: 80
            resources:
                limits:
                    cpu: 500m
                requests:
                    cpu: 200m
    ---
    apiVersion: v1
    kind: Service
    metadata:
        name: php-apache
        labels:
            run: php-apache
    spec:
        ports:
        - port: 80
        selector:
            run: php-apache

Apply file để tạo Deployment và Service:
```shell
kubectl create ns hpa-demo
kubectl apply -f php-apache.yaml
```
Chờ một chút và xem kết quả:

    trungle@tpp-lab-058:~$ kubectl get all -n hpa-demo
    NAME                              READY   STATUS    RESTARTS   AGE
    pod/php-apache-8669477df6-b4ml6   1/1     Running   0          68m

    NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/php-apache   1/1     1            1           68m

    NAME                                    DESIRED   CURRENT   READY   AGE
    replicaset.apps/php-apache-8669477df6   1         1         1       68m

### Cấu hình HPA cho cái Deployment này
```shell
kubectl autoscale deployment php-apache -n hpa-demo --cpu-percent=50 --min=1 --max=10
```

    trungle@tpp-lab-058:~/learn-code/k8s/k8s_lab/hpa-demo$ kubectl get hpa -n hpa-demo
    NAME         REFERENCE               TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
    php-apache   Deployment/php-apache   <unknown>/50%    1         10        1          61s
    
Nếu thấy kết quả **\<unknown\>/50%** thì chờ một chút để  để cAdvisor thu thập thông tin của Pod thông qua metrics-server.

    trungle@tpp-lab-058:~/learn-code/k8s/k8s_lab/hpa-demo$ kubectl get hpa -n hpa-demo
    NAME         REFERENCE               TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
    php-apache   Deployment/php-apache   0%/50%    1         10        1          61s

### Kiểm thử HPA

Setup coi như xong, giờ tiến hành theo dõi khả năng autoscale thôi.

Mở 2 cửa sổ terminal:
- Một cái để chạy generate load liên tục vào ứng dụng: <code>kkubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -n hpa-demo -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"</code>
- Một cái để theo dõi trạng thái Deployment: <code>kubectl get hpa php-apache --watch -n hpa-demo</code>

Theo dõi log sẽ thấy **TARGET** đạt quá ngưỡng **50%** thì sẽ tạo thêm pod.

    NAME         REFERENCE               TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
    php-apache   Deployment/php-apache   0%/50%    1         10        1          13m
    php-apache   Deployment/php-apache   31%/50%   1         10        1          17m
    php-apache   Deployment/php-apache   250%/50%   1         10        1          17m
    php-apache   Deployment/php-apache   250%/50%   1         10        4          17m
    php-apache   Deployment/php-apache   88%/50%    1         10        5          18m
    php-apache   Deployment/php-apache   69%/50%    1         10        5          18m

Rồi, giờ tắt cái generate load đi xem thế nào?

    php-apache   Deployment/php-apache   69%/50%    1         10        7          25m
    php-apache   Deployment/php-apache   49%/50%    1         10        7          25m
    php-apache   Deployment/php-apache   18%/50%    1         10        7          25m
    php-apache   Deployment/php-apache   0%/50%     1         10        7          25m
    php-apache   Deployment/php-apache   0%/50%     1         10        7          30m
    php-apache   Deployment/php-apache   0%/50%     1         10        2          30m
    php-apache   Deployment/php-apache   0%/50%     1         10        1          30m

Có thể thấy, khi CPU < 50% thì hệ thống autoscale số pod của Deployment xuống về đúng trạng thái ban đầu là 1 pod.

### Clear resource trên K8S
Sau khi thực hành xong, chúng ta có thể xoá đi tất cả resource đã cài đặt nảy giờ trên K8S bằng lệnh <code>kubectl delete all --all -n hpa-demo</code>. Vì tất cả resource nảy giờ đều cài đặt trong namespace này, nên chỉ cần chỉ định xoá tất cả tài nguyên trong namespace là xong!

    trungle@tpp-lab-058:~/learn-code/k8s/k8s_lab/hpa-demo$ kubectl delete all --all  -n hpa-demo
    pod "php-apache-8669477df6-b4ml6" deleted
    service "php-apache" deleted
    deployment.apps "php-apache" deleted
    replicaset.apps "php-apache-8669477df6" deleted
    horizontalpodautoscaler.autoscaling "php-apache" deleted

    trungle@tpp-lab-058:~/learn-code/k8s/k8s_lab/hpa-demo$ kubectl delete ns hpa-demo
    namespace "hpa-demo" deleted


# IV. Tổng kết

Như vậy chúng ta đã biết vai trò và cách sử dụng metrics-server trong K8S. Ngoài ra, cũng vọc qua cách sử dụng HPA đơn giản (tìm hiểu thêm ở đây: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale).

Bài viết sau sẽ cấu hình Load Balancing gồm: nginx, haproxy và keepalive.