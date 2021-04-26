import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { useHistory } from "react-router-dom";
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import styles from "./style.module.css"

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));

export default function ButtonAppBar() {
  const classes = useStyles();
  const history=useHistory()
  const handleOCRClick=()=>{
    history.push("./")
  }
  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" className={classes.title}>
            <div className={styles.typo} onClick={handleOCRClick}>
              OCR
            </div>
          </Typography>

          <Button color="inherit" onClick={()=>{history.push("/about")}}>About</Button>
          <Button color="inherit" onClick={()=>{history.push("/contributors")}}>Who are we</Button>
        </Toolbar>
      </AppBar>
    </div>
  );
}