## 
#  @package WallpaperUpdater
#  A library for updating your wallpaper via python
#  @todo Make set_wallpaper() work with any and all OS environments. Currently the wallpaper module only works
#  with linux systems which are running a gnome environment, however, WallpaperUpdater should be agnostic of the
#  the environment of which is running and should still work.

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
