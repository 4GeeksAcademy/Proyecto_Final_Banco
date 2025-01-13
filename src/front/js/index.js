//import react into the bundle
import React from "react";
import ReactDOM from "react-dom";

//include your index.scss file into the bundle
import "../styles/index.css";

//import your own components
import Layout from "./layout";

// importacion de la libreria de traduccion
import './i18n';

//render your react application
ReactDOM.render(
    <React.StrictMode>
        <Layout />
    </React.StrictMode>
, document.querySelector("#app"));
