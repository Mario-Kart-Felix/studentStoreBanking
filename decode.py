import subprocess
var = subprocess.check_output('./quick_start_example1').decode('utf-8').strip();
output = open('output', 'w+');
output.write(var);

