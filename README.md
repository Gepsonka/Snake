# Snake
Simple snake game with pygame

### Install

Run command to install dependencies:

```bash
pip3 install -r /path/of/game/requirements.txt 
```


### Run

After you have installed the dependencies start
the game with

```bash
python3 /path/to/game/main.py
```

After you started it wait for both the game and gesture recognition to start, then you can play the game.


### How to play

You can control the game either with the arrow
keys or with the corresponding gestures.

The goal is to reach a good score.

You can gather points by eating the purple food on the field.

The game ends if you eat yourself. (run into yourself...classical snake game)


### Gestures

#### Peace

![peace](https://cdn.shopify.com/s/files/1/0074/7598/6491/products/peace-lf-3_grande.jpg?v=1548153577)

Set the snake's direction to right.


#### Okay


![okay](https://proofreadmyessay.co.uk/wp-content/uploads/2019/12/Tauchzeichen-Okay-Diving-Sign-Okay.png)

Set snake's direction to left.


#### Thumbs up

![thumbs up](https://www.nicepng.com/png/detail/7-74503_free-image-on-pixabay-youtube-thumbs-up-png.png)

Set snake's direction upwards


#### Thumbs down

![thumbs down](https://jf-staeulalia.pt/img/other/66/collection-thumbs-down-cliparts-31.png)

Set snake's direction downwards


##### Comment to the project

I know... the implementation of the program is terrible.

The original plan was to start in two different processes the gesture detection and the game and give them a shared object so they can communicate with each other. But the problem with this idea is that the pygame.Surface object is unpickleable which is a problem because if a process is made with the multiprocessing module, the process's object needs to be pickled to make the processes be able to communicate with each other (brief explanation...I do not want to go into the details)  so I started the gesture recognition processe inside th Game class which is a terrible practice but the only way to make this thing work (or as it seems, and I do not want to deal with the lowest-level stuff like forking/spawning processes and configuring them, because it would make even harder to deal with the shared data).