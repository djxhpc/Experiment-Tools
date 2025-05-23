import os 
import subprocess 


commands = [
    'python3 RNN.py --num_layers=2 --hidden_size=64 --batch_size=16 --num_epochs=300',
    'python3 GRU.py --num_layers=2 --hidden_size=64 --batch_size=16 --num_epochs=300',
    'python3 ResNet-18.py --batch_size=16 --num_epochs=300',
    'python3 ResNet-50.py --batch_size=16 --num_epochs=300'

]

# Open a file to save the results
with open('CCTVresult0308.txt', 'w') as f:
    # Loop through each command
    for cmd in commands:
        count = commands.index(cmd) + 1
        print("Now executing command", count, "out of", len(commands))

        # Execute the command and capture the result
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Write the command and its output to the file
        f.write(f'Command: {cmd}\n')
        f.write(f'Stdout: {result.stdout.decode()}\n')
        f.write(f'Stderr: {result.stderr.decode()}\n')
        f.write('------------------------\n')
        
        # Parse the output to find the highest accuracy
        accuracies = []
        lines = result.stdout.decode().split('\n')
        for i, line in enumerate(lines):
            if 'phase: val' in line:
                accuracy_line = lines[i+1]
                accuracy_str = accuracy_line.split('accuracy :')[1].strip().split()[0] # Extract only the numeric part
                accuracy = float(accuracy_str)
                accuracies.append(accuracy)
        
        if accuracies:
            max_accuracy = max(accuracies)
            f.write(f'Maximum accuracy: {max_accuracy}\n')
        else:
            f.write('No accuracy found\n')
import smtplib
from email.mime.text import MIMEText
#讀取檔案
with open("CCTVresult0308.txt", "rb") as file:
    filecontent=file.read()
mime=MIMEText(filecontent, "base64", "utf-8")   
mime["Content-Type"]="application/octet-stream"   
mime["Content-Disposition"]='attachment; filename="CCTVresult0308.txt"' 
mime["Subject"]="訓練完成了" #撰寫郵件標題
mime["From"]="暱稱" #撰寫你的暱稱或是信箱
mime["To"]="XXXXXX@mail.nkk.edu.tw" #撰寫你要寄的人
mime["Cc"]="XXXXXXXXX@gmail.com" #副本收件人
msg=mime.as_string() #將msg將text轉成str
print(msg)
smtp=smtplib.SMTP("smtp.gmail.com", 587)  #googl的ping
smtp.ehlo() #申請身分
smtp.starttls() #加密文件，避免私密信息被截取
smtp.login("XXXXXXXXX@gmail.com", "XXXX xxxx xxxx xxxx") 
from_addr="XXXXXXXXX@gmail.com"
to_addr=["XXXXXX@mail.nkk.edu.tw"]
status=smtp.sendmail(from_addr, to_addr, msg)
if status=={}:
    print("郵件傳送成功!")
else:
    print("郵件傳送失敗!")
smtp.quit()
