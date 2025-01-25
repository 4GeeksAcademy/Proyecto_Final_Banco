import React, { useContext, useEffect, useState } from "react";
import { Context } from "../../store/appContext";
import NotificacionCol from "./NotificacionCol.jsx";


const ContenedorNotificaciones = () => {
    const { store, actions } = useContext(Context);

    const [userLoad, SetUserLoad] = useState("elemento");
    useEffect(() => {
        SetUserLoad("elemento visible")
    }, [])
    return (
        <div className={store.notificaciones ? "d-none" : ""}>
            <div className="row">
                <div className="col-12 text-center fw-bold"><h3 className="text-center">Notificaciones</h3></div>
            </div>
            <div className={`row fw-bold ${store.borde} ${userLoad} py-2 px-3 scroll`}>
                <NotificacionCol cuerpo="No te olvides de solicitar tu tarjeta de coordenadas" />
                <NotificacionCol cuerpo="Si eres nuevo usuario puedes modificar tus configuraciones en el componente de abajo" />
                <NotificacionCol cuerpo="Necesitas ayuda? no dudes en contactar con nuestro Chat" />
                <NotificacionCol cuerpo="Tranferencia realizada hace 10 minutos" />
            </div>
        </div>
    )
}

export default ContenedorNotificaciones