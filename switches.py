# define and manage interruptors
import dio433

switches = [
    # name, sender, interruptor
    ( 'rasp3b', 7128122, 0 ),
    ( 'sovol', 29014766, 0 ),
#    ( 'unused', 7128122, 5 ),  # sound like a duplicate of the first one
]

state = [False] * len(switches)

def switch(newstate, intno):
    global state

    interruptor = switches[intno]
    dio433.dio433(onoff=newstate, pinno=None, sender=interruptor[1], interruptor=interruptor[2])
    state[intno] = newstate

def nswitches():
    return len(switches)

if __name__ == "__main__":
    for i in switches:
        print(f"Interruptor: {i[0]}, Sender: {i[1]}, Interruptor ID: {i[2]}")
