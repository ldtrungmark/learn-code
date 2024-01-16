1. [sudo] Add user to group "sudo"
- Change user root: su root
- Add user use sudo: adduser trungle sudo
- Switch user: su trungle

2. [mkdir] Create folder:
- Folder: mkdir foler_name
- Sub folder: mkdir -p folder_name/sub_folder

3. [service/systemctl] Manager Service:
- Show all services: service --status-all
- Interact service: service service_name start/stop/restart/reload
- Show status service: service service_name status

4. Folder:
- Create: mkdir folder_name
- Create sub: mkdir -p folder_name/sub_folder
- Copy: cp -r path_folder path_new_folder
- Delete (still exists file): rm -rf path_folder

5. File:
- Create file: touch file_name
- Open file: nano file_name
- Show content file: cat file_name
- Copy file: cp path_file_name path_new_file_name
- Move folder/file: mv path_file_name path_new_file_name
- Delete file: rm path_file
- Find: find . -name file_name
- Link: ln path_file link_name

6. Group:
- Show all group: getent group
- Show user group: getent group group_id/group_name
- Create group: sudo groupadd group_name
- Add user to group: sudo usermod -a -G group_name user_name
- Remove user: sudo gpasswd -d user_name group_name
- Delete: sudo groupdel group_name

7. User:
- Create: sudo adduser user_name
- Change password: sudo passwd user_name
- Show all user: getent passwd
- Show detail user: getent passwd user_name | id user_name
- Switch user: su user_name
- Delete user: sudo userdel user_name

8. Permission:
- Show: getfacl path_name
- Change permisson: chmod u=rwx,g=rwx,o=rwx path_name
- Change permission of user: setfacl -m u:user_name:rwx path_name
- Change permission of group: setfacl -m g:group_name:rwx path_name

9. System infor:
- Infor: uname -a
- Detail release: cat /etc/os-release
- Distribution: lsb_release -a
- CPU: lscpu
- Detail CPU: cat /proc/cpuinfo
- RAM: free -h
- Detail RAM: cat /proc/meminfo
- Disk and file system: df -h
- Disk usage directories: du -h
- Network: ifconfig
- Wifi: iwconfig
- DNS: cat /etc/resolv.conf
- Graphic: lspci
- Time: uptime

10. Port:
- Show TCP connect HTTPS 443: ss -t src :443
- Show TCP listening 8080: ss -lt src :8080
- Sow TCP connect SSH: ss -pt dst :ssh
- Kil port: ss --kill dst ip_connect dport=port
- Find PID: pgrep app_name
- Kill PID: kill pid_app
