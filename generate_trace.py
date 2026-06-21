import random

def generate_trace(filename, num_accesses=1000):
    trace = []
    
    # Hot addresses — accessed frequently (frequency skew)
    hot = [1, 2, 3, 4, 5]
    
    # Warm addresses — accessed occasionally (temporal locality)
    warm = list(range(6, 20))
    
    # Cold addresses — sequential scan (new addresses)
    cold_start = 20
    cold_counter = [cold_start]

    for i in range(num_accesses):
        r = random.random()
        
        if r < 0.4:
            # 40% chance — access a hot address (frequency skew)
            trace.append(random.choice(hot))
        
        elif r < 0.7:
            # 30% chance — access a warm address (temporal locality)
            trace.append(random.choice(warm))
        
        else:
            # 30% chance — sequential scan (new address)
            trace.append(cold_counter[0])
            cold_counter[0] += 1

    with open(filename, 'w') as f:
        for addr in trace:
            f.write(str(addr) + '\n')

    print(f"Generated {len(trace)} accesses -> {filename}")

generate_trace("traces/realistic.trace")
generate_trace("traces/frequency_heavy.trace", 1000)