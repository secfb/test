Get-Content .\hostnames.txt | ForEach-Object { Resolve-DnsName $_ -Type A | Select-Object -ExpandProperty IPAddress }



echo "ssh id_rsa.pub" >> ~/.ssh/authorized_keys



https://plugins.nessus.org/v2/nessus.php?f=all-2.0.tar.gz&u=4e2abfd83a40e2012ebf6537ade2f207&p=29a34e24fc12d3f5fdfbb1ae948972c6'
