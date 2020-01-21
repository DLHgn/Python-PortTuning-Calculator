import gui_setup

#setup main window
mainWindow = gui_setup.window_setup.Window(700, 200)
mainWindow.window_setup("Port Tuning Calculator")

#setup port area text/textfield/button
portArea = gui_setup.gui_items.Row("Port Cross Sectional Area", 0, 0)
portArea.row_setup(mainWindow.window, 5, 8, "in^2", "cm^2", "ft^2", "mm^2")
gui_setup.computations.set_port_area(portArea)

#setup Net Volume (Box)
netVolume = gui_setup.gui_items.Row("Net Volume (Box)", 3, 0)
netVolume.row_setup(mainWindow.window, 5, 8, "in^3", "L", "cm^3", "ft^3", "mm^3")
gui_setup.computations.set_net_volume(netVolume)


#setup Length of Port
portLength = gui_setup.gui_items.Row("Length of Port", 0, 1)
portLength.row_setup(mainWindow.window, 5, 8, "in", "cm", "ft", "m", "mm")
gui_setup.computations.set_port_length(portLength)


#setup the end correction
endCorrection = gui_setup.gui_items.Row("End Correction", 3, 1)
endCorrection.row_setup(mainWindow.window, 5, 8, "3 Common Walls", "1 Common Wall", "2 Common Walls",
                        "One Flanged End", "Both Flanged Ends", "Both Free Ends", use_btn=False, use_cmb=True)
gui_setup.computations.set_end_correction(endCorrection)


#setup port tuning
portTuning = gui_setup.gui_items.Row("Port Tuning (Hz)", 0, 2)
portTuning.output(mainWindow.window, 5, 8)
gui_setup.computations.set_port_tuning(portTuning)


#setup number of ports
numberOfPorts = gui_setup.gui_items.Row("Number of Ports", 3, 2)
numberOfPorts.row_setup(mainWindow.window, 5, 8, 'no name', use_btn=False)
numberOfPorts.insert_default_txtfield('1')
gui_setup.computations.set_number_of_ports(numberOfPorts)


#setup submit button
submitBtn = gui_setup.gui_items.Row("Submit", 1, 3)
submitBtn.btn_setup(mainWindow.window, 5)

mainWindow.window.mainloop()
