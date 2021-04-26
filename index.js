const express = require("express")
const { spawn } = require('child_process');

const ls = spawn('ls',['-a','>','file.txt']);
ls.stdout.on('data',data=>{
    console.log(`standard output: ${data}`);
})
ls.stderr.on('err',err=>{
    console.log(`standard err: ${err}`);
})
ls.on('close',code=>{
    console.log(`child process ended with code ${code}`)
})

const app=express();

app.get("/",(req,res)=>{
    res.send("<h1>Hello world</h1>")
})

// app.listen(3000,()=>{
//     console.log("server started at port 3000")
// })