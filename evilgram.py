import requests, json, base64, os, sys, telegram, asyncio, datetime, instaloader
from datetime import datetime
from instaloader import ProfileNotExistsException, PrivateProfileNotFollowedException

# GLOBAL INSTANCE OF INSTALOADER
L = instaloader.Instaloader()
MY_INSTAGRAM_USERNAME= ''
# GLOBAL INSTANCE OF BOT
TOKEN = ''
CHAT_ID = ''
bot = telegram.Bot(token=TOKEN)

def request_stories(username):
    # LOAD THE TARGET PROFILE
    profile = instaloader.Profile.from_username(L.context, username)
    
    # DOWNLOAD STORIES
    try:
        if not profile.has_public_story:
            return "There are no new stories."
        raw_stories = L.get_stories([profile.userid])
        
    except ProfileNotExistsException:
        return "Profile not found"
    except PrivateProfileNotFollowedException:
        return "Private or blocked Profile"

    received_stories = []
    # PARSE RECEIVED STORIES
    for story in raw_stories:
        for item in story.get_items():
            if item.is_video:
                story_url=item.video_url
            else:
                story_url=item.url
            story_date = item.date_utc.isoformat()
            story_id = item.mediaid

            story_dict = {
                "id": story_id,
                "date": story_date,
                "url": story_url
            }

            received_stories.append(story_dict)

    # GET RESPONSE STORIES
    output_file = f'{username}.json'

    # SAVE/LOAD FILE
    if os.path.exists(output_file):

        # LOAD SAVED STORIES FROM DISK
        with open(output_file, 'r') as f:
            stored_stories = json.load(f)

        # FILTER NEW STORIES
        new_stories = []

        ids_stored_stories = []
        for stored_story in stored_stories:
            ids_stored_stories.append(stored_story['id'])

        for received_story in received_stories:
            if received_story['id'] not in ids_stored_stories:
                print(f"New story found {received_story['id']}")
                new_stories.append(received_story)
                stored_stories.append(received_story)

        if len(new_stories)>0 :
            #  SAVE UPDATED PROFILE
            with open(output_file, 'w') as f:
                json.dump(stored_stories, f, indent=4)

            return sorted(new_stories, key=lambda x: datetime.fromisoformat(x['date']))
        else:
            return "All new stories have been logged."

    else:
        # IF THERE AREN'T SAVED STORIES
        with open(output_file, 'w') as f:
            json.dump(received_stories, f, indent=4)
            return received_stories
    
async def send_message(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=telegram.constants.ParseMode.HTML)
    except Exception as e:
        print(f"Error sending the message: {e}")

async def main():
    
    # GET USERNAME
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("You must provide a target username.")
        return

    # LOGIN TO INSTAGRAM
    try:
        L.load_session_from_file(MY_INSTAGRAM_USERNAME)
        print("Logged in.")
    except FileNotFoundError:
        print("Session not found.\nExit.")
        return
    

    # # PARSE PROFILE
    new_stories = request_stories(username)
    
    # PRINT OUTPUT
    if isinstance(new_stories, list):
        for story in new_stories:
            message = ""
            message += f"👤 <b>{username}</b>\n"
            message += f"🕑 {story['date']}\n"
            message += f"🏷 {story['id']}\n"
            message += f"{story['url']}\n"
            
            await asyncio.sleep(1)
            await send_message(message)
    elif isinstance(new_stories, str):
        print(new_stories)
        await send_message(f"<b>{username}</b>: <i>{new_stories}</i>")

if __name__ == "__main__":
    asyncio.run(main())
