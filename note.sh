Get-Content .\hostnames.txt | ForEach-Object { Resolve-DnsName $_ -Type A | Select-Object -ExpandProperty IPAddress }

Get-Content "C:\Scripts\netbios_names.txt" | ForEach-Object { "$_ : $([System.Net.Dns]::GetHostAddresses($_) | Where-Object { $_.AddressFamily -eq 'InterNetwork' } | Select-Object -First 1).IPAddressToString" } | Out-File "C:\Scripts\hostname_ip_addresses.txt"

sudo timedatectl set-ntp off;sudo timedatectl set-timezone Asia/Istanbul ;date;timedatectl

sudo date -s "2025-08-04 16:00:00"


echo "ssh id_rsa.pub" >> ~/.ssh/authorized_keys

ssh-keygen -t rsa -b 4096


cat /opt/nessus/etc/nessus/nessusd.rules

  | tee -a /opt/nessus/etc/nessus/nessusd.rules


202410170946

nuclei -duc -ni -c 500 -es info,low -etags wordpress,wp-plugin -l httpx.txt -o nuclei-result.txt

Windows Big Size Find
Get-ChildItem (Get-Location) -Directory | ForEach-Object { [PSCustomObject]@{ FolderPath = $_.FullName; SizeMB = (Get-ChildItem $_.FullName -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB } } | Sort-Object SizeMB -Descending | Format-Table FolderPath, @{Name='Size (MB)'; Expression={"{0:N2}" -f $_.SizeMB}} -AutoSize
