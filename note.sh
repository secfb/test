Get-Content .\hostnames.txt | ForEach-Object { Resolve-DnsName $_ -Type A | Select-Object -ExpandProperty IPAddress }



echo "ssh id_rsa.pub" >> ~/.ssh/authorized_keys
