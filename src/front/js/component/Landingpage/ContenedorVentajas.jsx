import React, { useContext, useEffect, useRef, useState, useTransition } from "react";
import { Context } from "../../store/appContext";
import { TbPigMoney } from "react-icons/tb";
import { TiDocumentText } from "react-icons/ti";
import { IoMdTime } from "react-icons/io";
import { useTranslation } from "react-i18next";

const ContenedorVentajas = () => {
    const { t } = useTranslation()
    const { store, actions } = useContext(Context);

    const [userLoad, SetUserLoad] = useState(false);
    const [userLoadv2, SetUserLoadv2] = useState(false);

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
                threshold: 0.1, // Al menos el 10% del componente debe estar visible
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
            SetUserLoad(true)
        } else {
            SetUserLoad(false)
        }
    }, [isVisible])

    useEffect(() => {
        SetUserLoadv2(true)
    }, [])

    return (<div className="contenedor-landing">
        <div className="container">
            <div className="row">
                <div className="col-12 text-center"><h2 className={`titulo-landing ${userLoadv2 ? "animacion-der visible" : "animacion-der"}`}>{t('Landing4.h2')}</h2></div>
            </div>
            <div className="row" ref={sectionRef}>
                <div className="col-12 col-lg-4 col-md-6 my-3 my-lg-0">
                    <div className={`mx-md-2 contenedor-ventajas text-success ${store.borde} ${userLoad ? "animacion-izq visible" : "animacion-izq"} ${store.fondo === "fondo-modo-claro" ? "bg-dark" : "bg-white"}`}>
                        <div className="d-flex flex-column text-center">
                            <i className="logo-ventajas"><TbPigMoney /></i>
                            <div className="text-center fs-4">
                                <span className="fw-bold my-2">{t('Landing4.p1_1')}</span>
                                <p>{t('Landing4.p1_2')}</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="col-12 col-lg-4 col-md-6 my-3 my-lg-0">
                    <div className={`mx-md-2 contenedor-ventajas text-success ${store.borde} ${userLoad ? "animacion-abajo visible" : "animacion-abajo"} ${store.fondo === "fondo-modo-claro" ? "bg-dark" : "bg-white"}`}>
                        <div className="d-flex flex-column text-center">
                            <i className="logo-ventajas"><TiDocumentText /></i>
                            <div className="text-center fs-4">
                                <span className="fw-bold my-2">{t('Landing4.p2_1')}</span>
                                <p>{t('Landing4.p2_2')}</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="col-12 col-lg-4 col-md-12 my-3 my-lg-0">
                    <div className={`mx-md-2 contenedor-ventajas text-success ${store.borde} ${userLoad ? "animacion-der visible" : "animacion-der"} ${store.fondo === "fondo-modo-claro" ? "bg-dark" : "bg-white"}`}>
                        <div className="d-flex flex-column text-center">
                            <i className="logo-ventajas"><IoMdTime /></i>
                            <div className="text-center fs-4">
                                <span className="fw-bold my-2">{t('Landing4.p3_1')}</span>
                                <p>{t('Landing4.p3_2')}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>)
}

export default ContenedorVentajas

