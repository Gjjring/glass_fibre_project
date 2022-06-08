wvl = 1500e-6
freq = constants.c*2*np.pi/(wvl)
print("{:.3f} GHz".format(freq/(2*np.pi*1e9)))
fig, [ax0, ax1, ax2] = plt.subplots(3,1, figsize=(16,12))


def carrier_signal(frequency, time):
    return np.sin(2*np.pi*freq*time)

def modulation_signal(frequency, time, modulation):
    phase = np.pi/4.
    modulation = modulation*np.concatenate([np.linspace(0., 1., int((time.size)/2)),
                                            np.linspace(1., 0., int((time.size)/2))])
    signal = modulation*np.sin(2*np.pi*(freq/5)*time+phase)
    return signal

def combine_signals(signal1, signal2):
    combined_signal = (1+signal2)*signal1
    return combined_signal



ang_freq = 1.
t_step = 10/freq
word = "1001"
for iletter, letter in enumerate(word):
    t = np.linspace(t_step*iletter, t_step*(1+iletter), 1000)

    carrier = carrier_signal(ang_freq, t)
    plt.sca(ax0)
    plt.plot(t, carrier)
    if letter == "0":
        modulation = 0.
    if letter == "1":
        modulation = 1.0

    signal = modulation_signal(ang_freq, t, modulation)
    plt.sca(ax1)
    plt.plot(t, signal)

    combined_signal = combine_signals(carrier, signal)
    plt.sca(ax2)
    plt.plot(t, combined_signal)
    plt.plot(t, 1+signal, ls='--')
    plt.plot(t, -(1+signal), ls='--')
