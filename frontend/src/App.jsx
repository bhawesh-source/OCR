import React from "react";
import { Container } from "@material-ui/core";
import { BrowserRouter as Router, Switch, Route,useHistory } from "react-router-dom";
import NavBar from "./components/Navbar/Navbar";
import About from "./Routes/About"
import Contributors from "./Routes/Contributers"
import Home from "./Routes/Home"

export default () => {
  return (
    <React.Fragment>
        <Router>
      <Container>
        <NavBar maxWidth="sm" />
      </Container>
      
        <Switch>
          <Route path="/about">
            <About />
          </Route>
          <Route path="/contributors">
            <Contributors />
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </Router>
    </React.Fragment>
  );
};
