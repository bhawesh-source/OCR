const express = require('express')
const fileUpload = require("express-fileupload")
const fs=require("fs")
const {execFile} = require('child_process');

const app = express()
app.use(fileUpload())
const port = 3000;
let fileName=""

app.post('/upload/file',(req,res)=>{
    try{
        const {myFile} = req.files
        fs.writeFileSync(`./data/${myFile.name}`,myFile.data)
        fileName=myFile.name
    }
    catch(err){
        res.send(err)
    }
    finally{
        res.send({status:"success"})
    }
    
})
app.get("/convert",(req,res)=>{
    var dataToSend;
    const python = execFile('python', ['engine/main.py',`${__dirname}/data/${fileName}`]);
    python.stdout.on('data', function (data) {   
     dataToSend = data.toString();
     console.log(dataToSend)
    });
    python.on("error",(err)=>{
        console.log("err",err)
    })
    python.on('close', (code) => {
       console.log("close",code) 
       res.send(dataToSend)
    });
})

app.listen(port, () => console.log(`listening on port 3000!`))