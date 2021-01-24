import pickle

class TaskClass:
	def __init__(self, activity):
		self.activity = activity
		self.link = "(link)"
		self.done = False

	def mark_done(self):
		if self.done == False:
			self.done = True
		else:
			self.done = False

class SubjectClass:
	def __init__(self, name):
		self.name = name
		self.task_list = []

	def add_task(self, activity):
		self.task_list.append(TaskClass(activity))
		print("Task added to " + self.name + ".")

	def print_tasklist(self):
		print(self.name + ":")
		for i in range(len(self.task_list)):
			print(str(i) + ". ", end="")
			if self.task_list[i].done == False:
				print("[ ]", end=" ")
			else:
				print("[x]", end=" ")
			print(self.task_list[i].activity)
			i += 1

	def done(self, index, num="one"):
		if num == 'all':
			for i in range(0, len(self.task_list)):
				self.task_list[i].done = True
		else:
			if index >= 0 and index < len(self.task_list):
				if self.task_list[index].done == False:
					self.task_list[index].done = True
				else:
					self.task_list[index].done = False

	def delete_task(self, index):
		if index >= 0 and index < len(self.task_list):
			del self.task_list[index]

class UserClass:
	def __init__(self):
		self.username = "(name)"
		self.password = "(pass)"
		self.subject_list	= []
		self.today_tasks 	= SubjectClass('Today')

	def add_subject(self, subject_name):
		self.subject_list.append(SubjectClass(subject_name))
		print("Subject added.")

	def print_subjects(self):
		for i in range(len(self.subject_list)):
			print("[" + str(i) + "] " + self.subject_list[i].name)

class UserList:
	def __init__(self):
		self.user_list = []
		self.current_user = None

	def add_user(self):
		new_user = UserClass()
		username = input("Enter username: ")
		if username == "":
			print("Username cannot be empty.")
			return False
		else:
			for x in self.user_list:
				if x.username == username:
					print("Account with that username already.")
					return False

		password = input("Enter password: ")
		if password == "":
			print("Password cannot be empty.")
			return False
		new_user.username = username
		new_user.password = password

		self.user_list.append(new_user)
		self.current_user = new_user
		print("Created account for " + new_user.username + ".")
		repl.change_prompt(global_userlist.current_user.username)

		return True

	def login(self):
		username = input("Enter username: ")
		if username == "":
			print("Username cannot be empty.")
			return
		for x in self.user_list:
			if x.username == username:
				password = input("Enter password: ")
				if password == "":
					print("Password cannot be empty.")
					return
				if password == x.password:
					self.current_user = x
					print("Logged in successfully.")
					repl.change_prompt(global_userlist.current_user.username)
					return True
		print("Account not found or password incorrect.")
		return False

	def logout(self):
		self.current_user = None
		print("Logged out.")
		repl.change_prompt("")

	def logged_in(self):
		return self.current_user != None

	def print(self):
		print("User List:")
		for i in range(len(self.user_list)):
			print("[" + str(i) + "] " + self.user_list[i].username)


global_userlist = UserList()

