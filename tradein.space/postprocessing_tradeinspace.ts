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

const [{code}, rawError] = await Promise.all([
    py_run.status(),
    py_run.stderrOutput(),
]);

if (code !== 0) {
    const errorString = new TextDecoder().decode(rawError);
    console.log(errorString);
    Deno.exit(code);
}
