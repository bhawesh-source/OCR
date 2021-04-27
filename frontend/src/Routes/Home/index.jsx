import React, { useState } from "react";
import { getHeading, uploadFile, convertFile  } from "../../services";
import { Button, TextField, LinearProgress } from "@material-ui/core";
import style from "./style.module.css";

export default () => {
  const [selectedFile, setSelectedFile] = useState({ name: "" });
  const [fileUploaded, setFileUploaded] = useState(0);
  const [output, setOutput] = useState("");
  const onFileChange = (event) => {
    console.log(event.target);
    if (selectedFile.name == "") setSelectedFile(event.target.files[0]);
    setFileUploaded(0);
    setOutput("")
  };
  const onFileUpload = async () => {
    const formData = new FormData();

    formData.append("myFile", selectedFile, selectedFile.name);

    console.log(selectedFile);
    uploadFile(formData)
      .then(() => {
        setFileUploaded(1);
      })
      .catch((err) => {
        setFileUploaded(-1);
      });
  };
  const handleConvert=async ()=>{
    setOutput("!!loading")
    const res=await convertFile();
    setOutput(res)
  }
  return (
    <React.Fragment>
      <br></br>
      <div className={style.upper}>
        <TextField
          id="standard-basic"
          label="File Name"
          value={selectedFile.name}
          className={style.TextField}
        />
        <Button
          variant="contained"
          component="label"
          className={style.selectButton}
        >
          Select File
          <input type="file" hidden onChange={onFileChange} />
        </Button>
        <Button
          variant="contained"
          component="label"
          onClick={onFileUpload}
          className={style.uploadButton}
        >
          Upload File
        </Button>
      </div>
      {fileUploaded !== 0 ? fileUploaded === 1 ? (
        <div>
          <h2 className={style.successText}>File Uploaded Successfully</h2>
          <Button
            variant="contained"
            component="label"
            className={style.convertButton}
            onClick={handleConvert}
          >
            Convert
          </Button>
          <br></br>
          <div className={style.TextFieldOutput}>
            {output === "!!loading" ? (
              <LinearProgress />
            ) : (
              <p className={style.outputText}>{output}</p>
            )}
          </div>
        </div>
      ) : (
        <div>
          <h2 className={style.failureText}>Something went Wrong!!</h2>
        </div>
      ):null}
    </React.Fragment>
  );
};
