# pygame_pong

## Installation - Linux
```bash
$ git clone https://github.com/spailll/pygame_pong.git
$ cd pygame_pong
$ python3 -m venv venv
$ source ./venv/bin/activate
$ pip install -r requirements.tx
```
## Configuration
To change the size of the screen, change the WIDTH and HEIGHT variables. 

To change the size of the playable area, change the PLAY_AREA_WIDTH and PLAY_AREA_HEIGHT variables. 

To change the size of the paddles, change the PADDLE_WIDTH and PADDLE_HEIGHT variables.

To change the size of the ball, change the BALL_WIDTH and BALL_HEIGHT variables.

To change the speed of the paddles, change the VEL variable.

To change the rate at which the ball increases its speed after every hit of a paddle, change the VEL_INCREASE variable.

To change the frame rate, change the FPS variable.

## Playing
First run the command
```bash
$ python main.py
```
Then, press the SPACE bar to start the game and each subsequent round. Use the W and S keys to control the left side adn the UP and DOWN arrow keys to control the right side.

#### Author - Ben Sailor
#### Email - bsailor@okstate.edu