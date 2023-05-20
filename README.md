# Video_Conf_App
Open Source Video Conferencing App in Qt

## To install
### For Frontend
* Clone and activate virtual environment
* * `cd frontend/src`
* Run `pip install -r requirements.txt`
* `python3 main.py`

### For Backend
#### Configure RTMP Server
* Run the following commands `sudo apt update` `sudo apt install libnginx-mod-rtmp`
* Edit the configuration file by using the command `sudo nano /etc/nginx/nginx.conf`
* Paste the following in the configuration
```
rtmp {
        server {
                listen 1935;
                chunk_size 4096;
                allow publish 127.0.0.1;
                deny publish all;

                application live {
                        live on;
                        record off;
                        interleave on;
                }
        }
}
```
* Allow the RTMP port in your firewall `sudo ufw allow 1935/tcp`
* Reload the nginx server `sudo systemctl reload nginx.service`
#### Configure Socket Server and REST
* Install Qt Creator from [this link](https://www.qt.io/download)
* Open Qt Server from backend folder as a project in Qt Creator
* Build the project from Qt Creator
