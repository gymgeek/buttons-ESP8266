for ip in "$@"
do
  ./webrepl_cli.py main2.py $ip:/main.py
  ./webrepl_cli.py client2.py $ip:/client.py
done

