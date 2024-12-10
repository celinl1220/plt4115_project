// Generated JavaScript using Tone.js
import * as Tone from 'tone';


const durations_dict = {
    w: "1n",
    h: "2n",
    q: "4n",
    e: "8n",
    s: "16n"
};

Tone.Transport.bpm.value = 144;
let original_ks = "cmajor";
let ks_key = original_ks.charAt(0).toUpperCase() + '4';
let ks_majmin = original_ks.slice(1);
const ks = Tonal.Scale.get(ks_key + ' ' + ks_majmin).notes;

const synth = new Tone.Synth().toDestination();

async function playMelody() {
    await Tone.start();
    for (var i = 0; i < melody.length; i++) {
        var melody_i = melody[i];
        var melody_durations_i = melody_durations[i];
        for (var j = 0; j < melody_i.length; j++) {
            if (melody_i[j]) {
                synth.triggerAttackRelease(melody_i[j], melody_durations_i[j]);
            }
        }
    }
    Tone.Transport.start();
}

playMelody();
