const express=require("express");
const upload=require("express-fileupload");
const bodyParser = require("body-parser");
const app=express();
const spawn=require("child_process").spawn;
const fs = require("fs");
var yr,course,deg;
const pathInclude = __dirname + "/Test/Include/";
app.use(bodyParser.urlencoded({extended:true}));
app.use(express.static(__dirname + '/public'));
app.use(upload());
app.get("/",function(req,res){
  res.sendFile(__dirname  +"/login.html");
});
app.post("/",function(req,res){
  var userid = req.body.userid;
  var password = req.body.pswrd;
  if(userid==="admin" && password==="admin123")
  {
    res.sendFile(__dirname + "/index.html");
  }
  else
  {
    res.send("Invalid Username/Password");
  }
})
app.get("/download",function(req,res){
  res.download(__dirname + "/" + course + "_shortlisted.zip",yr + "--" + course + ".zip");
  // var filePath = "C:/Users/Sahil/Desktop/Project1/site/" + course + "_shortlisted.zip";
  // fs.unlinkSync(filePath);
});

app.post("/upload",function(req,res){
  if(req.files){
    // console.log(req.files);
    var file=req.files.file;
    var filename=file.name;
    yr = Number(req.body.year);
    deg = req.body.degree;
    // console.log(yr);
    // console.log(deg);

    // console.log(filename);
    file.mv('./'+filename,function(err){
      if(err)
      {
        res.send(err);
      }
      else if(deg[0]==='M')
      {
        course = "Mtech";
        fs.rename(__dirname+ "/" +filename, "mtech_file.csv", function(err){
        if ( err ) console.log('ERROR: ' + err);
        });
        const process=spawn("python",["./mtech_shortlisting.py",yr]);
        // res.send("file uploaded");
        res.sendFile(__dirname  +"/index2.html");
        // res.downlaod(__dirname+"/upload/sawan.reserch.cpp",'file.cpp');
      }
      else if(deg[0]==='P')
      {
        course = "PhD";
        fs.rename(__dirname+"/"+filename, "phd_file.csv", function(err){
        if ( err ) console.log('ERROR: ' + err);
        });
        const process=spawn("python",["./phd_shortlisting.py",yr]);
        // res.send("file uploaded");
        res.sendFile(__dirname  +"/index2.html");
      }
    });
  }
});
app.listen(3000,function(){
  console.log("Server is running at port 3000");
});
