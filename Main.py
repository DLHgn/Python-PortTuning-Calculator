import gui_setup
import gui_setup.gui_data_manager as data_manager

pad = 5
txtfield_size = 8

# setup main window
mainWindow = gui_setup.window_setup.Window(700, 300)
mainWindow.window_setup("Port Tuning Calculator")

# setup port area text/textfield/button
portArea = gui_setup.gui_items.Item("Port Cross Sectional Area", 0, 0)
portArea.item_setup(mainWindow.window, pad, txtfield_size, "in^2", "cm^2", "ft^2", "mm^2", 'm^2')
data_manager.set_port_area(portArea)

# setup Net Volume (Box)
netVolume = gui_setup.gui_items.Item("Net Volume (Box)", 3, 0)
netVolume.item_setup(mainWindow.window, pad, txtfield_size, "in^3", "L", "cm^3", "ft^3", "mm^3", "m^3")
data_manager.set_net_volume(netVolume)


# setup Length of Port
portLength = gui_setup.gui_items.Item("Length of Port", 0, 1)
portLength.item_setup(mainWindow.window, pad, txtfield_size, "in", "cm", "ft", "m", "mm")
data_manager.set_port_length(portLength)


# setup the end correction
endCorrection = gui_setup.gui_items.Item("End Correction", 3, 1)
endCorrection.item_setup(mainWindow.window, pad, txtfield_size, "3 Common Walls", "1 Common Wall", "2 Common Walls",
                         "One Flanged End", "Both Flanged Ends", "Both Free Ends", use_btn=False, use_cmb=True)
data_manager.set_end_correction(endCorrection)


# setup port tuning
portTuning = gui_setup.gui_items.Item("Port Tuning (Hz)", 0, 2)
portTuning.output(mainWindow.window, pad, txtfield_size)
data_manager.set_port_tuning(portTuning)


# setup number of ports
numberOfPorts = gui_setup.gui_items.Item("Number of Ports", 3, 2)
numberOfPorts.item_setup(mainWindow.window, pad, txtfield_size, 'no name', use_btn=False)
numberOfPorts.insert_default_txtfield('1')
data_manager.set_number_of_ports(numberOfPorts)

# setup Cms
cms = gui_setup.gui_items.Item("Cms", 0, 5)
cms.item_setup(mainWindow.window, pad, txtfield_size, "m/N", "mm/N", "um/N")
data_manager.set_cms(cms)

# setup Mms
mms = gui_setup.gui_items.Item("Mms", 3, 5)
mms.item_setup(mainWindow.window, pad, txtfield_size, "Kg", "g")
data_manager.set_mms(mms)

# setup Le
le = gui_setup.gui_items.Item("Le", 0, 6)
le.item_setup(mainWindow.window, pad, txtfield_size, "H", "mH")
data_manager.set_le(le)

# setup Re
re = gui_setup.gui_items.Item("Re", 3, 6)
re.item_setup(mainWindow.window, pad, txtfield_size, "ohm")
data_manager.set_re(re)

# setup Rms
rms = gui_setup.gui_items.Item("Rms", 0, 7)
rms.item_setup(mainWindow.window, pad, txtfield_size, "Kg/s", "Ns/s")
data_manager.set_rms(rms)

# setup Bl
bl = gui_setup.gui_items.Item("Bl", 3, 7)
bl.item_setup(mainWindow.window, pad, txtfield_size, "Tm", "Na")
data_manager.set_bl(bl)

# setup Sd
sd = gui_setup.gui_items.Item("Sd", 0, 8)
sd.item_setup(mainWindow.window, pad, txtfield_size, "m^2", "cm^2", "mm^2", "in^2", "ft^2")
data_manager.set_sd(sd)

# setup Vg
vg = gui_setup.gui_items.Item("Vg", 3, 8)
vg.item_setup(mainWindow.window, pad, txtfield_size, "w")
data_manager.set_vg(vg)

# setup submit button
submitBtn = gui_setup.gui_items.Item("Submit", 1, 9)
submitBtn.btn_setup(mainWindow.window, pad)

# This is for setting test data
# setup load test button
loadTest = gui_setup.buttons.Btn(3, 10, "Load Test")
loadTest.btn_setup(mainWindow.window, pad)

# The below fields are strictly for testing purposes and should be deleted once equations are tested

# setup test frequency
frequency = gui_setup.gui_items.Item("test frequency", 0, 10)
frequency.item_setup(mainWindow.window, pad, txtfield_size, "Hz")
data_manager.set_frequency(frequency)

mainWindow.window.mainloop()
