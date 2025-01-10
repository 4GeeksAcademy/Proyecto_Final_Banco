import React, { useContext } from "react";
import { Context } from "../store/appContext";
import "../../styles/login.css";
import ContenedorLoginYRegistro from "../component/Login/ContenedorLogin.jsx";

export const Login = () => {
  const { store, actions } = useContext(Context);

  return (
    <div className="text-center my-5 contenedor-main h-100">
      <ContenedorLoginYRegistro></ContenedorLoginYRegistro>
    </div>
  );
};
