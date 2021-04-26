const express = require('express')
const fileUpload = require("express-fileupload")
const fs=require("fs")
const {spawn} = require('child_process');

const app = express()
app.use(fileUpload())
const port = 3000;
let fileName=""

app.get('/heading', (req, res) => { 
 var dataToSend;
 const python = spawn('python3', ['main.py',"1.png"]);
 python.stdout.on('data', function (data) {
  dataToSend = data.toString();
 });
 python.on('close', (code) => {
    res.send(dataToSend)
 });
})
app.post('/upload/file',(req,res)=>{
    try{
        const {myFile} = req.files
        fs.writeFileSync(`${myFile.name}`,myFile.data)
        fileName=myFile.name
    }
    catch(err){
        res.send(err)
    }
    finally{
        console.log("here")
        res.send({status:"success"})
    }
    
})
app.get("./convert",(req,res)=>{
    var dataToSend;
    const python = spawn('python3', ['script.py']);
    python.stdout.on('data', function (data) {
     dataToSend = data.toString();
    });
    python.on('close', (code) => {
       res.send(dataToSend)
    });
})

app.listen(port, () => console.log(`listening on port ${port}!`))