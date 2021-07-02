from datetime import datetime
import re
import os


class File:

    def __init__(self,input_file_name="/filee.txt",input_file_path="~/Desktop" ,time_diff=5,output_file_path='~/Desktop/',):
        #input file path
        self.input_file =  os.path.expanduser(input_file_path+input_file_name)
        #interval
        self.duration = time_diff
        #the current date
        self.date_now = datetime.now()
        
        #input varaibles
        self.date_now_format =  self.date_now.strftime("%H:%M:%S")
        self.date_now_convert = datetime.strptime(self.date_now_format[0:21].replace(',',''),"%H:%M:%S")
        
        #output variables
        self.output_file_name = self.date_now.strftime("%d-%m-%Y_%H-%M-%S")+".txt"
        self.output_file_expanduser =  os.path.expanduser(output_file_path+self.output_file_name)
        self.output_file_open = open(self.output_file_expanduser,'a')
        self.read_data:list

    #It reads the file and assigns the read data to self.read_data
    def read(self):
        try:
            with open(self.input_file) as f:
                lines = f.readlines()
                self.read_data = lines
                f.close()
                return lines
        except Exception as error:
            message = f"read Error: {e}"
            return message


    #The if condition in the self.read_data variable writes the provided data to the file. Returns False if not provided
    def write(self):
        for l in self.read_data:
            if l != "\n":
                file_regex =re.findall(r'<(.*?)>', l, re.DOTALL)
                file_date = file_regex[0]
                title = file_regex[1]
                deployer = file_regex[2]
                weblogic = file_regex[6]
                #converts the date of the line read from the file to datetime format and finds the difference with the current time
                datetime_convert = datetime.strptime(file_date[13:21].replace(',',''),"%H:%M:%S")
                diff = self.date_now_convert - datetime_convert
                diff = diff.total_seconds()/60
                
                if diff <= self.duration and diff >= 0 and deployer == 'Deployer' and title in ['Info','Warning']:
                    script = f"<{title}>: ####<{file_date}> <Change Event :  Principal: <{weblogic}> | Object: com.bea:Name=deneme,Type=<{deployer}>,Server=TEB_TES1_1 | Attribute: file | Value: /wls/Oracle12c/domains/tebdomain/servers/AdminServer/upload/bireyselFerhat/app/bireyselFerhat.war\n"
                    self.output_file_open.write(script)
        self.output_file_open.close()
        try:
            if script:return True
        except:
            if diff > self.duration and diff < 0:
                message = "Not data found within the specified time range"
                print(message)
            elif deployer != 'Deployer' or title in ['Info','Warning']:
                message = "None of the keywords deployer, info, warning were found"
                print(message)
            return False

    #To delete the generated file at runtime
    def delete_file(self,description):
        try:
            self.output_file_open.close()
            if os.path.exists(self.output_file_expanduser):os.remove(self.output_file_expanduser)
            message =  f"Failed to write data to file\n{description}"
            print(message)
            return message
        except Exception as error:
            print(error)
            return f"{error}"


if __name__ == '__main__':
    file = File()
    try:
        #read file
        read = file.read()
        #write to file
        write = file.write()
        #It was returning False when write() did not meet the if conditions.
        # # Condition to delete the resulting empty file if it returns false
        if write == False:
            file.delete_file("")

    except Exception as e:
        #returns an error if the file is not found and deletes the resulting empty file
        file.delete_file(e)