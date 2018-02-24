#Sectional distribution
def innertube(z_sections):
	"""Takes the lampstrj file produced by the CHILL Algorithm and calculates the percent of each type of
		water, printing these to files for each type of water for plotting"""

#	filename = raw_input("Enter the file to be read: ")
	filename = "vmd.lammpstrj"
	infile = open(filename, 'r')
	print(infile, "is being read")

	outname1 = filename + ".hex.perc"
	outname2 = filename + ".cub.perc"
	outname3 = filename + ".ifcl.perc"
	outname4 = filename + ".ldl.perc"
	outname5 = filename + ".hdl.perc" 

	out1 = open(outname1, 'w')
	out2 = open(outname2, 'w')
	out3 = open(outname3, 'w')
	out4 = open(outname4, 'w')
	out5 = open(outname5, 'w')

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
	totalAtoms = 0 

	for line in infile:
		if line == "ITEM: TIMESTEP\n":
			line = skip(line, infile, 2)
			split = infile.next().split()
			totalAtoms = split[0]
			split = infile.next().split()
			xlo = split[0] 
			xhi = split[1]
			split = infile.next().split()
			ylo = split[0]
			yhi = split[1]
			split = infile.next().split()
			zlo = split[0]
			zhi = split[1]
			line = skip(line, infile, 3)
			frame_counter += 1
			atoms = True
			
		if atoms:
			total_counter += 1
			split = line.split()
			if int(split[1]) < 6:
				types[int(split[1])-1] += 1
				atom_counter += 1
		if total_counter == int(totalAtoms):
			print types, frame_counter, atom_counter, total_counter
			atom_counter = 0
			total_counter = 0
			types = [0 for i in range(5)]
			atoms = False

def skip(line, infile, nLines):
	"""Skips nLines in the file infile"""
	for i in range(nLines):
		line = infile.next()
	return line

innertube(5)

