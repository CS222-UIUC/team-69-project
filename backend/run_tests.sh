trap 'kill $(jobs -p) 2>/dev/null' EXIT # cleanup on exit 

python server.py > /dev/null 2>&1 & # run server in background and ignore stdout and stderr

pytest tests


