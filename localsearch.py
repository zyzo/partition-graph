import sys
from datetime import datetime
from heuristic.local import Local, Stub

k = 2
algo = Local()
depth = None
theta = None
replays = 0
preemption = []
rand = False
log = Stub()  
stat = False
plot = False

try:
    if len(sys.argv) < 3:
        raise ValueError('Error: too few arguments')

    args = [sys.argv[x] for x in range(1, len(sys.argv) - 1)] 
    args = iter(args)
    for arg in args:
        if arg == '-k':
            try:
                k = int(args.next())
            except ValueError:
                raise ValueError('Error: argument k should be an integer')
        elif arg == '-d':
            if theta == None and depth == None:
                try:
                    depth = int(args.next())
                except ValueError:
                    raise ValueError('Error: argument d should be an integer')
            else:
                raise ValueError('Error: can not define multiples stop conditions') 
        elif arg == '-t':
            if theta == None and depth == None:
                try:
                    theta = float(args.next())
                except ValueError:
                    raise ValueError('Error: argument t should be a numeral')
            else:
                raise ValueError('Error: can not define multiples stop conditions')
        elif arg == '-i':
            try:
                replays = int(args.next())
            except ValueError:
                raise ValueError('Error: argument i should be an integer')
        elif arg == '--random':
            rand = True
        elif arg == '--stat':
            stat = True
            log = sys.stdout
        elif arg == '--plot':
            plot = True
        elif arg == '--cut':
            preemption.append('cut')
        elif arg == '--balance':
            preemption.append('balance')
        elif arg == '--ratio':
            preemption.append('ratio')
        else:
            raise ValueError('Error: argument ' + str(arg) + ' is unknown')
except ValueError as error:
    print(error)
    print('Usage: localsearch.py [-k num] [-d|-t num] [-i num] [--random] [--stat] [--plot] --cut|balance|ratio path')
    exit(0)
if len(preemption) == 0:
    preemption.append('ratio')
path = sys.argv[-1]
     
if stat:
    print(datetime.now().time())
print('')

try:
    algo.load(path).partition(k=k, depth=depth, theta=theta, replays=replays, preemption=preemption, rand=rand, log=log)

    print('')
    print('Best solution:')
    print(algo)
    print('')

    if plot:
        if algo.number_of_nodes() < 50:
            algo.draw(label=True)
        else:
            print('Warning: Ignore --plot (graph is too large)')

except KeyboardInterrupt as ki:
    print(ki)

if stat:
    print(datetime.now().time())


