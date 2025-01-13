import React, { useContext, useEffect, useRef, useState } from "react";
import { Context } from "../../store/appContext.js";
import { useTranslation } from "react-i18next";// importacion de traducción
import { useNavigate } from "react-router-dom";

export const Login = () => {
    const { t } = useTranslation();

    const { store, actions } = useContext(Context);
    // estados para controlar los valores puestos por el usuario
    const [name, SetName] = useState("");
    const [email, SetEmail] = useState("");
    const [password, SetPassword] = useState("");

    // ejecuta el contenedor si el usuario se ha olvidado el password de su cuenta
    const [userForgotPassword, SetuserForgotPassword] = useState(false)

    // estado para controlar si el usuario solicito el codigo para cambiar su password
    const [code, SetCode] = useState(false);

    // estado que guarda el valor del email para recuperar la password
    const [forgotMail, SetForgotMail] = useState("");

    // tiempo que tiene que pasar para solicitar de nuevo el codigo
    const [timeCode, SetTimeCode] = useState(30);

    const HandleForgotMail = (e) => {
        SetForgotMail(e.target.value.toLowerCase())
    }

    const CountRef = useRef(null)
    const buttomCode = useRef(null)
    const InputCode = useRef(null)

    const Count = () => {
        //creamos el intervalo del contador
        clearInterval(CountRef.current);

        buttomCode.current.disabled = true;
        CountRef.current = setInterval(() => {
            SetTimeCode((prevContador) => prevContador - 1);
        }, 1000)
    };

    useEffect(() => {
        if (timeCode === 0) {
            clearInterval(CountRef.current)
            SetTimeCode(60)
            SetCode(false)
            buttomCode.current.disabled = false;
        }
    }, [timeCode])

    const HandleCode = (e) => {
        if (/^\d+$/.test(e.target.value) === false) {
            InputCode.current.value = InputCode.current.value.slice(0, -1)
        }
    }

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

    const FindUser = async () => {
        try {
            inputName.current.value = "";
            inputPassword.current.value = "";
            inputMail.current.value = "";
            const response = await fetch(
                process.env.BACKEND_URL + "/api/User/Login",
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
            console.log(data)
            // Accedemos al token desde la respuesta
            const token = data.token;

            localStorage.setItem('token', token)


            return "success";
        } catch (error) {
            console.error("Error al agregar usuario:", error);
        }
    }

    const navigate = useNavigate("");
    return (
        <div className="login">
            <form action="#" className={`d-flex flex-column align-content-center text-center justify-content-center ${store.fondo}`}>
                <h1>{t(userForgotPassword === false ? 'Login' : 'Recovery')}</h1>
                {/* hace la transicion mas suave  */}
                <div className={userForgotPassword ? "transicion-recuperar-password " : "transicion-Iniciar-Sesion "}>
                    {/*muestra dependiendo del estado userForgotPassword el contenedor de iniciar sesion o password olvidada*/}
                    <div className="d-flex flex-column text-center container">
                        {userForgotPassword === false ? (
                            <>
                                {/* cotenedor inciar sesion */}
                                <label className="my-1 fw-bold">{t('Name')}</label>
                                <input className=" mx-3 text-center py-1 rounded-pill input" type="text" onChange={HandleName} maxLength="40" ref={inputName} />
                                <label className="my-1 fw-bold">{t('Email')}</label>
                                <input className=" mx-3 text-center py-1 rounded-pill input" type="email" onChange={HandleEmail} ref={inputMail} />
                                <label className="my-1 fw-bold">{t('Password')}</label>
                                <input className=" mx-3 text-center py-1 rounded-pill input" type="password" onChange={HandlePassword} ref={inputPassword} />
                                <span className={`text-end mx-3 ${store.borde_hover}`} onClick={() => { SetuserForgotPassword(true) }}>{t('Forgot')}</span>
                                <div className="text-center">
                                    <button type="button" className={`btn btn-light mt-3 w-50 rounded-pill ${store.borde}`} onClick={() => {
                                        // FindUser();
                                        localStorage.setItem('token', "ejemplo")
                                        navigate("/home")
                                    }}>{t('Login')}</button>
                                </div>
                            </>
                        ) : (
                            <>
                                {/* contenedor password olvidada */}
                                <div className="text-center my-2">
                                    <span className="fw-bold">{t('Forgot')}</span>
                                    <p className="mx-3 text-center py-1 rounded-3 text-center">{t('Recovery2')}</p>
                                </div>
                                <label className="my-1 fw-bold">{t('Email')}</label>
                                <input className=" mx-3 text-center py-1 rounded-pill input" type="email" onChange={HandleForgotMail} />
                                <div className="text-center row mx-1 my-2">
                                    <div className="col-6 my-3 text-start">
                                        <button type="button" className="rounded-pill btn btn-primary w-100 fw-bold" ref={buttomCode} onClick={() => {
                                            SetCode(true)
                                            Count()
                                        }}>{code ?
                                            `( ${timeCode} ) s`
                                            : t('SendCode')}</button>
                                    </div>
                                    <div className="col-3 my-3 text-center">
                                        <input className="text-center py-1 rounded-pill input w-100 fw-bold input-code" type="text" onChange={HandleCode} maxLength={6} ref={InputCode} placeholder="******" />
                                        <label className="fw-bold">{t('Code')}</label>
                                    </div>
                                    <div className="col-3">
                                        <div className="col-12 text-center">
                                            <button type="button" className={`btn mt-3 w-100 rounded-pill ${store.borde} ${store.texto} `} onClick={() => {
                                                console.log(timeCode);
                                            }}>{t('Check')}</button>
                                        </div>
                                    </div>
                                </div>
                                <span className={`mx-3 ${store.borde_hover}`} onClick={() => {
                                    SetuserForgotPassword(false);
                                }}>{t('Return')}</span>
                            </>
                        )}
                    </div>
                </div>
            </form>
        </div>
    )
};

export default Login
