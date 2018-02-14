import sublime, sublime_plugin, os, stat

class BuildWithBluespecCommand(sublime_plugin.TextCommand): 
   def run(self, edit):
      absolute_file_path = self.view.window().active_view().file_name()
      file_name = os.path.basename(absolute_file_path)
      file_path = absolute_file_path [:-len(file_name)]
      tu_id_file = open('/tmp/sublime_tu_id.txt', 'r')
      tu_id = tu_id_file.readline()
      tu_id_file.close()
      tmp_file = open(file_path+'tmp', 'w+')
      tmp_file.write('#!/bin/bash\nBSV_FILE_PATH=$1\nBSV_FILE_NAME=$2\nBSV_MODULE=$3\nrsync $BSV_FILE_PATH '+tu_id+'@clientssh2.rbg.informatik.tu-darmstadt.de:~/AER/tmp/ > /dev/null 2>&1 && ssh -t '+tu_id+'@clientssh2.rbg.informatik.tu-darmstadt.de "export BLUESPECDIR=/opt/bluespec/lib ; export LM_LICENSE_FILE=27002@licence.rbg.informatik.tu-darmstadt.de ; cd ~/AER/tmp/ ; cp ~/AER/BlueCheck.bsv BlueCheck.bsv ; cp ~/AER/BlueCheck.bo BlueCheck.bo ; /opt/bluespec/bin/bsc -u -sim -g $BSV_MODULE $BSV_FILE_NAME ; /opt/bluespec/bin/bsc -sim -o out -e $BSV_MODULE ; echo "----------Start Simulation----------" ; ./out ; echo "-----------End Simulation-----------" ; rm out"')     
      tmp_file.close()
      st = os.stat(file_path+'tmp')
      os.chmod(file_path+'tmp', st.st_mode | stat.S_IEXEC)
      file = open(absolute_file_path, 'r')
      first_line = file.readline()  
      first_line = first_line [2:-1]
      file.close() 	
      module_string =  str(first_line)       
      self.view.window().run_command('exec', {'cmd': [file_path+'tmp', absolute_file_path, file_name, module_string]})
      os.remove(file_path+'tmp')
