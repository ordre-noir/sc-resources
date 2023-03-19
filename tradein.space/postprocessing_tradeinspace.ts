// Is this the cause of the failures ?
// import 'https://deno.land/x/flat@0.0.10/mod.ts'


// install requirements with pip
const pip_install = Deno.run({
    cmd: ['python', '-m', 'pip', 'install', '-r', 'requirements.txt'],
});

await pip_install.status();


// Forwards the execution to the python script
const py_run = Deno.run({
    cmd: ['python', './tradein.space/postprocessing_tradeinspace.py', '-i'].concat(Deno.args),
});


const {code} = await py_run.status()
Deno.exit(code);
