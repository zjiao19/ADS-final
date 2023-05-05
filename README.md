# ADS-final
## How to run
```
# install requirements
pip3 install -r requirements.txt
# start server using port 8888
python3 runserver.py --port 8888
```
Access the website `127.0.0.1:8888` in browser.  
## Website
This is the homepage of the website, where you can select a few games you like and your goals.
![Home page](img/index.png)
After clicking the generate recommendations button, you will be redirected to the recommendation result page, which contains a list of similar games based on your input. You can use filters on the side to find more specific results. The reason/explanation for each recommendation is in green under the game title. If you click the game card, you will be redirected to the game information page on [igdb.com](https://igdb.com/) to see more details about the game.
![Result page](img/result.png)
