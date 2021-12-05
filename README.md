# Internship_mazars
В работе используются библиотеки:
**pandas**,
**numpy**,
**selenium**,
**finvizfinance**,
**google**,
**email**,
**base64**.

 На почту intern.mazars@gmail.com отправляется письмо в виде
 
 Ticker: AAPL
 
 competitors: 21
 
 Робот ищет информацию на сайте finviz.com. делает скриншот графика и сохраняет html страницы чтобы найти область комании и характеристики компании по тикеру.
 
 В зависимости от области работы компании создаеься уникальная ссылка и собираются данные по компаниям конкурентам.
 
 Обратно на почту присылается график выбранной компании, технические показатели и файл с средними показателями для конкурентных компаний и покахатели компаний в одном файле.
 
 Пример графика находится в папек screenshot, однако он работает для определенных размеров экрана, я пробовал это решить с помощью set_window_size и после кропать изображение по стандартным меркам
 
 Пример присылаемых файлов data.csv и data_with_mean.csv
  
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
