declare name "EKS Guitar Sequencer - Progressive Rock Style";
declare author "Julius Smith / Modified";
declare version "1.0";
declare license "STK-4.3";

import("stdfaust.lib");

//==================== SEQUENCER ================

// Simple 16-step sequencer
gate_pattern = ba.beat(tempo) : ba.pulse_countup_loop(15, 1);
step = gate_pattern : int;

tempo = hslider("tempo [unit:BPM]", 138, 60, 200, 1) / 60;

// Progressive rock style bass pattern (inspired, not copied)
// Pattern in semitones relative to root (E2 = MIDI 40)
note_sequence(i) = ba.take(i+1, (
    0,  // E
    7,  // B
    5,  // A
    3,  // G
    0,  // E
    7,  // B
    5,  // A
    10, // D
    0,  // E
    7,  // B
    5,  // A
    3,  // G
    5,  // A
    3,  // G
    2,  // F#
    0   // E
));

root_note = hslider("root_note [midi:keynum]", 40, 24, 60, 1);
current_note = root_note + note_sequence(step);
freq = ba.midikey2hz(current_note);

// Gate/trigger
gate = ba.beat(tempo) : ba.impulsify;

//==================== EKS GUITAR SYNTH ================

gain = hslider("gain", 0.8, 0, 10, 0.01);

// Pick angle in [0,0.9]:
pickangle = 0.9 * hslider("pick_angle",0.1,0,0.9,0.1);

// Normalized pick-position in [0,0.5]:
beta = hslider("pick_position", 0.13, 0.02, 0.5, 0.01);

// String decay time in seconds:
t60 = hslider("decaytime_T60", 4, 0, 10, 0.01);

// Normalized brightness in [0,1]:
B = hslider("brightness", 0.5, 0, 1, 0.01);

// Dynamic level specified as dB level desired at Nyquist limit:
L = hslider("dynamic_level", -10, -60, 0, 1) : ba.db2linear;

// Spatial "width":
W = hslider("center-panned spatial width", 0.5, 0, 1, 0.01);
A = hslider("pan angle", 0.5, 0, 1, 0.01);

//----------------------- noiseburst -------------------------
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
pickposfilter = fi.ffcombfilter(Pmax,ppdel,-1);

excitation = noiseburst(gate,P) : *(gain);

rho = pow(0.001,1.0/(freq*t60)); // multiplies loop-gain

// Linear phase FIR3 damping filter:
h0 = (1.0 + B)/2; h1 = (1.0 - B)/4;
dampingfilter(x) = rho * (h0 * x' + h1*(x+x''));

loopfilter = dampingfilter;

filtered_excitation = excitation : si.smoo
            : pickposfilter : fi.levelfilter(L,freq);

stringloop = (+ : de.fdelay4(Pmax, P-2)) ~ (loopfilter);

// Second output decorrelated somewhat for spatial diversity:
widthdelay = de.delay(Pmax,W*P/2);

// Stereo panner:
stereopanner(pan) = _,_ : *(1.0-pan), *(pan);

process = filtered_excitation : stringloop
          <: _, widthdelay : stereopanner(A);
