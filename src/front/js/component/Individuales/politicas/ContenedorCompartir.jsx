import React, { useContext, useEffect, useRef, useState } from "react";
import ColLateral from "../ColLateral.jsx";

const ContenedorCompartir = () => {
    const [userLoad, SetUserLoad] = useState(false);
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
    return (
        <div className="container espaciado-fondo" ref={sectionRef}>
            <h1 className={`text-center titulo-politica my-3 ${userLoad ? "animacion-arriba visible" : "animacion-arriba"}`}>Política de Compartición de Datos en GeekBank</h1>
            <p className={`fs-3 text-center my-3 ${userLoad ? "animacion-abajo visible" : "animacion-abajo"}`}>
                En GeekBank, valoramos su privacidad y nos comprometemos a proteger su información personal.
                Solo compartimos sus datos con terceros en los siguientes casos:
            </p>
            <div className="row my-3">
                <ColLateral width="w-25" text="Servicios" position="left" userLoad={userLoad} />
                <ColLateral width="w-25" text="Legales" position="" userLoad={userLoad} />
                <ColLateral width="w-25" text="Consentimiento" position="left" userLoad={userLoad} />
            </div>
            <p className={`fs-3 text-center my-3 ${userLoad ? "animacion-abajo visible" : "animacion-abajo"}`}>
                Servicios
                Legales
                Consentimiento
                En todo momento, nos aseguramos de que cualquier compartición de datos se realice de manera responsable y transparente, priorizando siempre su seguridad y privacidad. Si tiene alguna pregunta sobre cómo compartimos sus datos, puede contactarnos en cualquier momento.
            </p>
        </div>
    )

}

export default ContenedorCompartir