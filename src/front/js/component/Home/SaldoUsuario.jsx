import React, { useContext, useEffect, useState } from "react";
import { Context } from "../../store/appContext";

const SaldoUsuario = () => {
    const { store, actions } = useContext(Context);
    const [hidden, SetHidden] = useState(false);
    const [userLoad, SetUserLoad] = useState("elemento");
    useEffect(() => {
        SetUserLoad("elemento visible")
    }, [])


    return (<div className={`container my-3 p-3 color-principal w-100 rounded-3 ${store.texto} ${store.borde} ${userLoad}`}>
        <div className="row">
            <div className="col-12">
                <div className="row">
                    <div className="col-4 d-flex flex-column text-center">
                        <p className="fs-1 fw-light">Hola, <span className="fw-bold">User</span></p>
                    </div>
                    <div className="col-8 text-end"><button className="btn btn-black" onClick={() => {

                    }}>ejemplo</button></div>
                </div>
            </div>
        </div>
        <div className="row">
            <div className="col-4 d-flex flex-column">
                <div className="row">
                    <div className="col-6 px-1 text-end"><p className="fw-light my-2">Saldo Disponible:</p></div>
                    <div className="col-6  px-1 text-start"><span className="fs-3 fw-bold">0</span></div>
                </div>
                <div className="row">
                    <div className="col-6 px-1 text-end"><p className="fw-light my-2">Saldo Retenido: </p></div>
                    <div className="col-6  px-1 text-start"><span className="fs-3 fw-bold">0</span></div>
                </div>
            </div>
            <div className="col-8"></div>
        </div>
    </div>)
}

export default SaldoUsuario