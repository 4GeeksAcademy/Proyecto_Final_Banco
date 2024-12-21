import React, { useState } from "react";
import logo_negro from "../../img/logo-negro.png";
import logo_blanco from "../../img/logo-blanco.png";
import "../../styles/navbar.css";
import { FaMoon } from "react-icons/fa";
import { MdWbSunny } from "react-icons/md";
import { GiWorld } from "react-icons/gi";


export const Navbar = () => {

	const [ejemplo, setejemplo] = useState(false) // esto es para test

	const [openSelect, setOpenSelect] = useState(false)
	return (
		<>
			<div className="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">{/* Modal selector de idiomas */}
				<div className="modal-dialog">
					<div className="modal-content bg-dark rounded-3">
						<div className="modal-header">
							<h1 className="modal-title fs-5 text-white" id="exampleModalLabel">Lenguajes</h1>
							<button type="button" className="btn-close rounded-circle" data-bs-dismiss="modal" aria-label="Close"></button>
						</div>
						<div className="modal-body">
							<div className="row py-3">
								<div className="col-4"> <p className="fw-bold text-white enlace"><span className="fi mx-1 fi-gb"></span>  Inglés</p></div>
								<div className="col-4"> <p className="fw-bold text-white enlace"><span className="fi mx-1 fi-cn"></span>  Chino</p></div>
								<div className="col-4"> <p className="fw-bold text-white enlace"><span className="fi mx-1 fi-es"></span>  Español</p></div>
							</div>
							<div className="row py-3">
								<div className="col-4"> <p className="fw-bold text-white enlace"><span className="fi mx-1 fi-pt"></span>  Portugués</p></div>
								<div className="col-4"><p className="fw-bold text-white enlace"><span className="fi mx-1 fi-ru"></span>  Ruso</p></div>
								<div className="col-4"><p className="fw-bold text-white enlace"><span className="fi mx-1 fi-de"></span>  Alemán</p></div>
							</div>
							<div className="row py-3">
								<div className="col-4"> <p className="fw-bold text-white enlace"><span className="fi mx-1 fi-sa"></span>  Árabe</p></div>
								<div className="col-4"> <p className="fw-bold text-white enlace"><span className="fi mx-1 fi-fr"></span>  Francés</p></div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<nav >
				<div className="row my-2">
					<div className="col-3 text-end fs-3 fw-bold text-white px-0"><img src={ejemplo === false ? logo_negro : logo_blanco} className="img-fluid img" /></div> {/* Simbolo */}
					<div className="col-2 text-start fs-3 fw-bold text-white px-0 align-content-center"><span>GeekBank</span></div>
					<div className="col-1 align-content-center text-white fw-bold text-center">
						<span className="enlace-claro">Movimientos</span> {/* Seccion movimientos */}
					</div>
					<div className="col-1 align-content-center text-white fw-bold text-center">
						<span className="enlace-claro">Transferencias</span> {/* Seccion transferencias */}
					</div>
					<div className="col-1 align-content-center text-white fw-bold text-center">
						<span className="enlace-claro">Tienda Geek</span>{/* Seccion tienda */}
					</div>
					<div className="col-1 align-content-center text-white fw-bold text-center">
						<span className="enlace-claro">Cambio/Divisas</span> {/* Seccion divisas */}
					</div>
					<div className="col-1 align-content-center text-white fw-bold text-center">
						<span className="enlace-claro">Inversiones</span> {/* Seccion divisas */}
					</div>

					{/*------------------------------ eleccion de idiomas ------------ */}
					<div className="col-1 text-end align-content-center">
						<div type="div" className="rounded-circle enlace" data-bs-toggle="modal" data-bs-target="#exampleModal"> {/* Ejecuta el modal */}
							<GiWorld className="text-white simbolo-idioma" />
						</div>
					</div>
					{/*------------------------------ eleccion de idiomas ------------ */}
					{/*------------------------------ modo oscuro/ modo claro ------------ */}
					<div className="col-1 align-content-center text-white fw-bold text-center ">
						<div className={ejemplo === true ? "dark-mode rounded-pill fondo-claro borde-brillante" : "dark-mode rounded-pill fondo-oscuro borde-brillante"}>
							<div className={ejemplo === true ? "text-warning circle rounded-circle bg-white w-50 border border-warning fw-bold enlace position-relative d-flex justify-content-center active" : "circle rounded-circle w-50 border border-white bg-black text-white fw-bold enlace position-relative d-flex justify-content-center"} onClick={() => {
								ejemplo === true ? setejemplo(false) : setejemplo(true);
							}}>
								<div className="icono">
									{ejemplo === false ? <FaMoon /> : <MdWbSunny />}
								</div>
							</div>
						</div>
					</div>
					{/*------------------------------ modo oscuro/ modo claro ------------ */}
				</div>
			</nav></>
	);
};
