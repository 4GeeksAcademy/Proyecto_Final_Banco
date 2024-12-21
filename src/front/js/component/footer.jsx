import React, { Component } from "react";
import "../../styles/footer.css";

export const Footer = () => {


	return (
		<footer className="footer mt-auto py-3 bg-black border-top border-white">
		<div className="row px-3 m-0">
			<div className="col-2 text-start d-flex flex-column">
			<h6 className="subtitulo text-white">Informacion de contacto</h6>
			<span className="enlace-claro text-white">Contacto</span>
			<span className="enlace-claro text-white">Chat</span>
			</div>
			<div className="col-2 text-start d-flex flex-column">
			<h6 className="subtitulo text-white">Enlaces legales</h6>
			<span className="enlace-claro text-white">Politica de privacidad</span>
			<span className="enlace-claro text-white">Termino de condiciones</span>
			<span className="enlace-claro text-white">aviso legal</span>
			</div>
			<div className="col-2 text-start d-flex flex-column">
			<h6 className="subtitulo text-white">Enlaces a recursos</h6>
			<span className="enlace-claro text-white">Tarifas / Comisiones</span>
			<span className="enlace-claro text-white">Educacion</span>
			</div>
			<div className="col-2 text-start d-flex flex-column">
			<h6 className="subtitulo text-white">Seguridad</h6>
			<span className="enlace-claro text-white">Consejos</span>
			<span className="enlace-claro text-white">Metodos de Seguridad</span>
			<span className="enlace-claro text-white">Tarjeta de cordenadas</span>
			</div>
			<div className="col-2 text-start d-flex flex-column">
			<h6 className="subtitulo text-white">Productos y Servicios</h6>
			<span className="enlace-claro text-white">Store</span>
			<span className="enlace-claro text-white">Seguro</span>
			<span className="enlace-claro text-white">Prestamo</span>
			</div>
			<div className="col-2 text-start d-flex flex-column">
			<h6 className="subtitulo text-white">Certificaciones</h6>
			<span className="enlace-claro text-white">Titulos certificados</span>
			<span className="enlace-claro text-white">Titulos de seguridad</span>
			</div>
		</div>
	</footer>
	)
};
