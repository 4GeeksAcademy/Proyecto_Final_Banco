import React, { useContext } from "react";
import { Context } from "../../../../store/appContext";
import { MdAccountCircle } from "react-icons/md";
const BloqueoDesbloqueoCuentas = () => {
    const { store, actions } = useContext(Context);

    return (
        <div className={`bg-cuentas animacion-contenedor hover contenedor-componente-interactivo my-2 rounded text-center fw-bold ${store.borde} text-white d-flex flex-column`}>
            <span className="align-content-start mb-auto my-2">Cuentas</span>

            <p className="fs-1 simbolo"><MdAccountCircle /></p>
            <p className="enlace-claro">Bloqueo</p>
            <p className="enlace-claro">Desbloqueo</p>

        </div >
    )
}

export default BloqueoDesbloqueoCuentas