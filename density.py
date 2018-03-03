#Sectional distribution
def innertube(sections):
	"""Takes the lampstrj file produced by the CHILL Algorithm and calculates the percent of each type of
		water, printing these to files for each type of water for plotting"""

	file_name = ""	
	tube_radius = 6.29
	tube_length = 80
	atoms = False
	frame_counter = 0
	water_counter = [0 for i in range(sections)] 
	total_counter = 0
	total_atoms = 0
	total_waters = 0

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
	with open(file_name, 'r') as infile:

		print(infile, "is being read")

		out_name1 = file_name + ".density"
		out1 = open(out_name1, 'w')
		out1.write("#Radius, Percent of Waters\n")

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
				if int(split[1]) < 6 and z > 0 and z < tube_length:
					water_counter[get_section(r,sections,tube_radius)] += 1

			if total_counter == int(total_atoms):
				total_counter = 0
				atoms = False

	infile.close()

	for i in range(len(water_counter)):
		total_waters += float(water_counter[i])
	for i in range(len(water_counter)):
		out1.writelines(str(i)+" "+str(water_counter[i]/total_waters)+"\n")

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

innertube(10)
