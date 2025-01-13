import React, { useContext, useEffect } from "react";
import { Context } from "../store/appContext";
import "../../styles/login.css";
import ContenedorLoginYRegistro from "../component/Login/ContenedorLogin.jsx";

export const Login = () => {
  useEffect(() => {
    localStorage.clear();
  }, []);
  return (
    <div className="text-center my-5 contenedor-main h-100">
      <ContenedorLoginYRegistro></ContenedorLoginYRegistro>
    </div>
  );
};
