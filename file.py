from datetime import datetime
import re
import os



duration = 5

#Okunacak Dosya İşlemleri
file_name = "/filee.txt"
path = "~/Desktop" 
input_file = os.path.expanduser(path+file_name)

#Güncel Tarih
date_now = datetime.now()
date_now_format =  date_now.strftime("%H:%M:%S")
date_now_convert = datetime.strptime(date_now_format[0:21].replace(',',''),"%H:%M:%S")

#Yazılacak Dosya Adı
output_date_now = date_now.strftime("%d-%m-%Y_%H-%M-%S")
output_file_name = output_date_now +".txt"
output_file_path = '~/Desktop/'
output_file_expanduser =  os.path.expanduser(output_file_path+output_file_name)
output_file_open = open(output_file_expanduser,'a')





try:
    with open(input_file) as f:
        lines = f.readlines()
        for l in lines:
            if l != "\n":
                file_regex =re.findall(r'<(.*?)>', l, re.DOTALL)
                # yazdırılacak değişkenler
                file_date = file_regex[0]
                title = file_regex[1]
                deployer = file_regex[2]
                weblogic = file_regex[6]

                datetime_convert = datetime.strptime(file_date[13:21].replace(',',''),"%H:%M:%S")
                diff = date_now_convert - datetime_convert
                diff = diff.total_seconds()/60
               
                if 'Info' == title or 'Warning' == title :
                    if diff <= duration and diff >= 0 and file_regex[2] == 'Deployer':
                        script = f"<{title}>: ####<{file_date}> <Change Event :  Principal: <{weblogic}> | Object: com.bea:Name=deneme,Type=<{deployer}>,Server=TEB_TES1_1 | Attribute: file | Value: /wls/Oracle12c/domains/tebdomain/servers/AdminServer/upload/bireyselFerhat/app/bireyselFerhat.war\n"
                        print('##',script)
                        output_file_open.write(script)
                    else:
                        pass
                else:
                    pass
except Exception as e:
    #hata alındığı için dosya kapatıldı
    output_file_open.close()
    #Oluşturulan Dosya Silindi
    try:
        if os.path.exists(output_file_expanduser):
            os.remove(output_file_expanduser)
        else:
            pass
    except Exception as error:
        print(error)
    print(e)

    #Hata alması durumunda bir dosya oluşturarak hatayı dosyaya ekliyor.
    output_file_name = "Error_log.txt"
    output_file_expanduser =  os.path.expanduser(output_file_path+output_file_name)
    output_file_open = open(output_file_expanduser,'a')
    error_message = f"{output_date_now} - {str(e)}\n\n"
    output_file_open.write(error_message)
    output_file_open.close()

    



