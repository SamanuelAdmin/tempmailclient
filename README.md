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
<i> You can use any unoccupied port, just change it in last command. For example: </i>
