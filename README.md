<h1 align="center">
  <img src="https://github.com/Olament/MycologyBot/blob/master/img/mushroom.png" alt="Mushroom logo" width="100">
  <br>
    <a href="https://www.reddit.com/r/mycology/">/r/Mycology</a> Bot
  <br>
</h1>

MycologyBot is a Reddit bot that dedicated to identify mushroom images from [/r/Mycology](https://www.reddit.com/r/mycology/) using the [DeepMushroom API](https://github.com/Olament/DeepMushroom-docker). You can visit [/u/Mycology_Bot](https://www.reddit.com/user/Mycology_Bot) to see this bot in action.

##  Getting Started
Setup your ```praw.ini``` configuration file inside app directory
```ini
[mycology]
client_id=CLIENT_ID
client_secret=CLIENT_SECRET
password=PASSWORD
username=USERNAME
```
Build and run the docker
```cmd
docker build && docker run
```

## Behavior
The bot will reply a post at [/r/Mycology](https://www.reddit.com/r/mycology/) if the post is an ID request and the bot is confident enough in its prediction. The reply will have following format

>These are the Top-5 predictions given by AI.
>
>Species | Probability
>:--|:--
>*sepcies_1*|prob_1
>*sepcies_2*|prob_2
>*sepcies_3*|prob_3
>*sepcies_4*|prob_4
>*sepcies_5*|prob_5
>
>Disclaimer: This bot is not in any way affiliated with r/mycology or the mode team. The prediction given by this bot **is not 100% accurate** and you should not use this information to determine the edibility of mushroom.
> ***
>MycologyBot power by [DeepMushroom](https://github.com/Olament/DeepMushroom) API | [GitHub](https://github.com/Olament/MycologyBot)

## Acknowledge
Mycology Bot is a peronsal project and is not in any way affiliated with [/r/Mycology](https://www.reddit.com/r/mycology/) or the mode team
