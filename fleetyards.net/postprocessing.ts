import {readJSON, writeCSV} from 'https://deno.land/x/flat@0.0.15/mod.ts'
import {join} from 'https://deno.land/std/path/mod.ts'

console.log(Deno.args)
const filename = join("..", Deno.args[0])
const arr = await readJSON(filename)
const res = arr.map(({name, cargo}: { name: string; cargo: number }) => ({name, cargo}));
await writeCSV(join("..", "nargit", "models.csv"), res)
