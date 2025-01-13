import React, { useContext, useEffect, useState } from "react";
import { Context } from "../../store/appContext";


const NotificacionCol = ({ cuerpo }) => {
    const { store, actions } = useContext(Context);

    const [userLoad, SetUserLoad] = useState("elemento-noti");
    useEffect(() => {
        SetUserLoad("elemento-noti visible")
    }, [])

    return (
        <div className={`col-12 text-center fw-bold align-content-center border-top-0 border-end-0 border-start-0 ${store.borde} py-3 my-2 ${userLoad}`}><p>{cuerpo}</p></div>
    )
}

export default NotificacionCol