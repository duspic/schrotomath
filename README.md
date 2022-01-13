# Schrotomath
> I can't believe it's not Photomath™


This is a simple homage project. Not worthy to bear the name of Photomath. It has obvious flaws for which I can't currently muster any more time, but it still somewhat works.
If you don't believe me - try it out: https://schrotomath.herokuapp.com/          *(Look for instructions on how to use it at the bottom of this file)*

It goes without saying, but if you haven't yet seen the ***original*** Photomath - take a look at it:   
https://photomath.com/en/


If you've compared the two, you probably wonder how did my project manage to be so... underwhelming? Well, give me a chance to explain myself:
______________________________________________________________________________________________________________________________________________

# Basic info
The detector is a simple opencv function cv2.findContours(), the recognizer is a barely-deep learning model and I've hand-implemented a parser/solver using the Shunting Yard Algorithm. So there's definitely room for improvement... Still, let me show you what I've done so far:


Let's dive into the repository. The first step is to take a look at the project tree:

```
photomath
├─ app
│  ├─ app.py
│  ├─ backend.py
│  ├─ utils.py
│  ├─ solver.py
│  ├─ templates
│  │  └─ index.html
│  ├─ model
|  |  └─ # tensorflow model files #
│  ├─ requirements.txt
│  └─ Dockerfile
|
|
└─ notebooks
   ├─ augment_dataset.ipynb
   ├─ create_model.ipynb
   ├─ emnist_extraction.ipynb
   ├─ emnis_digits_extraction.ipynb
   ├─ entire_process.ipynb
   ├─ uniform_dataset.ipynb
   |
   ├─ example.png
   ├─ architecture.png
   ├─ solver.py
   
   └─ utils.py

```

The main directory is /app. The same directory is dockerized and its image can be found here: 
https://hub.docker.com/r/duspic/schrotomath 

In the directory, there are a couple of important files to keep in mind.
And, as can be read in the **requirements.txt**, there are a couple of important libraries needed to run the scripts
```
flask 0.12.2
tensorflow 2.7.0
numpy 1.21.3
opencv 4.0.1
```
These are my current versions of the libraries, but I guess newer versions will work for some time. Try it out if you wish to.

There's a main script, **app.py**, which instantiates the Flask app. To keep the main script tidy, I've distributed the code among other scripts; **utils.py**, **solver.py**, **backend.py**. 
The folder **model** is pretty self-explainatory. The entire folder servers as a save-file for tensorflow, from which it loads the weights and architecture of a pre-trained convolutional neural network (CNN). If you find those words somewhat fuzzy, don't sweat about it. In simple terms, the CNN serves as a function, it takes an input and returns an output. The input must be an image of certain shape, and the output is an array which represents what the CNN thinks is in the image.

In the folder **templates** there's a single file **index.html** which contains the layout of the page. There's a javascript part in the file which fetches the camera *client-side* and sends the image to the server for processing.
If you're wondering:
* "Wait. Can't I just make a cv2.VideoCapture() in my python file?" 

The answer is - You can do it locally, but not when the app is running in the cloud.
There's an explanation for that waiting at the bottom of this file


______________________________________________________________________________________________________________________________________________

# The Notebooks

I don't think there's much point in me typing all the steps and details about them. So I placed most of the information alongside related code in the notebooks.
I recommend the **create_model.ipynb** and **entire_process.ipynb**. The first one explains how I built, trained and evaluated my model, where are it's flaws and what are the difficulties surrounding it. The second one takes you trough the entire process which is happening in the background of the app. Open the **example.png** in your image editor of choice, try writing your own equation and run the notebook to see the results. As explained in the create_model.ipynb, some classes are often mispredicted, so try out a couple of examples if you wish.

Other notebooks contain other processes, mainly inspecting and augmenting datasets.

______________________________________________________________________________________________________________________________________________

# Additional info

https://schrotomath.herokuapp.com/  ------>  To use the app, allow it acces to your camera. Find a nice white piece of paper and write clearly the equation, bearing in mind the following limitations
* it only knows characters [0,1,2,3,4,5,6,7,8,9,(,),+,-,*,/] and will probably assume other characters (and any dark blobs) to be one from the list
* multiplication must be explicit, if multiplying an entire bracketed expression (eg. 5*(1+2) and NOT 5(1+2))
* the characters that it knows are written in peculiar ways, get familiar with them to avoid constant mispredictions (MNIST)

![class samples](https://user-images.githubusercontent.com/72471213/149320350-f1677f6f-d78f-44cb-9a58-b68a2d804bab.png)


When you've written the equation, place it in front of your camera. Try to position it in the center, while keeping the remainder of the screen white. The detector will catch on to edges between the paper and table for example, and your equation will go bonkers. It's a good idea to have decent lightning as well. It still won't work as expected, but sometimes it can surprise ;)

![Happy New Year](https://user-images.githubusercontent.com/72471213/149353808-dad39bc3-6ac1-4232-b9a5-166e7061faca.gif)

______________

Regarding the cv2.VideoCapture():
> Q: Why use javascript in index.html to fetch webcam. Can't I just make a cv2.VideoCapture() in my python file?

> A: When deployed on a cloud, the main script will be run on a server somewhere. The user will interact with it trough his own device, but will have access only to what's displayed on the webpage. The method cv2.VideoCapture() tries to find a camera on the machine on which the script is running. So, when you run it locally it will work as planned, but when you deploy it, it will try to find a camera on the **server** machine. The user can have as many cameras as they please, but the script cannot access them trough this method, because the user doesn't run the code. With JS provided in the index.html, users webcam is displayed directly in the front-end, sending only the necessary photo to the server for processing using the "fetch" function

_____________

The dataset is made up of two free datasets found online, EMNIST (https://www.kaggle.com/crawford/emnist) and https://www.kaggle.com/xainano/handwrittenmathsymbols.
From EMNIST I've picked out all the digits and an X symbol, while from the other dataset I've taken only the brackets. All the files were augmented in one way or another (See the notebooks), and many examples were picked out of the dataset. The process was overwhelming and I stopped long before the dataset is optimal. Still, I encourage you to pick up my work and continue rather than going all the way from the beginning. The link to my dataset is: https://drive.google.com/u/0/uc?export=download&confirm=_wbt&id=1FtqqI4EBXyrruvyTw7i-MAUQkW9GnLPn
_____________


There's tons of related quality content on the internet, so if you'd want to build something like this yourself I suggest a couple of easy-to-follow articles:

Making a computer vision app with Flask:
https://towardsdatascience.com/camera-app-with-flask-and-opencv-bd147f6c0eec

Deploying app on heroku:
https://medium.com/featurepreneur/how-to-deploy-a-flask-app-on-heroku-part-1-14782c3068bc
https://medium.com/featurepreneur/how-to-deploy-docker-container-on-heroku-part-2-eaaaf1027f0b
