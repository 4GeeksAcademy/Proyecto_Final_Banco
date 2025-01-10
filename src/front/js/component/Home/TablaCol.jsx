import React, { useContext } from "react";
import { Context } from "../../store/appContext";


const TablaCol = ({ fecha, monto, cuerpo, importe, saldo }) => {
    const { store, actions } = useContext(Context);
    return (
        <div className={`row fw-bold border-top-0 border-end-0 border-start-0 ${store.borde} py-2`}>
            <div className="col-3 text-center fw-bold align-content-center"><p>{fecha}</p></div>
            <div className="col-3 text-center fw-bold align-content-center"><p>{cuerpo}</p></div>
            <div className={`col-3 text-center fw-bold align-content-center ${monto === undefined ? "text-danger" : "text-success"}`}><p>{monto === undefined ? importe : monto}</p></div>
            <div className="col-3 text-center fw-bold align-content-center"><p>{monto === undefined ? saldo - importe : monto + saldo}</p></div>
        </div>
    )
}

export default TablaCol