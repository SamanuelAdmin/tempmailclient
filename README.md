How to set up and use:
1) <strong>Download and install docker</strong> (or/and docker desktop) from <a href="https://www.docker.com/">official website</a>.
2) Run terminal (For windows - <code>Win+R</code> -> <code>cmd</code>).
3) Download project source code by
```
git clone https://github.com/SamanuelAdmin/tempmailclient
```
4) Change current directory (<code>cd tempmailclient</code>)
3) Make docker image via
```
docker image build -t temp_mail_client .
```
4) Start docker container with command
```
docker run -p 4999:4999 -d temp_mail_client
```
<strong>Now your client is running and can be used via <code>127.0.0.1:4999</code></strong>


<i> You can easy change working port to any unoccupied, just change it in last command. For example: <code>docker run -p 80:4999 -d temp_mail_client</code></i>
