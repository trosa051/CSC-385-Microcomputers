TJ Rosario-Rosa

Include a file README.txt with your name at the top outlining what files you are submitting and what I should look at for grading.
MAKE SURE TO INCLUDE INSTRUCTIONS IN THE FINAL ASSN5 README.txt AND IN DOCUMENTATION
COMMENTS IN THE TOP OF THE SKETCH THAT TELL ME HOW TO RUN IT FOR TESTING.
IF I HAVE TO FISH THROUGH THE CODE TO DETERMINE THAT, IT WILL COST POINTS.
Also, please provide links or other references to any starting-point sketches or libraries used by your project.


This project is the framework for running distance based artificial intelligence algorithms and Arduino integration in processing's environment. 
Currently movement is manual and there is no serial communication/AI code attached. I plan on adding those features by late Wednesday. 

My apologies for the later than expected submission. Hope you like it! Thanks for another great semester.

INTERACTION:
keyPressed():
    mousePressed:
        Drag the screen around
    mouseWheel:
        Zoom into the simulation to get a better look at things
    '0' or '1':
        change cameras. 0 *should* be top down orthogonal and 1 is a 3rd person camera
    'Up', 'Down', 'Left', "Right':
        Move the mailman
    'R':
        Experimental!! Resets movement back to original points. Breaks 3rd person camera temporarily 

http://gdsstudios.com/processing/libraries/ocd/reference/
add_library('ocd')

KNOWN ISSUES:
- The random nature of the streets will not always produce a great looking result. Resetting is currently the best way to get a better street layout.
- Processing Memory leak issue
- Pressing escape can lead to odd startup issues on the next run. To fix, just try opening it again.