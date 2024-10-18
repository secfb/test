Get-Content .\hostnames.txt | ForEach-Object { Resolve-DnsName $_ -Type A | Select-Object -ExpandProperty IPAddress }

Get-Content "C:\Scripts\netbios_names.txt" | ForEach-Object { "$_ : $([System.Net.Dns]::GetHostAddresses($_) | Where-Object { $_.AddressFamily -eq 'InterNetwork' } | Select-Object -First 1).IPAddressToString" } | Out-File "C:\Scripts\hostname_ip_addresses.txt"

sudo timedatectl set-ntp off;sudo timedatectl set-timezone Asia/Istanbul ;date;timedatectl

echo "ssh id_rsa.pub" >> ~/.ssh/authorized_keys

ssh-keygen -t rsa -b 4096


  | tee -a /opt/nessus/etc/nessus/nessusd.rules


202410170946


https://share.securefuture.com.tr/portal/r/l/e/dbc045ee-9e0f-4c2e-a3ad-996141e189d9/eb170987-f5e4-4618-9044-5abd7f85e801
