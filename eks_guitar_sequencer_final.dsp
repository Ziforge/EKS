declare name "EKS Guitar Sequencer - Progressive Rock Arpeggio";
declare author "Julius Smith / Modified";
declare version "1.0";
declare license "STK-4.3";
declare copyright "Julius Smith";
declare reference "http://ccrma.stanford.edu/~jos/pasp/vegf.html";

import("stdfaust.lib");

//==================== SEQUENCER ================

// Run/stop button
run = checkbox("run_sequencer");

// Direct Hz calculation for 16th notes at 180 BPM
// 180 BPM = 3 beats per second, 16th notes = 12 notes per second
note_rate = hslider("note_rate [unit:Hz]", 12, 1, 30, 0.1);

// Generate clock pulses at note_rate Hz
clock = os.lf_imptrain(note_rate) * run;

// Step counter (0-31)
step = clock : ba.pulse_countup_loop(31, 1) : int;

// Fast arpeggiated pattern
note_at_step(s) =
    (s == 0)  * 0 +   // E
    (s == 1)  * 3 +   // G
    (s == 2)  * 7 +   // B
    (s == 3)  * 12 +  // E
    (s == 4)  * 15 +  // G
    (s == 5)  * 12 +  // E
    (s == 6)  * 7 +   // B
    (s == 7)  * 3 +   // G
    (s == 8)  * 0 +   // E
    (s == 9)  * 7 +   // B
    (s == 10) * 12 +  // E
    (s == 11) * 15 +  // G
    (s == 12) * 19 +  // B
    (s == 13) * 15 +  // G
    (s == 14) * 12 +  // E
    (s == 15) * 7 +   // B
    (s == 16) * 5 +   // A
    (s == 17) * 7 +   // B
    (s == 18) * 12 +  // E
    (s == 19) * 14 +  // F#
    (s == 20) * 12 +  // E
    (s == 21) * 7 +   // B
    (s == 22) * 5 +   // A
    (s == 23) * 3 +   // G
    (s == 24) * 0 +   // E
    (s == 25) * 7 +   // B
    (s == 26) * 12 +  // E
    (s == 27) * 15 +  // G
    (s == 28) * 12 +  // E
    (s == 29) * 7 +   // B
    (s == 30) * 5 +   // A
    (s == 31) * 3;    // G

root_note = hslider("root_note [midi:keynum]", 64, 48, 84, 1);
current_note = root_note + note_at_step(step);
freq = ba.midikey2hz(current_note);

// Gate is the clock signal
gate = clock;

//==================== EKS GUITAR SYNTH (FULL ORIGINAL) ================

gain = hslider("gain", 1.0, 0, 10, 0.01);

// Additional parameters (MIDI "controllers"):

// Pick angle in [0,0.9]:
pickangle = 0.9 * hslider("pick_angle",0.1,0,0.9,0.1);

// Normalized pick-position in [0,0.5]:
beta = hslider("pick_position [midi: ctrl 0x81]", 0.13, 0.02, 0.5, 0.01);
       // MIDI Control 0x81 often "highpass filter frequency"

// String decay time in seconds:
t60 = hslider("decaytime_T60", 1.0, 0, 10, 0.01);  // Short decay

// Normalized brightness in [0,1]:
B = hslider("brightness [midi:ctrl 0x74]", 0.7, 0, 1, 0.01);// Bright
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

//==================== MODULATION ================

// LFO for modulation
mod_rate = hslider("mod_rate [unit:Hz]", 0.5, 0.01, 10, 0.01);
mod_depth = hslider("mod_depth", 0.5, 0, 1, 0.01);

// LFO oscillator (sine wave)
lfo = os.osc(mod_rate);

// Pan modulation: LFO modulates the pan position
auto_pan = A + (lfo * mod_depth * 0.5);
auto_pan_clipped = max(0, min(1, auto_pan));

//==================== REVERB ================

// Reverb parameters
reverb_mix = hslider("reverb_mix", 0.3, 0, 1, 0.01);

// Use built-in stereo reverb
my_reverb = dm.zita_light;

process = filtered_excitation : stringloop
          <: _, widthdelay : stereopanner(auto_pan_clipped)
          : (_, _ <: _, _, my_reverb) : _, _, *(reverb_mix), *(reverb_mix) : +, +;
