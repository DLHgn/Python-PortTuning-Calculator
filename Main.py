import gui_setup

pad = 5
txtfield_size = 8

#setup main window
mainWindow = gui_setup.window_setup.Window(700, 200)
mainWindow.window_setup("Port Tuning Calculator")

#setup port area text/textfield/button
portArea = gui_setup.gui_items.Item("Port Cross Sectional Area", 0, 0)
portArea.item_setup(mainWindow.window, pad, txtfield_size, "in^2", "cm^2", "ft^2", "mm^2")
gui_setup.computations.set_port_area(portArea)

#setup Net Volume (Box)
netVolume = gui_setup.gui_items.Item("Net Volume (Box)", 3, 0)
netVolume.item_setup(mainWindow.window, pad, txtfield_size, "in^3", "L", "cm^3", "ft^3", "mm^3")
gui_setup.computations.set_net_volume(netVolume)


#setup Length of Port
portLength = gui_setup.gui_items.Item("Length of Port", 0, 1)
portLength.item_setup(mainWindow.window, pad, txtfield_size, "in", "cm", "ft", "m", "mm")
gui_setup.computations.set_port_length(portLength)


#setup the end correction
endCorrection = gui_setup.gui_items.Item("End Correction", 3, 1)
endCorrection.item_setup(mainWindow.window, pad, txtfield_size, "3 Common Walls", "1 Common Wall", "2 Common Walls",
                         "One Flanged End", "Both Flanged Ends", "Both Free Ends", use_btn=False, use_cmb=True)
gui_setup.computations.set_end_correction(endCorrection)


#setup port tuning
portTuning = gui_setup.gui_items.Item("Port Tuning (Hz)", 0, 2)
portTuning.output(mainWindow.window, pad, txtfield_size)
gui_setup.computations.set_port_tuning(portTuning)


#setup number of ports
numberOfPorts = gui_setup.gui_items.Item("Number of Ports", 3, 2)
numberOfPorts.item_setup(mainWindow.window, pad, txtfield_size, 'no name', use_btn=False)
numberOfPorts.insert_default_txtfield('1')
gui_setup.computations.set_number_of_ports(numberOfPorts)


#setup submit button
submitBtn = gui_setup.gui_items.Item("Submit", 1, 3)
submitBtn.btn_setup(mainWindow.window, pad)

mainWindow.window.mainloop()
