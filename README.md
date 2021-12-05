# Internship_mazars
В работе используется:

 **Haarcascade_frontalface_default.xml** предобученная модель OpenCV
  
  **LBPHFaceRecognizer** модель распознавания лиц. Также необходима для добавления новых фотографий в датасет
  
  **FaceMesh** необходим для предсказания лицевых точек
  
  ## Installation and running

1. Clone the repo
```
$ git clone https://github.com/TheAceHome/Internship_mazars.git
```

2. Create a Python virtual environment named 'venv1' and activate it
```
$ virtualenv venv1
```
```
$ source venv1/bin/activate
```

3. Run the following command in your Terminal/Command Prompt to install the libraries required
```
$ pip3 install -r requirements.txt
```

4. To recognize face masks in real-time video streams type the following command:

```
$ python3 main.py
```
