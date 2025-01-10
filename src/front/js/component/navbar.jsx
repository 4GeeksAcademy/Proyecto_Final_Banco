import React, { useContext, useEffect, useState } from "react";
import logo_negro from "../../img/logo-negro.png";
import logo_blanco from "../../img/logo-blanco.png";
import "../../styles/navbar.css";
import { FaMoon } from "react-icons/fa";
import { MdWbSunny } from "react-icons/md";
import { GiWorld } from "react-icons/gi";
import { IoClose } from "react-icons/io5";

// Importacion de la traduccion
import { useTranslation } from "react-i18next";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";

export const Navbar = () => {
	const { store, actions } = useContext(Context);

	// Logica para botones onclick modal/traduccion
	const { t, i18n } = useTranslation();
	const handleLanguageChange = (language) => {
		i18n.changeLanguage(language);
	};

	const [btn, setbtn] = useState(false) // estado boton modo claro, modo oscuro
	const navigate = useNavigate(null);

	useEffect(() => {
		btn === true ? actions.CambiarModo(true) : actions.CambiarModo(false)
	}, [btn])

	return (
		<div> {/* modo oscuro y claro */}
			<div className="modal fade" id="lenguajes" tabIndex="-1" aria-labelledby="label" aria-hidden="true">
				{/* Modal selector de idiomas */}
				<div className="modal-dialog">
					<div className={`modal-content rounded-3 ${store.fondo} borde-brillante`}>
						<div className="modal-header">
							<h1 className="modal-title fs-5 " id="label">{t('Languages')}</h1>
							<div className="hover fs-3" data-bs-dismiss="modal"><IoClose /></div>
						</div>
						<div className="modal-body">
							{/* Selector de lenguaje */}
							<div className="row py-3">
								<div className="col-4">
									<div data-bs-dismiss="modal" onClick={() => handleLanguageChange('en')}>
										<p className={`fw-bold ${store.borde_hover}`}><span className="fi mx-1 fi-gb"></span>Inglés</p>
									</div>
								</div>
								<div className="col-4">
									<div data-bs-dismiss="modal" onClick={() => handleLanguageChange('zh')}>
										<p className={`fw-bold ${store.borde_hover}`}><span className="fi mx-1 fi-cn"></span>Chino</p>
									</div>
								</div>
								<div className="col-4">
									<div data-bs-dismiss="modal" onClick={() => handleLanguageChange('es')}>
										<p className={`fw-bold ${store.borde_hover}`}><span className="fi mx-1 fi-es"></span>Español</p>
									</div>
								</div>
							</div>
							<div className="row py-3">
								<div className="col-4">
									<div data-bs-dismiss="modal" onClick={() => handleLanguageChange('pt')}>
										<p className={`fw-bold ${store.borde_hover}`}><span className="fi mx-1 fi-pt"></span>Portugués</p>
									</div>
								</div>
								<div className="col-4">
									<div data-bs-dismiss="modal" onClick={() => handleLanguageChange('ru')}>
										<p className={`fw-bold ${store.borde_hover}`}><span className="fi mx-1 fi-ru"></span>Ruso</p>
									</div>
								</div>
								<div className="col-4">
									<div data-bs-dismiss="modal" onClick={() => handleLanguageChange('de')}>
										<p className={`fw-bold ${store.borde_hover}`}><span className="fi mx-1 fi-de"></span>Alemán</p>
									</div>
								</div>
							</div>
							<div className="row py-3">
								<div className="col-4">
									<div data-bs-dismiss="modal" onClick={() => handleLanguageChange('ar')}>
										<p className={`fw-bold ${store.borde_hover}`}><span className="fi mx-1 fi-sa"></span>Árabe</p>
									</div>
								</div>
								<div className="col-4">
									<div data-bs-dismiss="modal" onClick={() => handleLanguageChange('fr')}>
										<p className={`fw-bold ${store.borde_hover}`}><span className="fi mx-1 fi-fr"></span>Francés</p>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<nav >
				<div className="row my-2 mx-0">
					<div className="col-3 text-end d-flex justify-content-end">
						<img src={logo_negro} className={`img-fluid img ${store.fondo == "fondo-modo-oscuro" ? "d-block" : "d-none"}`} /><img src={logo_blanco} className={`img-fluid img ${store.fondo == "fondo-modo-oscuro" ? "d-none" : "d-block"}`} />
					</div>

					<div className="col-2 text-start fs-3 fw-bold  px-0 align-content-center"><span>GeekBank</span></div>
					{localStorage.getItem('token') === null ? (<div className="col-5 align-content-center  fw-bold text-center">
						<span className={store.borde_hover} onClick={() => {
							navigate("/example")
						}}></span>
					</div>) : (
						<>
							<div className="col-1 align-content-center  fw-bold text-center">
								<span className={store.borde_hover} onClick={() => {
									navigate("/example")
								}}>{t('Movements')} </span>{/* Seccion movimientos */}
							</div>
							<div className="col-1 align-content-center  fw-bold text-center">
								<span className={store.borde_hover} onClick={() => {
									navigate("/example")
								}}>{t('Transfers')}</span> {/* Seccion transferencias */}
							</div>
							<div className="col-1 align-content-center  fw-bold text-center">
								<span className={store.borde_hover} onClick={() => {
									navigate("/example")
								}}>{t('GEEK Store')}</span>{/* Seccion tienda */}
							</div>
							<div className="col-1 align-content-center  fw-bold text-center">
								<span className={store.borde_hover} onClick={() => {
									navigate("/example")
								}}>{t('Exch/Currency')}</span> {/* Seccion divisas */}
							</div>
							<div className="col-1 align-content-center  fw-bold text-center">
								<span className={store.borde_hover} onClick={() => {
									navigate("/example")
								}}>{t('Investments')}</span> {/* Seccion divisas */}
							</div>
						</>)}

					{/*------------------------------ eleccion de idiomas ------------ */}
					<div className="col-1 text-end align-content-center">
						<div type="div" className="rounded-circle enlace" data-bs-toggle="modal" data-bs-target="#lenguajes"> {/* Ejecuta el modal */}
							<GiWorld className="simbolo-idioma hover" />
						</div>
					</div>
					{/*------------------------------ eleccion de idiomas ------------ */}
					{/*------------------------------ modo oscuro/ modo claro ------------ */}
					<div className="col-1 align-content-center  fw-bold text-center ">
						<div className={btn === true ? "dark-mode rounded-pill fondo-claro borde-brillante" : "dark-mode rounded-pill fondo-oscuro borde-brillante"}>
							<div className={btn === true ? "text-warning circle rounded-circle bg-white w-50 border  fw-bold enlace position-relative d-flex justify-content-center active" : "circle rounded-circle w-50 border  bg-black  fw-bold enlace position-relative d-flex justify-content-center"} onClick={() => {
								btn === true ? setbtn(false) : setbtn(true);
							}}>
								<div className="icono hover">
									{btn === false ? <FaMoon /> : <MdWbSunny />}
								</div>
							</div>
						</div>
					</div>
					{/*------------------------------ modo oscuro/ modo claro ------------ */}
				</div>
			</nav >
		</div >
	);
}