import os
from colorama import *

def check_rights_and_user(jobs):
    if os.getuid() == 0:
        job_without_user_field = []
        for job in jobs:
            if job.user == '':
                job_without_user_field.append(job)
        print(f"{Back.RED}{Style.BRIGHT}[WARNING]{Style.RESET_ALL}{Fore.RED}{Style.BRIGHT} It appears that you lanch Taskmaster as root.{Style.RESET_ALL}")
        if len(job_without_user_field) == 0:
            print(f"{Back.RED}{Style.BRIGHT}[WARNING]{Style.RESET_ALL}{Fore.RED}{Style.BRIGHT} Currently, there is no job directly impacted by this. But be root with this script can lead to severe security issues.{Style.RESET_ALL}")
            choice = input(f"{Back.RED}{Style.BRIGHT}[WARNING]{Style.RESET_ALL}{Fore.RED}{Style.BRIGHT}{Fore.RED}{Style.BRIGHT} Are you sure you want to continue ? [Y/Every key to refuse]: {Style.RESET_ALL}")
            if choice.lower() == 'y' or choice.lower() == 'yes':
                print(f"{Back.RED}{Style.BRIGHT}[WARNING]{Style.RESET_ALL}{Fore.RED}{Style.BRIGHT}{Fore.RED}{Style.BRIGHT} At your own risk.{Style.RESET_ALL}")
                return False
            else:
                print(f"{Fore.GREEN}{Style.BRIGHT}The program will exit. Bye.{Style.RESET_ALL}")
                exit(0)
        elif len(job_without_user_field) != 0:
            print(f"{Back.RED}{Style.BRIGHT}[WARNING]{Style.RESET_ALL}{Fore.RED}{Style.BRIGHT} Currently, the job(s)...{Style.RESET_ALL}")
            for job in job_without_user_field:
                print(f'{Style.BRIGHT}\n- {job.name}\n{Style.RESET_ALL}')
            print(f"{Back.RED}{Style.BRIGHT}[WARNING]{Style.RESET_ALL}{Fore.RED}{Style.BRIGHT} ...coul'd be impacted by root launch.{Style.RESET_ALL}")
            choice = input(f"{Fore.RED}{Style.BRIGHT}Are you sure you want to continue ? [Y/Every key to refuse]: {Style.RESET_ALL}")
            if choice.lower() == 'y' or choice.lower() == 'yes':
                print(f"{Fore.BLUE}{Style.BRIGHT}We'll set the job(s) to be launched as root.{Style.RESET_ALL}")
                for job in job_without_user_field:
                    job.user = 'root'
                print(f"{Fore.GREEN}{Style.BRIGHT}Done.{Style.RESET_ALL}")
                return False
            else:
                print(f"{Fore.GREEN}{Style.BRIGHT}The program will exit. Bye.{Style.RESET_ALL}")
                exit(0)
        else:
            print(f"{Back.RED}{Style.BRIGHT}[ERROR]{Back.RED}{Style.BRIGHT} Something went wrong. The program will exit.{Style.RESET_ALL}")
            exit(1)
    else :
        current_username = os.getlogin()
        for job in jobs:
            if job.user == '':
                job.user = current_username

