import React, { useContext, useRef, useState } from "react";
import { Context } from "../../store/appContext.js";
import { useTranslation } from "react-i18next";// importacion de traducción
import { useNavigate } from "react-router-dom";

export const Register = () => {
    const { t } = useTranslation();
    //estados para controlar los valores puestos por el usuario
    const [name, SetName] = useState("");
    const [email, SetEmail] = useState("");
    const [password, SetPassword] = useState("");
    const navigate = useNavigate(null);

    const { store, actions } = useContext(Context);

    //handles para cambiar los valores puestos por el usuario

    const HandleName = (e) => {
        SetName(e.target.value)
    }
    const HandleEmail = (e) => {
        SetEmail(e.target.value.toLowerCase())
    }
    const HandlePassword = (e) => {
        SetPassword(e.target.value)
    }

    const inputName = useRef(null)
    const inputPassword = useRef(null)
    const inputMail = useRef(null)

    const AddUser = async () => {
        try {
            inputName.current.value = "";
            inputPassword.current.value = "";
            inputMail.current.value = "";
            const response = await fetch(
                process.env.BACKEND_URL + "/api/User/Register",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        "password": password,
                        "email": email,
                        "name": name,
                        "is_active": true
                    }),
                }
            );
            if (!response.ok) {
                throw new Error(`Error: :( )`);
            }

            const data = await response.json(); // Parseamos la respuesta JSON

            // Accedemos al token desde la respuesta
            const token = data.token;

            localStorage.setItem('token', token)


            return "success";
        } catch (error) {
            console.error("Error al agregar usuario:", error);
        }
    }

    return (
        <div className="register">
            <form action="#" className={`d-flex flex-column align-content-center text-center justify-content-center ${store.fondo}`}>
                <h1>{t('Create')}</h1>
                <div className="d-flex flex-column text-center container mb-3">
                    <label className="my-1 fw-bold">{t('Name')}</label>
                    <input className=" mx-3 text-center py-1 rounded-pill input" type="text" onChange={HandleName} maxLength="40" ref={inputName} />
                    <label className="my-1 fw-bold">{t('Email')}</label>
                    <input className=" mx-3 text-center py-1 rounded-pill input" type="email" onChange={HandleEmail} ref={inputMail} />
                    <label className="my-1 fw-bold">{t('Password')}</label>
                    <input className=" mx-3 text-center py-1 rounded-pill input" type="password" onChange={HandlePassword} ref={inputPassword} />
                </div>

                <div className="text-center">
                    <button className={`btn btn-light mt-3 w-50 rounded-pill  ${store.borde}`} onClick={async () => {
                        const user = await AddUser();
                        user === "success" ? navigate("/home") : ""
                    }}>{t('Ready')}</button>
                </div>
            </form>
        </div>
    )
};

export default Register
