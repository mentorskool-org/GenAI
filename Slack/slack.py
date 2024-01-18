import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain_chain import chain # in langchain_chain library, the environment variables are already loaded so no need to load it again


# Load environment variables from .env file
app = App(token=os.environ.get("BOT_USER_OAUTH_TOKEN"))

#Message handler for Slack
@app.message(".*")
def message_handler(message, say, logger):
    print(message)
    
    output = chain.predict(human_input = message['text'])   
    say(output)


# start your app
if __name__=="__main__":
    SocketModeHandler(app, os.environ.get("APP_TOKEN")).start()