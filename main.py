# Function which returns subset or r length from n
from itertools import combinations_with_replacement
from itertools import permutations

import sys
import time
import multiprocessing
import threading

import config

import pikepdf

def comb(arr, r):
	return list(combinations_with_replacement(arr, r))

def perm(arr,r):
    return list(permutations(arr,r))

def checker(ret,filename,i,name,queue):
	for j in range(len(ret)):
		if not queue.empty():
			break
		perm_set = set(perm(ret[j],i))
		#print(perm_set)
		perm_arr = [a for a in perm_set]
		for k in range(len(perm_arr)):
			if not queue.empty():
				break
			text = "".join(perm_arr[k])
			#print(text)
			password = text
			#print(name,queue.qsize(),password)
			sys.stdout.write(password)
			sys.stdout.write("\r")
			try:
				with pikepdf.open(filename, password=password) as pdf:
					sys.stdout.write("\r")
					print("Password found - ",password)
					queue.put(password)
					break
			except Exception as e:
				if "invalid password" not in str(e):
					print(e)
		if not queue.empty():
			break

def main(filename):
    #filename = input("Enter filename > ")
    #filename = "D:\Projects\Bruteforcer\exec 2\dist\pan2.pdf"
    s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*"
    arr = [i for i in s]
    i = 1
    checks = 0
    q = multiprocessing.Queue()
    while True:
        start = time.time()
        r = i
        ret = comb(arr, r)
        print(i,len(ret))
        #print(ret)
        #print()
        perm_arr = []
        part = len(ret)//4
        print(part-1,part*2-1,part*3-1,len(ret[:part]),len(ret[part-1:part*2-1]),len(ret[part*2-1:part*3-1]),len(ret[part*3-1:]))
        process1 = multiprocessing.Process(target = checker,args=(ret[:part],filename,i,"1",q))
        process2 = multiprocessing.Process(target = checker,args=(ret[part-1:part*2-1],filename,i,"2",q))
        process3 = multiprocessing.Process(target = checker,args=(ret[part*2-1:part*3-1],filename,i,"3",q))
        process4 = multiprocessing.Process(target = checker,args=(ret[part*3-1:],filename,i,"4",q))
        process1.start()
        process2.start()
        process3.start()
        process4.start()
        config.processes.extend([process1,process2,process3,process4])
        process1.join()
        process2.join()
        process3.join()
        process4.join()
        end = time.time()
        print(f"Time Taken in the block - {end - start}")
        if not q.empty():
        	break
        ret = []
        i+= 1

# Driver Function
if __name__ == "__main__":
	multiprocessing.freeze_support()
	if len(sys.argv) == 1:
		filename = input("Enter filename > ")
		start = time.time()
		main(filename)
		end = time.time()
		print(f"Time taken to find the password - {end - start}")
	else:
		start = time.time()
		main(sys.argv[1])
		end = time.time()
		print(f"Time taken to find the password - {end - start}")
	x = input("Press any key to exit...")
