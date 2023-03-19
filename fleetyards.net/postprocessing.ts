import {readJSON, writeCSV} from 'https://deno.land/x/flat@0.0.15/mod.ts'

const filename = Deno.args[0]
const arr = await readJSON(filename)
const res = arr.map(({name, cargo}: { name: string; cargo: number }) => ({name, cargo}));
await writeCSV(`../nargit/models.csv`, res)
