#! /bin/bash


echo "
==========================================================================
Julia's Clock Automated Documentation Updater
 --- ver 1.5
 =========================================================================
                                                            .....
                                                    ..:-:....
                                                   ...:%+:::-..
                                                 .....:::**-:...
                                               .....::::**=-::...
                                            .......:=#=#@##+-*:....
                                         .........:::=#######-::......
                                       .......::::::-+#######=:::........
                                    .....:-==-:::=---=*#####=--::#::::::=..
                                  ......::+*#*#-=#################-::-:-=:..
                               .........:::########################*####==..
                      ................:::--=%###########################::...
                   .................:::@##@###########################@-::...
                 ....:-::::::::::::::::-=###############################-:::.
                ....::%-:@::==::::::::-@##################################%:.
               .....:::-+##==##+*=-::-###################################-:..
            .......::::=*##########===####################################+:.
        ........:::::-+#############@+###################################-:..
    ...........::-=-==%##################################################:...
 ....:-::::::::::=*#####################################################::...
:::-::#-:-=-=-=%+@####################################################-::....
 .....:....::::::-+#####################################################::...
     ..........::=---=%##############@###################################::..
         ........::::++*############*+###################################-:..
             ......::::**##########=-=####################################+:.
               .....:::-**#==*#=#-:::-+##################################-::.
                 ...:==:::::-=::::::::=###################################@*.
                  ...:=::...::::.::::::-*###############################-:::.
                   ..................::+#@+###########################+-::...
                        ..............::::-=############################*:...
                                ........:::########################=%#@#+:..
                                  .......:-#*==-=##############+##-::::-=:..
                                     ....:::--::::::-=######=-::::::...::..
                                       .........::::=@#######=:::........
                                          ........:::+######%=::.....
                                             ......::=-=@##=:::....
                                                .....:::-*=:::...
                                                  ....::-=@=:...
                                                   ...::%::.:..
                                                    ..:-:...
                                                      ...
Art by Rodrigo in Brazil (https://www.asciiart.eu/art-and-design/fractals)
==========================================================================
Dependancies
    -bash (https://www.gnu.org/software/bash/)
    -doxygen command line tool (https://www.doxygen.nl/index.html)
    -firefox (https://www.mozilla.org/en-US/firefox/new/)                                                                               
==========================================================================                           
# Press Enter to Update the Documentation                                                                            
"
read response;
rm -rf Documentation;
mkdir Documentation;
mv assets/Doxyfile .;
mv assets/logo.png .;
mv assets/doxygen-awesome-css .;
cd include;
doxygen Doxyfile;
mv html Documentation/;
mv doxygen-awesome-css assets;
mv Doxyfile assets;
mv logo.png assets;
mv latex Documentation/;
cd Documentation;
firefox html/index.html;

