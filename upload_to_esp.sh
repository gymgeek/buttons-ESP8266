for ip in "$@"
do
  ./webrepl_cli.py main.py $ip:/main.py
  ./webrepl_cli.py client.py $ip:/client.py  
done

