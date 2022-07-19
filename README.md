# myassignment

## Libraries
- python 3.6.10
- tensorflow-cpu latest
- numpy
- opencv
- sqlite3
- shutil
- flask
- heroku cli

## Folders and Files brief description

### folders
- application_data - having two sub folders 'input_image' (for test image) and 'verifying_images' (positive images).
- static - containing css file
- templates - containing main index html file and create html file for register page

### files
- app.py - main flask application run file
- haarcascade_frontalface_default.xml - used for face detection
- init_db.py - initialize sqlite database with schema
- layers.py - containing siamese similarity distance code
-  prepare_dataset.py - file used to prepare anchor and positive dataset for training siamese neural network
- requirements.txt -  containing all open source python libraries
- schema.sql - containing database table schema file
- siamese.ipynb - google colab training jupyter notebook
- utils.py -  python code to load the trained model and authenticate

## Training Data

- No of Negative images – 13233 (http://vis-www.cs.umass.edu/lfw/)

- No of Anchor image – 1

- NO of Positive image - 1

Training folder structure

![training folder structure](https://github.com/Amir22010/myassignment/blob/main/images/trainingfolderstructure.png)

All training instructions present in `siamese.ipynb` google colab file.

[Training notebook](https://colab.research.google.com/drive/1_H8cr-oFkQ2GlFVRyMnIbyKVX3fl5SnP?usp=sharing)

[Trained model](https://drive.google.com/file/d/1CWbtA04ThSqkAc-h9iuXiTxKRzQD85M4/view?usp=sharing)


### Brief naming of components of application

#### main page - index.html

![index](https://github.com/Amir22010/myassignment/blob/main/images/mainpage.png)

#### register page - create.html

![register](https://github.com/Amir22010/myassignment/blob/main/images/register.png)

### How to use the application instructions
- main page - index.html

- register page - create.html

1. first use Register link to register new user's name and face using capture and then Register New User button.
to verify the user registered successfully or not go to home page by clicking on Home Page Link on Top, and check Registered Users area on main page (index.html).

2. Now on main page with camera feed on, place yourself with face seeing webcam and then click on Authenticate button for siamese model authentication process. after 4-5 secs click on Refresh link on main page (index.html) to check results on Results area on main page with date time.