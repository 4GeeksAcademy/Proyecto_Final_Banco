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
        <>
            <div className="row">
                <div classname="col-12 text-center fw-bold"><h3 className="text-center">Notificaciones</h3></div>
            </div>
            <div className={`row fw-bold ${store.borde} ${userLoad} py-2 px-3 scroll`}>
                <NotificacionCol cuerpo="Si necesitas ayuda contacta con nosotros via Chat/Correo en contacto" />
                <NotificacionCol cuerpo="Tranferencia realizada hace 10 minutos" />
                <NotificacionCol cuerpo="Tranferencia realizada hace 10 minutos" />
                <NotificacionCol cuerpo="Tranferencia realizada hace 10 minutos" />
                <NotificacionCol cuerpo="Tranferencia realizada hace 10 minutos" />
                <NotificacionCol cuerpo="Tranferencia realizada hace 10 minutos" />
                <NotificacionCol cuerpo="Tranferencia realizada hace 10 minutos" />
                <NotificacionCol cuerpo="Tranferencia realizada hace 10 minutos" />
                <NotificacionCol cuerpo="Tranferencia realizada hace 10 minutos" />
                <NotificacionCol cuerpo="Tranferencia realizada hace 10 minutos" />
            </div>
        </>
    )
}

export default ContenedorNotificaciones