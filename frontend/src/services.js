import axios from "axios"

export const getHeading =()=> axios.get("/heading").then((res, err) => res.data);

export const uploadFile =data=>axios.post("/upload/file",data).then((res,err)=>res.data)
