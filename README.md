# W-node

W-node on minun ensimmäinen sensori node toteutettuna micropythonilla. Tällä luetaan lämpösensoreita ja ohjataan lamppuja
<br>
# Johonkin tähän voisin kirjoittaa siitä mikä tämä rakenne on, että minulla on yksi micropython projekti jossa on monta härveliä sisällä
<br>
<br>
# Muutamia havaintoja

\- TTGO display ei toimi SPIRAMin kanssa vaikka ainakin SPI flashia pitäisi läytyä \-\-\> No käytin nyt ihan standardi EPS32 kirjastoa \(esp32\-20210902\-v1\.17\.bin\)
\- Jostain syystä sertifertifikaatillinen MQTT communikaatio ei suostu toimimaan samaa aikaa bluethooth haun kanssa\. Tätä selvitän nyt
\- Stubsien päivittämiseksi pitää päivittää halutut kirjastot Pylance ja \.pylintrc varten\. Tässä suorat linkit niihin
    - .vscode\settings.json
    - .pylintrc