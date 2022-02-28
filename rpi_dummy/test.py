# importing time and vlc
import time, vlc

BASE_DIR='/home/pi/Desktop/rpi_dummy'
BASE_DIR='.'

vlc_instance = vlc.Instance()

# Initialize instance, player, and media_list
player = vlc_instance.media_player_new()
player.toggle_fullscreen()
list_player = vlc_instance.media_list_player_new()
list_player.set_media_player(player)
#list_player.play()

media_list = vlc.MediaList()
media_list.add_media("./videos/1-minecraft.mp4")
media_list.add_media("./videos/2-fumo_balls.mp4")
list_player.set_media_list(media_list)
list_player.next()
player.toggle_fullscreen()
player.toggle_fullscreen()
time.sleep(20)

