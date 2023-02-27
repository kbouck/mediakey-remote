# mediakey-remote
Forward local media key events to remote streaming media control APIs

# install

```bash
pip install

```

# start/stop
```
sudo systemctl start mediakey-remote.service 
sudo systemctl stop mediakey-remote.service 
```

# auto-start on boot
```
sudo systemctl enable mediakey-remote.service 
```

# config
```bash
/etc/opt/mediakey-remote/config.toml
```

# logs
```bash
/var/opt/mediakey-remote/logs/mediakey-remote.log
```

# build
```bash
# enable your venv
# pip install keyboard soco toml pyinstaller 
pyinstaller mediakey-remote.py --onefile
```


