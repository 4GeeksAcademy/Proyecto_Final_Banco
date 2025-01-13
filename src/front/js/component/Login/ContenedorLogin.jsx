import React, { useContext, useEffect, useState } from "react";
import Register from "./Register.jsx";
import Login from "./Login.jsx";
import { Context } from "../../store/appContext.js";
import ContenedorAnimado from "./ContenedorAnimado.jsx";

export const ContenedorLoginYRegistro = () => {
    const [Registro, setRegistro] = useState(true) // cambiar el estado de la animacion para que sea interactiva
    const { store, actions } = useContext(Context);

    const [userLoad, SetUserLoad] = useState("elemento-login");
    useEffect(() => {
        SetUserLoad("elemento-login visible")
    }, [])

    //contenedor para registrarse o iniciar sesion con animacion incluida
    return (
        <div className={`contenedor container w-75 h-100 d-flex ${Registro === true ? "" : "panel-derecho-activo"} ${store.borde} ${userLoad}`}>
            {/* contenedor registro*/}
            <Register />
            {/* contenedor login*/}
            <Login />
            {/*Contenedor animacion*/}
            <ContenedorAnimado funcion={setRegistro} />
        </div>
    )
};

export default ContenedorLoginYRegistro
