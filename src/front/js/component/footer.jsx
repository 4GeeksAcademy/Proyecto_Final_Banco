import React, { Component, useContext } from "react";
import "../../styles/footer.css";
import { useTranslation } from "react-i18next";// importacion de traducción
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";
import { FaFacebookSquare } from "react-icons/fa";
import { FaSquareXTwitter } from "react-icons/fa6";
import { FaSquareInstagram } from "react-icons/fa6";
import { FaLinkedin } from "react-icons/fa";
import { IoLogoYoutube } from "react-icons/io5";
import { FaSquareWhatsapp } from "react-icons/fa6";

export const Footer = () => {

	const { t } = useTranslation();
	const { store, actions } = useContext(Context);
	const navigate = useNavigate(null);

	return (
		<footer className={`footer mt-auto py-3 border-end-0 border-start-0 ${store.borde} ${store.texto} ${store.fondo}`}> {/* modo oscuro y claro */}
			<div className="row px-3 m-0"> {/* Links */}
				<div className="col-2 flex-column animation">
					<h6 className="subtitulo d-flex ">{t('Contact information')}</h6>
					<span className={`d-flex ${store.borde_hover}`} onClick={() => {
						navigate("/example")
					}}>{t('Contact')}</span>
					<span className={`d-flex ${store.borde_hover}`} onClick={() => {
						navigate("/example")
					}}>{t('Chat')}</span>
				</div>
				<div className="col-2 flex-column animation">
					<h6 className="subtitulo d-flex ">{t('Legal links')}</h6>
					<span className={`d-flex ${store.borde_hover}`} onClick={() => {
						navigate("/example")
					}}>{t('Privacy Policy')}</span>
					<span className={`d-flex ${store.borde_hover}`} onClick={() => {
						navigate("/example")
					}}>{t('Term of conditions')}</span>
					<span className={`d-flex ${store.borde_hover}`} onClick={() => {
						navigate("/example")
					}}>{t('Legal notice')}</span>
				</div>
				<div className="col-2 flex-column animation">
					<h6 className="subtitulo d-flex ">{t('Links to resources')}</h6>
					<span className={`d-flex ${store.borde_hover}`} onClick={() => {
						navigate("/example")
					}}>{t('Rates and commissions')}</span>
					<span className={`d-flex ${store.borde_hover}`} onClick={() => {
						navigate("/example")
					}}>{t('Education')}</span>
				</div>
				<div className="col-2 flex-column animation">
					<h6 className="subtitulo d-flex ">{t('Security')}</h6>
					<span className={`d-flex ${store.borde_hover}`} onClick={() => {
						navigate("/example")
					}}>{t('Tips')}</span>
					<span className={`d-flex ${store.borde_hover}`} onClick={() => {
						navigate("/example")
					}}>{t('Security methods')}</span>
					<span className={`d-flex ${store.borde_hover}`} onClick={() => {
						navigate("/example")
					}}>{t('Coordinate card')}</span>
				</div>
				<div className="col-2 flex-column animation">
					<h6 className="subtitulo d-flex ">{t('Products and services')}</h6>
					<span className={`d-flex ${store.borde_hover}`} onClick={() => {
						navigate("/example")
					}}>{t('Shop')}</span>
					<span className={`d-flex ${store.borde_hover}`} onClick={() => {
						navigate("/example")
					}}>{t('Insurance')}</span>
					<span className={`d-flex ${store.borde_hover}`} onClick={() => {
						navigate("/example")
					}}>{t('Loans')}</span>
				</div>
				<div className="col-2 flex-column animation">
					<h6 className="subtitulo d-flex ">{t('Certifications')}</h6>
					<span className={`d-flex ${store.borde_hover}`} onClick={() => {
						navigate("/example")
					}}>{t('Certified titles')}</span>
					<span className={`d-flex ${store.borde_hover}`} onClick={() => {
						navigate("/example")
					}}>{t('Security titles')}</span>
				</div>
			</div>
			<div className="row mx-0">
				<div className="col-12 justify-content-end px-3 d-flex">

					<div className="icono_redes"><FaFacebookSquare /></div>
					<div className="icono_redes"><FaSquareXTwitter /></div>
					<div className="icono_redes"><FaSquareInstagram /></div>
					<div className="icono_redes"><FaLinkedin /></div>
					<div className="icono_redes"><IoLogoYoutube /></div>
					<div className="icono_redes"><FaSquareWhatsapp /></div>


				</div>
			</div> {/* Redes sociales */}
		</footer>
	)
};