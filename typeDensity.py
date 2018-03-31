#Sectional distribution
def innertube(sections):
	"""Takes the lampstrj file produced by the CHILL Algorithm and calculates the percent of each type of
		water, printing these to files for each type of water for plotting"""

	file_name = ""	
	tube_radius = 0 
	tube_length = 80
	types = [[0] * sections for i in range(5)]
	average_types = [[0] * sections for i in range(5)]
	total_water = [0 for i in range(sections)]
	atoms = False
	frame_counter = 0
	water_counter = 0 
	total_counter = 0
	total_atoms = 0
	section = 0

	x_low = 0
	x_high = 0
	y_low = 0
	y_high = 0
	z_low = 0
	z_high = 0
	x = 0
	y = 0
	z = 0
	r = 0

	while file_name == "":
		file_name = raw_input("Enter the file to be read: ")
	tube_radius = float(raw_input("Enter the expected tube radius: "))
	with open(file_name, 'r') as infile:
		print(infile, "is being read")

		out_name1 = file_name + ".hex.dens"
		out_name2 = file_name + ".cub.dens"
		out_name3 = file_name + ".ifcl.dens"
		out_name4 = file_name + ".ldl.dens"
		out_name5 = file_name + ".hdl.dens" 
		out_name6 = file_name + ".tot.dens"

		out1 = open(out_name1, 'w')
		out2 = open(out_name2, 'w')
		out3 = open(out_name3, 'w')
		out4 = open(out_name4, 'w')
		out5 = open(out_name5, 'w')
		out6 = open(out_name6, 'w')

		out_list = [out1, out2, out3, out4, out5, out6]

		out1.write("#Section Proportion Hexagonal Ice \n")
		out2.write("#Section Cubic Ice\n")
		out3.write("#Section Interfacial\n")
		out4.write("#Section LDL\n")
		out5.write("#Section HDL\n")
		out6.write("#Radius Waters\n")

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
				x = to_normal_coord(x_low, x_high, split[2])
				y = to_normal_coord(y_low, y_high, split[3])
				z = to_normal_coord(z_low, z_high, split[4])
				r = (x**2+y**2)**.5
				if int(split[1]) < 6 and z > 0 and z < tube_length and r < tube_radius:
					types[int(split[1])-1][get_section(r,sections,tube_radius)] += 1
					water_counter += 1

			if total_counter == int(total_atoms):
				for i in range(len(types)):
					for j in range(len(types[i])):
						if water_counter > 0:
							average_types[i][j] += (float(types[i][j])/float(water_counter))
						else:
							average_types[i][j] += (float(types[i][j]))
				water_counter = 0 
				total_counter = 0
				types = [[0] * sections for i in range(5)]
				atoms = False
	infile.close()

	for i in range(len(average_types)):
		for j in range(len(average_types[i])):
			total_water[j] += average_types[i][j]
			out_list[i].writelines(str(j*(tube_radius/sections))+" "+str(average_types[i][j]/frame_counter)+"\n")

	for i in range(len(total_water)):
		out6.writelines(str(i*tube_radius/sections)+" "+str(total_water[i]/frame_counter)+"\n")

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

def get_section(r, num_sections, tube_radius):
	"""Takes an r value, the number of sections, and the radius of the tube and returns the corresponding section"""

	section = int(r / (tube_radius / num_sections))
	return section

innertube(100)
