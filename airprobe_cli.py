import requests
import argparse
import json
 

def createUser(args):
	username,password = args
	try:data = json.load(open('data.json'))
	except:data = {}
	if data.get(username):print("User already exists !")
	else:
		data[username] = password
		json.dump(data,open('data.json','w'))
	
def loginUser(args):
	username,password  = args
	try:data = json.load(open('data.json'))
	except:data = {}
	if data.get(username,None)==password:
		ch = 0
		choiceScreen= """
		Choose Options
		1. Create User
		2. Update User
		3. Delete User
		4. Read All User
		5. Weather Info
		6. Exit
		Choice: """
		while ch!=6:
			ch = int(input(choiceScreen))
			if ch==1: 
				usern = input("Enter username: ")
				passw = input("Enter password: ")
				createUser((usern,passw))
			elif ch==2: 
				usern = input("Enter username: ")
				updateUser(usern)
			elif ch==3: 
				usern = input("Enter username: ")
				deleteUser(usern)
			elif ch==4: readAllUser()
			elif ch==5: weatherInfo()

	else: print("Wrong Username or Password !")

def updateUser(username):
	data = json.load(open('data.json'))
	ch = 5
	choiceScreen= """
		Choose Options
		1. Change Username
		2. Change Password
		3. Exit
		Choice: """
	while ch!=3:
		ch = int(input(choiceScreen))
		if ch==1: 
			new_username = input("Enter new username: ")
			data[new_username] = data[username]
			del data[username]
			print("Username changed successfully !")
		elif ch==2:
			new_password =''
			pass2 = 'password'
			while new_password!=pass2:
				new_password = input("Enter new password: ")
				pass2 = input("Confirm your password: ")
				if new_password!=pass2:print("Password not match !")
			data[username] = new_password
			print("Password changed successfully !")
		json.dump(data,open('data.json','w'))

def deleteUser(username):
	data = json.load(open('data.json'))
	del data[username]
	json.dump(data,open('data.json','w'))

def readAllUser():
	data = json.load(open('data.json'))
	print("\n\t\t\tUSERS")
	print("\t\t\t------")
	for username in data:
		print('\t\t\t',username)

def weatherInfo():
	choiceScreen ="""
		Choose Options
		1. Humidity
		2. Pressure
		3. Average temperature
		4. Wind Speed
		5. Wind degree
		6. UV Index
		7. Another City Weather
		8. Exit
		Choice: """
	city  = str(input('\n\t\tEnter your location:    '))
	api_key = '53735fde8bca0a7d86d184790bb52530'
		
	url =  f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}"
	data = requests.get(url).json()
	lat = data['coord']['lat']
	lon = data['coord']['lon']
	dt = data['dt']
	
	url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&appid={api_key}"
	data = requests.get(url).json()['current']
	
	while True:
		ch = int(input(choiceScreen))
		if ch==8: break
		print('\t\t\t',end='')
		if ch==1: print('Humidity:',data['humidity'],'%')
		elif ch==2: print('Pressure:',data['pressure'],'hPa')
		elif ch==3:print('Average Temperature:',data['temp'],'Kelvin') 
		elif ch==4:print('Wind Speed:',data['wind_speed'],'meter/sec')
		elif ch==5:print('Wind Degree:',data['wind_deg'])
		elif ch==6:print('UV Index',data['uvi'])
		elif ch==7:
			city  = str(input('\n\t\tEnter new location:    '))
			url =  f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}"
			data = requests.get(url).json()
			lat = data['coord']['lat']
			lon = data['coord']['lon']
			dt = data['dt']
			url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&appid={api_key}"
			data = requests.get(url).json()['current']
			

if __name__ =='__main__':
	parser = argparse.ArgumentParser()
	loginHelp = """
		Utility for Login User.
		E.g Input : --login harsh mypassword123
	"""
	parser.add_argument('--login', nargs=2, metavar=('username','password'),type=str, default=1.0,help=loginHelp)
	createUserHelp = """
		Utility for Create User.
		E.g Input : --create-user harsh mypassword123
	"""
	parser.add_argument('--create-user', nargs=2, metavar=('username','password'),type=str, default=1.0,help=createUserHelp)
	try:
			args = parser.parse_args()
			if type(args.create_user)==list:
				print(1,args)
				createUser(args.create_user)
			elif type(args.login)==list:loginUser(args.login)
	except:pass
	
	
		