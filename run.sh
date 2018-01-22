if [ ! -d "venv" ]; then
  # no venv directory lets make sure everything is setup
  apt update
  apt install python3 -y
  apt install python3-pip -y
  python3 -m pip install virtualenv
  python3 -m virtualenv venv
  ./venv/bin/python3 -m pip install -r requirements.txt
fi
./venv/bin/python3 run.py
