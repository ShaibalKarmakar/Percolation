import pickle
import os
import matplotlib.pyplot as plt
 
path = os.path.join(os.getcwd(), "fine_long_mesh")
# path = os.path.join(os.getcwd(), "fine_mesh")
def print_seperate(): 
	global path
	files=os.listdir(path)
	for filename in files:
		if filename[-4:]!=".pkl": continue
		filepath=os.path.join(path,filename)
		with open(filepath,"rb") as fp:
			rec=dict(pickle.load(fp))
			# print(rec)
			nrange=[]
			density=[]
			i=1
			while(i in rec.keys()):
				nrange.append(i)
				density.append(rec[i]/rec["trials_done"])
				i+=1
			# print(f"p={rec['p']}")
			# print(density)
			plt.plot(nrange,density)
			plt.savefig(os.path.join(path,f"p={rec['p']}.png"))
			plt.close()

def print_together():
	global path
	files=os.listdir(path)
	plt.figure(figsize = (10,6))
	for filename in files:
		if filename[-4:]!=".pkl": continue
		filepath=os.path.join(path,filename)
		with open(filepath,"rb") as fp:
			rec=dict(pickle.load(fp))
			print(rec)
			nrange=[]
			density=[]
			i=1
			while(i in rec.keys()):
				nrange.append(i)
				density.append(rec[i]/rec["trials_done"])
				i+=1
			# print(f"p={rec['p']}")
			# print(density)
			plt.plot(nrange,density, label = f"p={rec['p']}")
			# plt.savefig(os.path.join(path,f"p={rec['p']}.png"))
	plt.legend(loc = 'best')
	plt.savefig(os.path.join(path, f"all.png"))

if __name__ == "__main__":
	print_seperate()
	print_together()