class REPLClass:
	def __init__(self):
		print("LazyCodersList v1.0")
		self.prompt_text = "> "
		self.admin_running = True
		self.session_running = False

	def change_prompt(self, text = ""):
		self.prompt_text = text + "> "

	def help(self, func = "all"):
		if func == "all":
			print("Commands: ")
			print("\t1. add 	('+')	- Add user/task to selected subject.")
			print("\t2. del 	('-')	- Delete task from selected subject.")
			print("\t3. done 	('x')	- Mark/Unmark task from selected subject.")
			print("\t4. view 	('v')	- View users/subjects/tasks.")
			print("\t5. login 	('li')	- Login to an account.")
			print("\t6. logout 	('lo')	- Logout of account.")
			print("\t7. select 	('s')	- Select a subject.")
			print("\t8. clear 	('c')	- Clear screen/subject list/task list.")
			print("\t9. help 	('h')	- Print this list.")

	def clear_screen(self):
		print("\n" * 512)

	def prompt(self):
		return input(self.prompt_text)

	def parse(self, args):
		args = args.split()
		if len(args) == 0:
			command = ""
		else:
			command = args[0]
			del args[0]

		if command in ["quit", "exit", "q"]:
			print("Ending session...")
			quit()

		elif command in ["add", "+"]:
			if len(args) > 0:
				if args[0] in ["subject", "sub", "s"]:
					# Add subject
					del args[0]
					subject_name = ' '.join(args)
					if subject_name != "":
						global_userlist.current_user.add_subject(' '.join(args))
				elif args[0].isnumeric():
					# Add subject task
					index = int(args[0])
					del args[0]
					if index in range(len(global_userlist.current_user.subject_list)):
						activity = ' '.join(args)
						if activity != "":
							global_userlist.current_user.subject_list[index].add_task(' '.join(args))
					else:
						print("Invalid subject index.")
				else:
					# Add to Today's tasks
					activity = ' '.join(args)
					if activity != " ":
						global_userlist.current_user.today_tasks.add_task(' '.join(args))

		elif command in ["delete", "del", "-"]:
			if len(args) > 0:
				if args[0] in ["subject", "sub", "s"]:
					# Delete subject -> - sub 0
					if len(args) != 2:
						print("Subject index required.")
						return
					if args[1].isnumeric():
						subject_index = int(args[1])
						if subject_index in range(len(global_userlist.current_user.subject_list)):
							print(global_userlist.current_user.subject_list[subject_index].name + " deleted.")
							del global_userlist.current_user.subject_list[subject_index]

						else:
							print("Invalid subject index.")

				elif args[0].isnumeric():
					# Delete subject task -> - 1 0
					if len(args) == 2:
						subject_index = int(args[0])
						if subject_index in range(len(global_userlist.current_user.subject_list)):
							if args[1].isnumeric():
								task_index = int(args[1])
								if task_index in range(len(global_userlist.current_user.subject_list[subject_index].task_list)):
									del global_userlist.current_user.subject_list[subject_index].task_list[task_index]
								else:
									print("Invalid task index.")
							else:
								print("Task index must be a number.")
						else:
							print("Invalid subject index.")

					# Delete today's tasks -> - 0
					else:
						task_index = int(args[0])
						if task_index in range(len(global_userlist.current_user.today_tasks.task_list)):
							del global_userlist.current_user.today_tasks.task_list[task_index]
						else:
							print("Invalid task index.")

		elif command in ["logout", "lo"]:
			global_userlist.logout()
			self.session_running = False
			return

		elif command in ["view", "v"]:
			if len(args) > 0:
				if args[0] in ["subjects", "sub", "s"]:
					# View subject tasks
					if len(args) == 2:
						if args[1].isnumeric():
							index = int(args[1])
							if index in range(len(global_userlist.current_user.subject_list)):
								global_userlist.current_user.subject_list[index].print_tasklist()
							else:
								print("Invalid index.")
						else:
							print("Index should be a number.")
					else:
						# View today's tasks
						global_userlist.current_user.print_subjects()

				elif args[0] in ["today", "t"]:
					# View today's tasks
					global_userlist.current_user.today_tasks.print_tasklist()
			else:
				# View today's tasks
				global_userlist.current_user.today_tasks.print_tasklist()

		elif command in ["done", "x"]:
			if len(args) == 2:
				# Mark subject tasks
				if args[0].isnumeric():
					subject_index = int(args[0])
					if subject_index in range(len(global_userlist.current_user.subject_list)):
						if args[1].isnumeric():
							task_index = int(args[1])
							if task_index in range(len(global_userlist.current_user.subject_list[subject_index].task_list)):
								global_userlist.current_user.subject_list[subject_index].done(task_index)
					else:
						print("Invalid index.")
				else:
					print("Index should be a number.")

			else:
				if args[0].isnumeric():
					index = int(args[0])
					if index in range(len(global_userlist.current_user.today_tasks.task_list)):
						global_userlist.current_user.today_tasks.done(index)
					else:
						print("Invalid index.")
				else:
					print("Index should be a number.")

		elif command in ["copy", "cp", "."]:
			# copy 0 0
			if len(args) == 2:
				if args[0].isnumeric():
					subject_index = int(args[0])
					if subject_index in range(len(global_userlist.current_user.subject_list)):
						if args[1].isnumeric():
							task_index = int(args[1])
							if task_index in range(len(global_userlist.current_user.subject_list[subject_index].task_list)):
								global_userlist.current_user.today_tasks.add_task(global_userlist.current_user.subject_list[subject_index].task_list[task_index].activity)
							else:
								print("Invalid task index.")

					else:
						print("Invalid subject index.")

			# copy 1 0 2
			elif len(args) == 3:
				if args[0].isnumeric():
					from_index = int(args[0])
					if from_index in range(len(global_userlist.current_user.subject_list)):
						if args[1].isnumeric():
							task_index = int(args[1])
							if task_index in range(len(global_userlist.current_user.subject_list[from_index].task_list)):
								if args[2].isnumeric():
									to_index = int(args[2])
									if to_index in range(len(global_userlist.current_user.subject_list)):
										global_userlist.current_user.subject_list[to_index].add_task(global_userlist.current_user.subject_list[from_index].task_list[task_index].activity)
									else:
										print("Invalid to-list index.")
							else:
								print("Invalid task index.")
					else:
						print("Invalid from-list index.")

		elif command == "#":
			pass

		elif command in ["help", "h"]:
			self.help()

		elif command in ["clear", "c"]:
			if len(args) == 0:
				self.clear_screen()
			else:
				pass

		elif command == "":
			pass

		else:
			print(command + ": not understood.")
repl = REPLClass()

def admin_interface():
	global repl
	print()
	print("1. Add new user.")
	print("2. Delete a user.")
	print("3. Login.")
	print("4. List users.")
	print("5. Clear screen.")
	print("6. Quit session.")
	choice = input("admin> ")
	if choice.isnumeric() == False:
		return
	choice = int(choice)
	if choice == 1:
		if global_userlist.add_user():
			repl.session_running = True

	elif choice == 2:
		if len(global_userlist.user_list) == 0:
			print("No users in list.")
			return
		index = int(input("Enter user-number: "))
		if index in range(len(global_userlist.user_list)):
			del global_userlist.user_list[index]
			print("User deleted.")
		else:
			print("Invalid index.")

		repl.session_running = False
		
	elif choice == 3:
		if global_userlist.login():
			repl.session_running = True

	elif choice == 4:
		global_userlist.print()

	elif choice == 5:
		repl.clear_screen()

	elif choice == 6:
		print("Ending admin...")
		quit()

	else:
		print("Choice invalid.")
		return False

	while repl.session_running:
		repl.parse(repl.prompt())

def main():
	while repl.admin_running:
		admin_interface()

		
main()
