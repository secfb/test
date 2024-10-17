Get-Content .\hostnames.txt | ForEach-Object { Resolve-DnsName $_ -Type A | Select-Object -ExpandProperty IPAddress }

Get-Content "C:\Scripts\netbios_names.txt" | ForEach-Object { "$_ : $([System.Net.Dns]::GetHostAddresses($_) | Where-Object { $_.AddressFamily -eq 'InterNetwork' } | Select-Object -First 1).IPAddressToString" } | Out-File "C:\Scripts\hostname_ip_addresses.txt"

sudo timedatectl set-ntp off;sudo timedatectl set-timezone Asia/Istanbul ;date;timedatectl

echo "ssh id_rsa.pub" >> ~/.ssh/authorized_keys

ssh-keygen -t rsa -b 4096


  | tee -a /opt/nessus/etc/nessus/nessusd.rules



https://share.securefuture.com.tr/portal/r/l/e/ab6d2203-f88c-4321-9c53-03d35b9dd156/c3fca58f-64a3-44a9-8326-b7ded0ff0d0f
