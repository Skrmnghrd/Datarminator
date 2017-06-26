
# Datarminator

A script that will be redundant but is written for super lazy people so they could manipulate files easily. 

--scanall funtions add all your files into a log file for easy greping. you could like
./script.py --source / --scanall --verbose

to record all your files on a log file. use bash to format the output nicely on the script. 

./script.py -s /home -d /root/Desktop --scanall --verbose 
-copies all files form /home to /root/Desktop

./script.py -s /home -d /root/Desktop --extensions --preserve --verbose
-input your extension and script will just copy all files with that extension and preserve the file tree to avoid disorientation

./script.py -m /home -d /root/Desktop --scanall --verbose
-moves all in home to /root/Desktop

# Might Contain some bugs.
