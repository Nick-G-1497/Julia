## 
#  @package WallpaperUpdater
#  A library for updating your wallpaper via python


import os 

##
# Class used to update your wallpaper
# @note currently only works with gnome
class WallpaperUpdater:

      def __init__ (self):
            pass
      
      ## 
      # Set your wallpaper to whatever photo is given via the path
      def set_wallpaper(self, absolute_path):
        command = 'dconf write \"/org/gnome/desktop/background/picture-uri" \"\'' + absolute_path + "\'\""
        resize = 'dconf write "/org/gnome/desktop/background/picture-options" "\'stretched\'"' 
        os.system(command)
        os.system(resize)



if __name__ == '__main__':
      pass
