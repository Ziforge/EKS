declare name "Progressive Rock Bass Sequencer";
declare author "Faust Example";
declare version "1.0";

import("stdfaust.lib");

// Simple 16-step sequencer with gate and pitch
gate_pattern = ba.beat(tempo) : ba.pulse_countup_loop(15, 1);
step = gate_pattern : int;

tempo = hslider("tempo [unit:BPM]", 138, 60, 200, 1) / 60;

// Iconic progressive rock style bass pattern (inspired, not copied)
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

// Simple bass synth
bass_synth(f, g) = os.sawtooth(f) * env
with {
    env = g : en.ar(0.001, decay);
    decay = hslider("decay", 0.3, 0.1, 2.0, 0.01);
};

// Add some filtering for analog bass sound
bass_filter = fi.lowpass(2, cutoff)
with {
    cutoff = hslider("cutoff [unit:Hz]", 800, 200, 2000, 10);
};

// Optional distortion/drive
drive_amount = hslider("drive", 1.0, 1.0, 5.0, 0.1);
soft_clip(x) = x : ma.tanh;

process = bass_synth(freq, gate)
        : bass_filter
        : *(drive_amount)
        : soft_clip
        : *(0.5)
        <: _, _;
