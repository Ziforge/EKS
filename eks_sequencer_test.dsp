declare name "EKS Guitar Sequencer - Progressive Rock Style";
declare author "Julius Smith / Modified";
declare version "1.0";
declare license "STK-4.3";
declare copyright "Julius Smith";
declare reference "http://ccrma.stanford.edu/~jos/pasp/vegf.html";

import("stdfaust.lib");

//==================== SEQUENCER ================

// Run/stop button
run = checkbox("run_sequencer");

seq_tempo = hslider("tempo [unit:BPM]", 138, 60, 200, 1) / 60;

// Step counter (0-15)
step = (ba.beat(seq_tempo) * run) : ba.pulse_countup_loop(15, 1) : int;

// Progressive rock style bass pattern (inspired, not copied)
// Pattern in semitones relative to root (E2 = MIDI 40)
note_at_step(s) =
    (s == 0)  * 0 +   // E
    (s == 1)  * 7 +   // B
    (s == 2)  * 5 +   // A
    (s == 3)  * 3 +   // G
    (s == 4)  * 0 +   // E
    (s == 5)  * 7 +   // B
    (s == 6)  * 5 +   // A
    (s == 7)  * 10 +  // D
    (s == 8)  * 0 +   // E
    (s == 9)  * 7 +   // B
    (s == 10) * 5 +   // A
    (s == 11) * 3 +   // G
    (s == 12) * 5 +   // A
    (s == 13) * 3 +   // G
    (s == 14) * 2 +   // F#
    (s == 15) * 0;    // E

root_note = hslider("root_note [midi:keynum]", 40, 24, 60, 1);
current_note = root_note + note_at_step(step);
freq = ba.midikey2hz(current_note);

// Gate/trigger from sequencer (only when running)
gate = ba.beat(seq_tempo) * run;

//==================== EKS GUITAR SYNTH (FULL ORIGINAL) ================

gain = hslider("gain", 1, 0, 10, 0.01);    // 0 to 1

// Additional parameters (MIDI "controllers"):

// Pick angle in [0,0.9]:
pickangle = 0.9 * hslider("pick_angle",0,0,0.9,0.1);

// Normalized pick-position in [0,0.5]:
beta = hslider("pick_position [midi: ctrl 0x81]", 0.13, 0.02, 0.5, 0.01);
       // MIDI Control 0x81 often "highpass filter frequency"

// String decay time in seconds:
t60 = hslider("decaytime_T60", 4, 0, 10, 0.01);  // -60db decay time (sec)

// Normalized brightness in [0,1]:
B = hslider("brightness [midi:ctrl 0x74]", 0.5, 0, 1, 0.01);// 0-1
    // MIDI Controller 0x74 is often "brightness"
    // (or VCF lowpass cutoff freq)

// Dynamic level specified as dB level desired at Nyquist limit:
L = hslider("dynamic_level", -10, -60, 0, 1) : ba.db2linear;
// Note: A lively clavier is obtained by tying L to gain (MIDI velocity).

// Spatial "width" (not in original EKS, but only costs "one tap"):
W = hslider("center-panned spatial width", 0.5, 0, 1, 0.01);
A = hslider("pan angle", 0.5, 0, 1, 0.01);

//==================== SIGNAL PROCESSING ================

//----------------------- noiseburst -------------------------
// White noise burst (adapted from Faust's karplus.dsp example)
noiseburst(g,P) = no.noise : *(g : trigger(P))
with {
  diffgtz(x) = (x-x') > 0;
  decay(n,x) = x - (x>0)/n;
  release(n) = + ~ decay(n);
  trigger(n) = diffgtz : release(n) : > (0.0);
};

P = ma.SR/freq; // fundamental period in samples
Pmax = 4096; // maximum P (for delay-line allocation)

ppdel = beta*P; // pick position delay
pickposfilter = fi.ffcombfilter(Pmax,ppdel,-1); // defined in filter.lib

excitation = noiseburst(gate,P) : *(gain);

rho = pow(0.001,1.0/(freq*t60)); // multiplies loop-gain

// Original EKS damping filter:
b1 = 0.5*B; b0 = 1.0-b1; // S and 1-S
dampingfilter1(x) = rho * ((b0 * x) + (b1 * x'));

// Linear phase FIR3 damping filter:
h0 = (1.0 + B)/2; h1 = (1.0 - B)/4;
dampingfilter2(x) = rho * (h0 * x' + h1*(x+x''));

loopfilter = dampingfilter2; // or dampingfilter1

// Use smooth function with pickangle parameter
smoothing(x) = x : *(1.0-pickangle) + (x' * pickangle);

filtered_excitation = excitation
            : smoothing
            : pickposfilter
            : fi.levelfilter(L,freq);

stringloop = (+ : de.fdelay4(Pmax, P-2)) ~ (loopfilter);

// Second output decorrelated somewhat for spatial diversity over imaging:
widthdelay = de.delay(Pmax,W*P/2);

// Assumes an optionally spatialized mono signal, centrally panned:
stereopanner(pan) = _,_ : *(1.0-pan), *(pan);

process = filtered_excitation : stringloop
          <: _, widthdelay : stereopanner(A);
