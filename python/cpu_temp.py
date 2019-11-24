cpu_file = open('/sys/class/thermal/thermal_zone0/temp')
cpu_temp = float(cpu_file.read())/1000
print cpu_temp
cpu_file.close()
