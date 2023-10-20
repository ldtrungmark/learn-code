
><code>sudo usermod -aG docker sysadmin</code>

>***[Error] Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?***<br>
Nếu gặp lỗi sau khi gọi lệnh của docker thì thực hiện các bước sau:<br> <code>sudo systemctl restart docker<br>sudo service docker restart</code>


helm upgrade --install --namespace homelab-prod minio-operator operator-5.0.10.tgz

# Show service
kubectl get service minio -n homelab-prod -o yaml