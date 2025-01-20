import React, { useContext, useEffect, useRef, useState } from "react";
import ContenedorCuadrado from "../ContenedorCuadrado.jsx";
import { IoIosInformationCircleOutline } from "react-icons/io";
import { IoDocumentOutline } from "react-icons/io5";
import { CiLock } from "react-icons/ci";

const ContenedorResponsabilidad = () => {
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
        <div className="container">
            <h1 className={`text-center titulo-politica ${userLoad ? "animacion-abajo visible" : "animacion-abajo"}`}>Responsabilidades Del Cliente</h1>
            <p className={`fs-3 text-center ${userLoad ? "animacion-abajo visible" : "animacion-abajo"}`} ref={sectionRef}>
                En GeekBank, ofrecemos soluciones bancarias seguras y eficientes para satisfacer sus necesidades financieras.
                Al utilizar nuestros servicios, usted se compromete a hacerlo de manera responsable y conforme a las leyes y
                regulaciones aplicables. Es su responsabilidad proporcionar información precisa y actualizada al registrarse y realizar
                transacciones. No debe utilizar nuestros servicios para actividades ilegales, fraudulentas o malintencionadas. GeekBank
                se reserva el derecho de suspender o cancelar su acceso si detectamos un uso inapropiado. Además, le recomendamos proteger
                sus dispositivos y datos personales con medidas de seguridad adecuadas. Al acceder a nuestros servicios, se compromete a seguir
                estos términos para garantizar una experiencia segura y eficiente.
            </p>
            <div className="row">
                <div className="col-12 col-lg-4"><ContenedorCuadrado position="left" text="Proveer información veraz y actualizada" title="Informacion" logo={<IoDocumentOutline />} /></div>
                <div className="col-12 col-md-6 col-lg-4"><ContenedorCuadrado position="bottom" text="Proteger la confidencialidad de sus credenciales" title="Confidencialidad" logo={<CiLock />} /></div>
                <div className="col-12 col-md-6 col-lg-4"><ContenedorCuadrado position="right" text="Notificar inmediatamente cualquier uso no autorizado de su cuenta" title="Responsabilidad" logo={<IoIosInformationCircleOutline />} /></div>
            </div>
        </div>
    )
}

// logo, position, text, title, userLoad

{/* <li>Proveer información veraz y actualizada.</li>
<li>Proteger la confidencialidad de sus credenciales de acceso.</li>
<li>
    Notificar inmediatamente cualquier uso no autorizado de su cuenta.
</li> */}

export default ContenedorResponsabilidad



