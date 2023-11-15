# I. Giới thiệu

## 1. Storage class
Trong Kubernetes (K8s), Storage Classes là một khái niệm quan trọng liên quan đến quản lý lưu trữ. Storage Class định nghĩa cách mà Persistent Volumes (PVs) sẽ được cung cấp và triển khai.

<p align="center"><img src="https://www.kubecost.com/images/kubernetes-best-practices/kubernetes-storage-concepts.png"><i>(Nguồn: <a href="https://www.kubecost.com/kubernetes-best-practices/kubernetes-storage-class">https://www.kubecost.com/kubernetes-best-practices/kubernetes-storage-class</a>>)</i></p>

Tìm hiểu thêm về Storage Class: https://kubernetes.io/docs/concepts/storage/storage-classes

    Retain (reclaimPolicy: Retain):
        Nếu reclaimPolicy được đặt thành Retain, PersistentVolume sẽ không bị xóa khi PVC bị xóa.
        Dữ liệu trên PersistentVolume không được xóa và PV không được phân phối lại.
        Người quản trị hệ thống có trách nhiệm quyết định làm thế nào để xử lý PersistentVolume đã được giữ lại.

    Delete (reclaimPolicy: Delete):
        Nếu reclaimPolicy được đặt thành Delete, PersistentVolume sẽ bị xóa khi PVC bị xóa.
        Dữ liệu trên PersistentVolume sẽ bị xóa và PV có thể được phân phối lại cho các PVC khác.

Trong bài viết này, chúng ta sẽ thực hành cài đặt storage class sử dụng NFS bằng Helm Chart.


## 2. Helm chart

Helm là một công cụ quản lý gói (package manager) cho Kubernetes. Helm giúp đơn giản hóa quá trình triển khai ứng dụng và dịch vụ trên Kubernetes bằng cách đóng gói các tài nguyên của ứng dụng thành các bản cài đặt có thể tái sử dụng gọi là "charts".

Một Helm chart là một bản mô tả của một ứng dụng Kubernetes. Nó chứa tất cả các tài nguyên và cấu hình cần thiết để triển khai ứng dụng trên Kubernetes. Chart có thể bao gồm các tài nguyên như Deployment, Service, ConfigMap, Secret, và nhiều loại tài nguyên khác.

Helm cung cấp khả năng đóng gói, phân phối, và quản lý các ứng dụng Kubernetes, giúp người phát triển và quản trị hạ tầng đơn giản hóa quy trình triển khai và cập nhật ứng dụng trên Kubernetes.

## 3. NFS

NFS (Network File System) là một giao thức mạng cho phép máy tính chia sẻ và truy cập các tệp tin trên mạng. Trong ngữ cảnh của Kubernetes (K8s), NFS thường được sử dụng như một cách để chia sẻ và lưu trữ dữ liệu giữa các nút (nodes) trong một cụm Kubernetes.

Trong Kubernetes, NFS có thể được tích hợp như một dịch vụ lưu trữ (StorageClass) để cung cấp dữ liệu cho các Pod. Khi một ứng dụng chạy trong một Pod trên một nút cụm Kubernetes cần truy cập dữ liệu, NFS có thể giúp chia sẻ tệp tin giữa các nút, giúp đảm bảo rằng dữ liệu có sẵn cho các Pod trên toàn cụm.


# II. Cài đặt NFS trên K8S

Các bước cài đặt gồm:
- Cài đặt NFS Server (trên node master)
- Cài đặt NFS Client (trên node worker)
- Cài đặt helm3 (trên node control/local)
- Cài đặt nfs storage class trên K8S bằng Helm
- Tạo PVC để test

## 1. Cài đặt NFS Server

[Thực hiện trên node master]

Thông thường chúng ta cần có 1 node chuyên dụng chia sẻ phân vùng lưu trữ resource của K8S. Tuy nhiên, tài nguyên máy local có hạn, tôi sẽ sử dụng node master để làm NFS Server chia sẻ phân vùng lưu trữ. Thực hiện chạy các lệnh sau để tạo phân vùng NFS:
```shell
# NFS Server installation
sudo yum install nfs-utils -y
# Create shared folder
mkdir -p /data/delete
mkdir -p /data/retain
# Change permission folder
chmod -R 755 /data
chown -R nobody:nobody /data

sudo systemctl enable rpcbind
sudo systemctl enable nfs-server
sudo systemctl enable nfs-lock
sudo systemctl enable nfs-idmap

sudo systemctl start rpcbind
sudo systemctl start nfs-server
sudo systemctl start nfs-lock
sudo systemctl start nfs-idmap 
# Restart NFS service
sudo systemctl restart nfs-server
```
Cấu hình file /etc/exports để share quyền cho các node trong dải IP 192.168.61.0 để access vào folder data:
```shell
sudo nano /etc/exports
```
Paste nội dung bên dưới vào file exports:

    /data/delete    192.168.61.0/24(rw,sync,no_root_squash,no_all_squash)
    /data/retain    192.168.61.0/24(rw,sync,no_root_squash,no_all_squash)
Sau đó chạy restart lại nfs-server:
```shell
sudo systemctl restart nfs-server
```
Giờ kiểm tra xem 2 thư mục trong data đã được share chưa?
```shell
# 192.168.61.128 là IP của node master - nơi tạo phân vùng data để share
showmount -e 192.168.61.128
```
Thấy kết quả bên dưới thì đã thành công! ✅

    Export list for 192.168.61.128:
    /data/retain 192.168.61.0/24
    /data/delete 192.168.61.0/24


## 2. Cài đặt NFS Client

Cần phải cài đặt NFS Client trên tất cả các worker node để khi tạo Pod trên node đó có sử dụng NFS Storage Class thì node đó có thể mount được phân vùng NFS đã được share bởi NFS Server.

[Thực hiện trên node worker]

```shell
sudo yum install nfs-utils -y
```
Sau đó cũng check xem node worker có thấy foler share không?

    [sysadmin@worker ~]$ showmount -e 192.168.61.128
    Export list for 192.168.61.128:
    /data/retain 192.168.61.0/24
    /data/delete 192.168.61.0/24


## 3. Cài đặt Helm

[Thực hiện trên node control/local]

Trước hết, cần cài đặt Helm trên node control/local để sử dụng:
```shell
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
sudo chmod 700 get_helm.sh
./get_helm.sh
```

Do helm sẽ mặc định dùng chung config của kubectl nếu có, nên ở bước này không cần cấu hình gì thêm cả. Giờ chạy thử xem đã thông chưa nào:

    trungle@tpp-lab-058:~$ helm list
    NAME	NAMESPACE	REVISION	UPDATED	STATUS	CHART	APP VERSION


## 4. Cài đặt NFS bằng Helm

[Thực hiện trên node control/local]

>Nhắc lại: Tất cả resource thực hành K8S tôi sẽ lưu trong folder [k8s_lab](../k8s_lab/)

### Tạo folder nfs-storage
```shell
cd cd k8s/k8s_lab/
mkdir nfs-storage
cd nfs-storage
```

### Download helm chart nfs-client-provisioner
>Lưu ý: Phần này tôi sẽ không dùng repo như ở [bài viết gốc](https://viblo.asia/p/k8s-phan-3-cai-dat-storage-cho-k8s-dung-nfs-RnB5pAw7KPG) vì nó lỗi thời so với version K8S hiện tại.
```shell
# Add chart vào repo
helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/
# Kiểm tra chart có tồn tại
helm search repo nfs-subdir-external-provisioner
# Pull chart về local với chart version
helm pull nfs-subdir-external-provisioner/nfs-subdir-external-provisioner --version 4.0.18
# Giải nén file vừa download về
tar -xzf nfs-subdir-external-provisioner-4.0.18.tgz
```

### Config 2 file value cho reclaim policy "delete" và "retain"
Tạo file value cho storage class có reclaim policy là "delete" và "retain":
```shell
cp nfs-subdir-external-provisioner/values.yaml values-nfs-delete.yml
cp nfs-subdir-external-provisioner/values.yaml values-nfs-retain.yml
```
Thay đổi tham số trong file **values-nfs-delete.yml** như sau:

    # Trong nfs:
    server: 192.168.61.128
    path: /data/delete
    reclaimPolicy: Delete
    # Trong storageClass:
    provisionerName: trungle-nfs-storage-delete
    name: trungle-nfs-delete
    reclaimPolicy: Delete
    archiveOnDelete: false

Thay đổi tham số trong file **values-nfs-retain.yml** như sau:

    # Trong nfs:
    server: 192.168.61.128
    path: /data/retain
    reclaimPolicy: Retain
    # Trong storageClass:
    provisionerName: trungle-nfs-storage-retain
    name: trungle-nfs-retain
    reclaimPolicy: Retain
    archiveOnDelete: true

### Cài đặt trên K8S

Tạo namespace riêng cho Storage Class để dễ quản lý:
```shell
kubectl create ns storage
```
Cài đặt nfs:
```shell
helm upgrade --install nfs-storage-retain --namespace storage -f values-nfs-retain.yml nfs-subdir-external-provisioner-4.0.18.tgz

helm upgrade --install nfs-storage-delete --namespace storage -f values-nfs-delete.yml nfs-subdir-external-provisioner-4.0.18.tgz
```
Kiểm tra kết quả sẽ như thế này:

    trungle@tpp-lab-058:~/learn-code/k8s/k8s_lab/nfs-storage$ kubectl get all -n storage
    NAME                                                                  READY   STATUS    RESTARTS   AGE
    pod/nfs-storage-delete-nfs-subdir-external-provisioner-776d59727vk6   1/1     Running   0          10m
    pod/nfs-storage-retain-nfs-subdir-external-provisioner-56f86fcd4bpt   1/1     Running   0          11m

    NAME                                                                 READY   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/nfs-storage-delete-nfs-subdir-external-provisioner   1/1     1            1           10m
    deployment.apps/nfs-storage-retain-nfs-subdir-external-provisioner   1/1     1            1           11m

    NAME                                                                            DESIRED   CURRENT   READY   AGE
    replicaset.apps/nfs-storage-delete-nfs-subdir-external-provisioner-776d5977db   1         1         1       10m
    replicaset.apps/nfs-storage-retain-nfs-subdir-external-provisioner-56f86fc594   1         1         1       11m


## 5. Tạo PVC để kiểm thử

[Thực hiện trên node control/local]

Giờ để kiểm tra xem NFS-StorageClass có tự động sinh ra PV hay không nhé!

### Tạo file test PVC
```shell
touch test-pvc-delete.yml
```
Sau đó paste nội dung bên dưới vào file rồi lưu lại:

    kind: PersistentVolumeClaim
    apiVersion: v1
    metadata:
        name: test-pvc-delete
    spec:
        storageClassName: trungle-nfs-delete
        accessModes:
            - ReadWriteOnce
        resources:
            requests:
                storage: 10Mi

Kiểm tra xem có PVC và PV tự tạo cho PVC như bên dưới là thành công!

    trungle@tpp-lab-058:~/learn-code/k8s/k8s_lab/nfs-storage$ kubectl get pvc,pv
    NAME                                    STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS         AGE
    persistentvolumeclaim/test-pvc-delete   Bound    pvc-32057e30-5f26-48b8-9687-ff0c113aa0ad   10Mi       RWO            trungle-nfs-delete   59s

    NAME                                                        CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                     STORAGECLASS         REASON   AGE
    persistentvolume/pvc-32057e30-5f26-48b8-9687-ff0c113aa0ad   10Mi       RWO            Delete           Bound    default/test-pvc-delete   trungle-nfs-delete            59s

Tạo file test-pvc-retain.yml rồi làm tương tự.

### Kiểm tra sự khác biệt giữa reclaimPolicy "Retain" và "Delete"

[Thực hiện trên node master]

Cài đặt package **tree** nếu chưa có:
```shell
sudo yum install tree
```
Kiểm tra cấu trúc file đang có trong thư mục **data**:

    [sysadmin@master ~]$ tree /data
    /data
    ├── delete
    │   └── default-test-pvc-delete-pvc-32057e30-5f26-48b8-9687-ff0c113aa0ad
    └── retain
        └── default-test-pvc-retain-pvc-8494c562-a7c9-4e7e-a951-24cd2966caaf

Như bạn có thể thấy, chúng ta tạo 2 PVC cho retain và delete thì ở thư mục data/retain và data/delete cũng đã tạo ra file lưu trữ tương ứng.

Giờ tiến hành xoá đi 2 PVC này trên K8S xem chuyện gì sẽ xảy ra?

    [sysadmin@master ~]$ kubectl delete pvc test-pvc-delete
    persistentvolumeclaim "test-pvc-delete" deleted
    [sysadmin@master ~]$ kubectl delete pvc test-pvc-retain
    persistentvolumeclaim "test-pvc-retain" deleted

Xoá xong rồi, kiểm tra lại dữ liệu trong thư mục data có gì thay đổi không?

    [sysadmin@master ~]$ tree /data
    /data
    ├── delete
    └── retain
        └── default-test-pvc-retain-pvc-8494c562-a7c9-4e7e-a951-24cd2966caaf

Wow, vậy là với reclaimPolicy "Delete" khi xoá PVC sẽ xoá luôn PV. Còn với "Retain" thì chỉ xoá PVC vẫn giữ lại PV. Xem thử PV trong K8S của retain còn không?

    [sysadmin@master ~]$ kubectl get pv
    NAME                                                        CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS     CLAIM                     STORAGECLASS         REASON   AGE
    persistentvolume/pvc-8494c562-a7c9-4e7e-a951-24cd2966caaf   10Mi       RWO            Retain           Released   default/test-pvc-retain   trungle-nfs-retain            7m16s

# III. Tổng kết

Vậy là chúng ta đã biết cách thức hoạt động của NFS tuy việc setup hơi mất thời gian. 

Ưu điểm của NFS (Network File System):
- Chia Sẻ File System: NFS cho phép nhiều máy chủ và máy khách cùng truy cập và chia sẻ các tập tin và thư mục trong hệ thống file.
- Tương Thích Đa Nền Tảng: NFS là một giao thức chuẩn mở và có sẵn trên nhiều hệ điều hành khác nhau, làm cho nó tương thích với nhiều nền tảng.
- Hiệu Suất Khá:
        Trong môi trường mạng nhanh, NFS có thể cung cấp hiệu suất tốt đối với các truy cập đọc và ghi.

Nhược Điểm của NFS:
- Phụ Thuộc vào Mạng: Hiệu suất của NFS có thể bị ảnh hưởng nếu có sự cố trong mạng, đặc biệt là trong các môi trường mạng không ổn định.
- Bảo Mật Thấp: NFS không cung cấp cơ chế bảo mật mạnh mẽ mặc định. Các phiên bản cũ của NFS có thể gặp vấn đề về bảo mật nếu không được cấu hình đúng.
- Khả Năng Mở Rộng Có Hạn: Trong môi trường với nhiều I/O và truy cập cùng một lúc, khả năng mở rộng của NFS có thể bị hạn chế.
- Không Hỗ Trợ Đồng Bộ: NFS có thể gặp vấn đề khi yêu cầu đồng bộ giữa các máy chủ và máy khách.
- Phục Vụ Một File System Đơn: Mỗi lần kết nối với một file system, NFS phục vụ toàn bộ file system đó, không thể chọn lọc cụ thể các thư mục hoặc tập tin.

Bài sau chúng ta sẽ tìm hiểu về loại storage class ngon cơm hơn là Longhorn. Xem nó có gì khác với NFS, bye bye. 🤗