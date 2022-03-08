# importing time and vlc
import time, vlc, sys, requests

# LOAD CONFIG FILE
config = {}
with open(sys.argv[1], 'r') as configfile:
    for line in configfile:
        s=line.rstrip().split('=')
        config[s[0]] = s[1]

TEMP_DIR=config['BASE_PATH']+'/tempfiles'

vlc_instance = vlc.Instance()

# Initialize instance, player, and media_list
player = vlc_instance.media_player_new()
player.set_fullscreen(True)
list_player = vlc_instance.media_list_player_new()
list_player.set_media_player(player)
list_player.play()

#time.sleep(10)
#media_list.add_media("./videos/1-minecraft.mp4")
#media_list.add_media("./videos/2-fumo_balls.mp4")
#print(media_list.count())
#print(media_list.item_at_index(0))
#list_player.next()
#time.sleep(20)

while 1:

    # CHECK CURRENT LOCATION
    incremented_requests = []
    location_file = open(TEMP_DIR+'/currentlocation', 'r')
    curr_loc = []
    for line in location_file:
        curr_loc.append(line.rstrip())
    location_file.close()

    video_file = open(TEMP_DIR+'/video_list', 'r')
    media_list = vlc.MediaList()
    for line in video_file:
        #vids = vlc_instance.media_new(config['BASE_PATH']+"/videos/"+line.rstrip())
        for location in curr_loc:
            if location == line.split('-')[0]:
                media_list.add_media(config['BASE_PATH']+"/videos/"+line.rstrip())
                # increment video played
                incremented_requests.append(line.split('-')[2])
                break
    list_player.set_media_list(media_list)
    video_file.close()

    player.set_fullscreen(True)
    list_player.next()
    time.sleep(2)
    while player.is_playing():
        for req in incremented_requests:
            requests.post('http://'+config['BASE_URL']+'/api/request/play_counter_increment/'+str(req))
        incremented_requests = []
        time.sleep(0.5)


    #for line in video_file:
    #    player.set_fullscreen(True)
    #    vids = vlc_instance.media_new("./videos/"+line.rstrip())
    #    # setting media to the player
    #    player.set_media(vids)
    #    # play the video
    #    player.play()
    #    time.sleep(2)
    #    # wait time
    #    while player.is_playing():
    #        time.sleep(0.5)

    #    # check for new videos

    #    player.stop()
