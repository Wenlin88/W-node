# W-node

W-node on minun ensimmäinen sensori node toteutettuna micropythonilla. Tällä luetaan lämpösensoreita ja ohjataan lamppuja
<br>
## **Uusia ominaisuuksia ja ideoita**
<br>
* [ ] <span class="colour" style="color:var(--vscode-unotes-wysText)"><span class="font" style="font-family:var(--vscode-editor-font-family)"><span class="size" style="font-size:1em">HA luokkaan yksinkertainen funktio millä voi lisätä sensorien funktioita näkyväksi HA devicessä yksinkertaisesti. Myös olemassa oleva ruuvitag esittelyn voisi muuttaa tähän muotoon</span></span></span>

## Muutamia havaintoja

\- TTGO display ei toimi SPIRAMin kanssa vaikka ainakin SPI flashia pitäisi läytyä \-\-\> No käytin nyt ihan standardi EPS32 kirjastoa \(esp32\-20210902\-v1\.17\.bin\)
\- Jostain syystä sertifertifikaatillinen MQTT communikaatio ei suostu toimimaan samaa aikaa bluethooth haun kanssa\. Tätä selvitän nyt
\- Stubsien päivittämiseksi pitää päivittää halutut kirjastot Pylance ja \.pylintrc varten\. Tässä suorat linkit niihin
    - .vscode\settings.json
    - .pylintrc