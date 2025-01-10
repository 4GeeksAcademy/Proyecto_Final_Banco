import React, { useContext } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";
import SaldoUsuario from "../component/Home/SaldoUsuario.jsx";
import TablaMovimientosUsuario from "../component/Home/TablaMovimientosUsuario.jsx";

export const Home = () => {
  const { store, actions } = useContext(Context);

  return (
    <div className={`${store.texto}`}>
      <SaldoUsuario />
      <TablaMovimientosUsuario />
    </div>
  );
};
