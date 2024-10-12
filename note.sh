Get-Content .\hostnames.txt | ForEach-Object { Resolve-DnsName $_ -Type A | Select-Object -ExpandProperty IPAddress }

sudo timedatectl set-ntp off;sudo timedatectl set-timezone Asia/Istanbul ;date;timedatectl

echo "ssh id_rsa.pub" >> ~/.ssh/authorized_keys

ssh-keygen -t rsa -b 4096
