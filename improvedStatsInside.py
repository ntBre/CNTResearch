#Sectional distribution
def innertube(z_sections):
	"""Takes the lampstrj file produced by the CHILL Algorithm and calculates the percent of each type of
		water, printing these to files for each type of water for plotting"""

#	file_name = raw_input("Enter the file to be read: ")
	file_name = "vmd.lammpstrj"
	infile = open(file_name, 'r')
	print(infile, "is being read")

	out_name1 = file_name + ".hex.perc"
	out_name2 = file_name + ".cub.perc"
	out_name3 = file_name + ".ifcl.perc"
	out_name4 = file_name + ".ldl.perc"
	out_name5 = file_name + ".hdl.perc" 

	out1 = open(out_name1, 'w')
	out2 = open(out_name2, 'w')
	out3 = open(out_name3, 'w')
	out4 = open(out_name4, 'w')
	out5 = open(out_name5, 'w')

	out1.write("#Frame Proportion Hexagonal Ice \n")
	out2.write("#Frame Cubic Ice\n")
	out3.write("#Frame Interfacial\n")
	out4.write("#Frame LDL\n")
	out5.write("#Frame HDL\n")
	
	types = [0 for i in range(5)]
	atoms = False
	frame_counter = 0
	atom_counter = 0
	total_counter = 0
	total_atoms = 0

	x_low = 0
	x_high = 0
	y_low = 0
	y_high = 0
	z_low = 0
	z_high = 0

	for line in infile:
		if line == "ITEM: TIMESTEP\n":
			line = skip(line, infile, 3)
			split = line.split()
			total_atoms = split[0]
			line = skip(line, infile, 2)
			split = line.split()
			x_low = split[0]
			x_high = split[1]
			line = skip(line, infile, 1)
			split = line.split()
			y_low = split[0]
			y_high = split[1]
			line = skip(line, infile, 1)
			split = line.split()
			z_low = split[0]
			z_high = split[1]
			line = skip(line, infile, 2)
			frame_counter += 1
			atoms = True
			
		if atoms:
			total_counter += 1
			split = line.split()
			z = to_normal_coord(z_low, z_high, split[4])
			if int(split[1]) < 6 and z > 0 and z < 80:
				types[int(split[1])-1] += 1
				atom_counter += 1

		if total_counter == int(total_atoms):
			for i in range(len(types)):
				types[i] = float(types[i])/float(atom_counter)
			print types
			atom_counter = 0
			total_counter = 0
			types = [0 for i in range(5)]
			atoms = False

def skip(iterator, file, num):
	"""Skips nLines in the file infile"""

	for i in range(num):
		iterator = file.next()
	return iterator

def to_normal_coord(low, high, relative_coord):
	"""Converts the default lammpstrj coordinates to normal coordinates"""

	low = float(low)
	high = float(high)
	relative_coord = float(relative_coord)
	converted_coord = (high - low)*relative_coord + low
	return converted_coord

innertube(5)

