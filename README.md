<h1>Temp mail client</h1>


Temp mail client is a simple and easy-to-use web application, 
which uses free temp mails services for high level of confidence and privacy. Perfect for creating anonymous 
accounts with email verification or maintaining private correspondence via lots of mails.
Also, you can use TempMailClient with Tor network to achieve maximum anonymity on the network.
Web interface of the client is starting locally, so you don't need to worry about attack from
another hacker`s side.



<h3>How to set up and use:</h3>

<ul>
<li><strong>Download and install docker</strong> (or/and docker desktop) from <a href="https://www.docker.com/">official website</a>.</li>
<li>Run terminal (For windows - <code>Win+R</code> -> <code>cmd</code>).</li>
<li>Download project source code by
```
git clone https://github.com/SamanuelAdmin/tempmailclient
```</li>
<li>Change current directory (<code>cd tempmailclient</code>)</li>
<li>Make docker image via
```
docker image build -t temp_mail_client .
```</li>
<li>Start docker container with command
```
docker run -p 4999:4999 -d temp_mail_client
```</li>
</ul>
<strong>Now your client is running and can be used via <code>127.0.0.1:4999</code></strong>


<i> You can easy change working port to any unoccupied, just change it in last command. For example: <code>docker run -p 80:4999 -d temp_mail_client</code></i>
