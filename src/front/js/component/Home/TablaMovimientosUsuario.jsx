import React, { useContext, useEffect, useState } from "react";
import { Context } from "../../store/appContext";
import TablaCol from "./TablaCol.jsx";

const TablaMovimientoUsuario = () => {
    const { store, actions } = useContext(Context);
    const [userLoad, SetUserLoad] = useState("elemento-segundario");
    useEffect(() => {
        SetUserLoad("elemento-segundario visible")
    }, [])


    return (<div className={`container my-3 p-3 w-100 rounded-3 ${userLoad}`}>
        <div className="row">
            <div className="col-12 text-center fw-bold">
                <h2>Movimientos</h2>
            </div>
        </div>
        <div className="row my-3">
            <div className="col-3 text-center fw-bold"><p>Dia</p></div>
            <div className="col-3 text-center fw-bold"><p>Establecimiento / Concepto</p></div>
            <div className="col-3 text-center fw-bold"><p>Importe</p></div>
            <div className="col-3 text-center fw-bold"><p>Saldo</p></div>
        </div>
        <div>
            <TablaCol fecha="01/03/2024" cuerpo="Mc Donalds / Sevilla" importe={12.9} saldo={400} />
            <TablaCol fecha="01/03/2024" cuerpo="Transferencia" importe={200} saldo={600} />
            <TablaCol fecha="01/03/2024" cuerpo="Alquiler" importe={800} saldo={1400} />
            <TablaCol fecha="01/03/2024" cuerpo="Nomina" monto={1000} saldo={400} />
            <TablaCol fecha="01/03/2024" cuerpo="Mc Donalds / Sevilla" importe={12.9} saldo={400} /></div>
    </div>)
}

export default TablaMovimientoUsuario