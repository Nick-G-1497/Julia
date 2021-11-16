##
# @package Unit Test module for the WallpaperUpdater module
import unittest
from WallpaperUpdater import WallpaperUpdater
import subprocess
from time import sleep
## 
# @brief Unit Testing Class for the wallpaper updater module of JuliasClock
class TestWallPaperUpdater(unittest.TestCase):

    ##
    # @brief Test that the wallpaper updater actually updates the wallpaper
    # @detials Given that I have called the set_wallpaper() method from the WallpaperUpdater class, when I check
    # what the current wallpaper is, then I should expect the current wallpaper to be the one which I set it to be
    def test_set_wallpaper(self):
        wp_updater = WallpaperUpdater()

        test_wallpapers_absolute_paths = [
                '/home/francis/Documents/JuliasClock/gist_gray_r/gist_gray_r18.jpg',
                '/home/francis/Documents/JuliasClock/ocean/ocean10.jpg',
                '/home/francis/Documents/JuliasClock/YlOrRd_r/YlOrRd_r0.jpg',
                '/home/francis/Documents/JuliasClock/winter_r/winter_r14.jpg',
                '/home/francis/Documents/JuliasClock/Purples/Purples6.jpg',
                '/home/francis/Documents/JuliasClock/ocean/ocean5.jpg'
                ]
        for path in test_wallpapers_absolute_paths:
            wp_updater.set_wallpaper(path) 
            sleep (10)
            expected_output = 'b\"\'file://' + path + "\'\\n\""
            output = str(subprocess.check_output("gsettings get org.gnome.desktop.background picture-uri", shell=True))
            self.assertEqual(expected_output, output)


if __name__ == '__main__':
    unittest.main()
