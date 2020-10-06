import interfaces.grovepiinterface
  
grove = GrovePiInterface(timelimit=20)
colour = (0,128,64)
message = "this is working"
grove.output_RGB(colour,message)
print(grove.read_light_sensor_analogueport(2))