# MQTTPublisher-V1-raw-text-to-json-format-
This is a MQTT publisher program that allow users to browse server's files through a socket connection and able to convert raw text files to json format by declaring the key names, start index and end index. First of all this program is developed using python language and solely for research purpose only. There are still some bugs that need to be fix in the next update.

# How to install
1) The first steps is to git clone by using this command ``git clone https://github.com/zhuangahmacro/MQTTPublisher-V1-raw-text-to-json-format-.git``
2) Install the requirement by using ``pip install -r requirements.txt`` (If requirement is not install properly, please run it on PyCharm)
3) Since this program is using PostgreSQL, user need to download the program and import the `database` file to it. (Database username and password can be change in the `client.py`)
4) Run the `server.py` on your server
5) After `server.py` run successfully, open up `client.py` and enter the Ip address of ur server and click connect. 

# How to use
![preview1](https://user-images.githubusercontent.com/81346846/112430419-15b9f600-8d79-11eb-8646-8c1061337128.png)

On the left panel, all the files on the server is being show to the users. They could simply choose files to be read on the text field area or click on `refresh` button to refresh the server content. Next there are three button which are "JSON, XML and CSV", each one of them represent different types of format that can be filter. 

![preview2](https://user-images.githubusercontent.com/81346846/112431462-86154700-8d7a-11eb-92e7-8500b9bd1c13.png)

After user clicked on "JSON" button, they are able to choose which preset to filter and convert the log files to json format. The idea of the preset is based on the key name, start and end index of the string (By using index slicing, user can customize which string to be convert to json format. Eg: slice the index from 0 to 10 as "Date"). If user want to create a new preset purposely for their data, they could simply press `Create New` and enter their desire string index and save it into database. In this case, when next time they want to access the data, they can choose from the drop down list without creating the preset again and again. 

![previwe3](https://user-images.githubusercontent.com/81346846/112432857-6bdc6880-8d7c-11eb-9c7d-13bcc9d3f1d6.png)
![image](https://user-images.githubusercontent.com/81346846/112433740-a1ce1c80-8d7d-11eb-8549-606719b58651.png)

After user declared all the keynames, start and end index, they can click on `Review JSON` and a new window will be prompt to view their Json formatted file (The raw files is already being converted to json format with the help of index slicing). Next, users can also view the JSON schema by `View JSON Schema`, all the data will now be convert to json schema with the help of `Genson`. 
**This is what i've done on the version 1** 

# Limitation 
1) Now the user input for start and end index can only accept integer value because its using index slicing method. 
2) The database is very vulnerable to SQL injection because the writing method and clear text on python code. 
3) The efficiency of the program can still be improve (For example, reading a text files that more 2000+ lines require 5-10 seconds)
4) Since its using index slicing, the output may have issues when the data is not in organized format. (eg, nested json structured)
5) The view of json schema is still messy because not formatted properly before convert. 
6) Since, i'm using `json dumps` to convert the text files to json format, the json schema for now can only return "string" value to all keynames.   

# Future Improvement
1) Use ReGex instead of index slicing to filter the string. By using ReGex it may take different data types as user input rather than just integer. (If the user input can process other data types, we could apply more validation)
2) To solve the vulnerability of the SQL, we could encrypt the PostgreSQL credentials. Futhermore, we could also export the .py to executable files in order to make code unreadable 
3) To improve the efficiency of the program, we could implement different library instead of writing a long polling code. (The priority of this is not high, because it doesnt affect the main function)
4) In order to have an organized json schema format, we could prettify the output by using `pprint` or other formatter library (Priority is not high)
5) Since the `json dumps` can only return string, maybe i can use `json loads` to return json objects.
6) `Download` function can be implement to download the json file and json schema. (Already in progresss)
