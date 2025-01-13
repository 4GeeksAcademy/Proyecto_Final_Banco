import React, { useEffect, useRef, useState } from "react";
import BloqueoDesbloqueoCuentas from "./Componentes/BloqueoDesbloqueoCuentas.jsx";

const ListaInteractiva = () => {

    const [firstCol, SetFirstCol] = useState("componente-izquierdo")
    const [thCol, SetThCol] = useState("componente-izquierdov2");;
    const [secCol, SetSecCol] = useState("componente-derecho");
    const [FoCol, SetFoCol] = useState("componente-derechov2");

    // logica para mostrar el conteindo si el usuario esta en la seccion del componente
    const [isVisible, setIsVisible] = useState(false);
    const sectionRef = useRef(null);

    // controla la variable para cambiarla si el usuario se encuentra encima del componente
    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
                // entry.isIntersecting indica si el elemento es visible
                setIsVisible(entry.isIntersecting);
            },
            {
                root: null, // Usar la ventana como viewport
                rootMargin: '0px', // Sin márgenes
                threshold: 0, // Al menos el 1% del componente debe estar visible
            }
        );

        if (sectionRef.current) {
            observer.observe(sectionRef.current); // Observar el componente
        }

        return () => {
            // Limpiar el observer al desmontar el componente
            if (sectionRef.current) {
                observer.unobserve(sectionRef.current);
            }
        };
    }, []);

    useEffect(() => {
        if (isVisible) {
            SetFirstCol("componente-izquierdo visible")
            SetSecCol("componente-derecho visible")
            SetThCol("componente-izquierdov2 visible")
            SetFoCol("componente-derechov2 visible")
        } else {
            SetFirstCol("componente-izquierdo")
            SetSecCol("componente-derecho")
            SetThCol("componente-izquierdov2")
            SetFoCol("componente-derechov2")
        }
    }, [isVisible])

    return (
        <div className="container-fluid w-85" ref={sectionRef}>
            <div className="row">
                <div className={`col-2 ${firstCol}`}><BloqueoDesbloqueoCuentas /></div>
                <div className={`col-4 ${thCol}`}><div className="color-principal contenedor-componente-interactivo my-2 rounded">Historial de transacciones</div></div>
                <div className={`col-3 ${FoCol}`}><div className="color-principal contenedor-componente-interactivo my-2 rounded">Alertas</div></div>
                <div className={`col-3 ${secCol}`}><div className="color-principal contenedor-componente-interactivo my-2 rounded">Tarjetas</div></div>
            </div>
            <div className="row">
                <div className={`col-4 ${firstCol}`}><div className="color-principal contenedor-componente-interactivo my-2 rounded">Tienda</div></div>
                <div className={`col-2 ${thCol}`}><div className="color-principal contenedor-componente-interactivo my-2 rounded">Productos</div></div>
                <div className={`col-4 ${FoCol}`}><div className="color-principal contenedor-componente-interactivo my-2 rounded">Configuracion</div></div>
                <div className={`col-2 ${secCol}`}><div className="color-principal contenedor-componente-interactivo my-2 rounded">Atencion al Cliente</div></div>
            </div>
            <div className="row">
                <div className={`col-2 ${firstCol}`}><div className="color-principal contenedor-componente-interactivo my-2 rounded">Enlaces Legales</div></div>
                <div className={`col-3 ${thCol}`}><div className="color-principal contenedor-componente-interactivo my-2 rounded">Recursos</div></div>
                <div className={`col-4 ${FoCol}`}><div className="color-principal contenedor-componente-interactivo my-2 rounded">Seguridad</div></div>
                <div className={`col-3 ${secCol}`}><div className="color-principal contenedor-componente-interactivo my-2 rounded">Certificaciones</div></div>
            </div>
            <div className="row">
                <div className={`col-2 ${firstCol}`}><div className="color-principal contenedor-componente-interactivo my-2 rounded">Inversiones</div></div>
                <div className={`col-3 ${thCol}`}><div className="color-principal contenedor-componente-interactivo my-2 rounded">Tarjeta de Cordenadas</div></div>
                <div className={`col-4 ${FoCol}`}><div className="color-principal contenedor-componente-interactivo my-2 rounded">Divisas</div></div>
                <div className={`col-3 ${secCol}`}><div className="color-principal contenedor-componente-interactivo my-2 rounded">Redes Sociales</div></div>
            </div>
        </div>
    )
}

export default ListaInteractiva

