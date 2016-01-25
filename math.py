from plne.exact import Exact
import sys


algo = Exact()
k = None
b = None
s = None
plot = False

try:
    if len(sys.argv) < 2:
        raise ValueError('Error: too few arguments')

    args = [sys.argv[x] for x in range(1, len(sys.argv) - 1)] 
    args = iter(args)
    for arg in args:
        if arg == '-k':
            if s != None:
                raise ValueError('Error: can not define two partitions constraints')
            try:
                k = int(args.next())
            except ValueError:
                raise ValueError('Error: argument k should be an integer')
	elif arg == '-b':
	    if k == None:
	    	raise ValueError('Error: argument k should be defined before -b')
            try:
                b = float(args.next())
            except ValueError:
                raise ValueError('Error: argument r should be a float')
        elif arg == '-s':
            if k != None:
                raise ValueError('Error: can not define two partitions constraints')
            try:
                s = int(args.next())
            except ValueError:
                raise ValueError('Error: argument s should be an integer')
        elif arg == '--plot':
            plot = True
        else:
            raise ValueError('Error: argument ' + str(arg) + ' is unknown')

    if k == None and s == None:
        k = 2

except ValueError as error:
    print(error)
    print('Usage: math.py [-k num [-b num]]|[-s num] [--plot] path')
    exit(0)
path = sys.argv[-1]

algo.load(path).partition(k=k, balance=b, size=s)

print('')
print('Best solution:')
print(algo)
print('')

if plot:
    if algo.number_of_nodes() < 50:
    	algo.draw(label=True)
    else:
        print('Warning: Ignore --plot (graph is too large)')

