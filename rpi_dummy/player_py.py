# importing time and vlc
import time, vlc



# method to play video
# creating a vlc instance
vlc_instance = vlc.Instance()
# creating a media player
player = vlc_instance.media_player_new()
list_player = vlc_instance.media_list_player_new()

list_player.set_media_player(player)

media_list = vlc.MediaList()
media_list.add_media("./videos/1-minecraft.mp4")
media_list.add_media("./videos/2-fumo_balls.mp4")

list_player.set_media_list(media_list)

list_player.play()
time.sleep(10)
# creating a media

#with open('video_list') as video_file:
#    for line in video_file:
#        player.set_fullscreen(True)
#        vids = vlc_instance.media_new("./videos/"+line.rstrip())
#        # setting media to the player
#        player.set_media(vids)
#        # play the video
#        player.play()
#        time.sleep(2)
#        # wait time
#        while player.is_playing():
#            time.sleep(0.5)
#
#        player.stop()
