import telethon.client.users
from telethon import TelegramClient, events, sync
#CONFIG-----------------------------------------------------------------------------------------------------------------
from telethon.tl import functions
from telethon.tl.types import PeerChannel, PeerUser, InputPeerEmpty
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest, GetDialogsRequest
import asyncio
import flask
import flask_session
from flask import redirect, request, url_for, Flask, render_template,session
from flask_session import Session
api_id = 3607037
api_hash = '0f114b8efffd5ef3d78f6ef30f13ebcd'


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def telegramClientStart():
    api_id=session["api_id"]
    api_hash=session["api_hash"]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient('user', api_id, api_hash,loop=loop)
    client.start()
    return client

def  SearchEntitybyName(name):
    client =  telegramClientStart()
    client.connect()
    entity=  client.get_entity(name)
    client.disconnect()
    print(entity)
def getContacts():
    client = telegramClientStart()
    client.start()
    result = client(functions.contacts.GetContactsRequest(
        hash=0
    ))
    print(result)
def getUserProfile(username):
    client = telegramClientStart()
    user= client.get_profile(username)
    print(user)

def inviteUserToChannel(client,user_id,channel_id):
    user =  client.get_entity(user_id)
    channel =  client.get_entity(channel_id)
    client(InviteToChannelRequest(
        channel,
        [user]
    ))
@app.route("/start", methods=["POST"])
def getGroups():
    try:
        client = telegramClientStart()
        client.connect()
        channel_id=request.form.get("channel_id")
        print(channel_id)
        last_date = None
        chunk_size = 10
        groups = []
        chats=[]
        result = client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0
        ))
        chats.extend(result.chats)

        for chat in chats:
            # try:
            #     if chat.megagroup == True:  # CONDITION TO ONLY LIST MEGA GROUPS.
            #         groups.append(chat)
            # except:
            #     continue
            groups.append(chat)
        for group in groups:
            print(group)
            try:
                all_participants = []
                all_participants = client.get_participants(group)
                for user in all_participants:
                    try:
                        print(user)
                        inviteUserToChannel(client,user.id,channel_id)
                        print(f"{user.username} has been invited")
                    except Exception as e:
                        print(f"error->{e}")
            except Exception as e:
                print(f"error->{e}")
        client.disconnect()
    except Exception as e:
        print(f"error-> {e}")
    return redirect("/")

@app.route("/")
def index():
    # check if the users exist or not
    if not session.get("api_hash"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    return render_template('index.html',api_id=session['api_id'],api_hash=session["api_hash"])


@app.route("/logout")
def logout():
    session["api_id"] = None
    session["api_hash"] = None
    return redirect("/")

@app.route("/login", methods=["POST", "GET"])
def login():
  # if form is submited
    if request.method == "POST":
        # record the user name
        session["api_id"] = request.form.get("api_id")
        session["api_hash"] = request.form.get("api_hash")
        # redirect to the main page
        return redirect("/")
    return render_template("login.html")

# @client.on(events.NewMessage(pattern='(?i).*Hello'))
# async def handler(event):
#       await event.reply('Hey!')

if __name__ == "__main__":

    app.run(debug=True)