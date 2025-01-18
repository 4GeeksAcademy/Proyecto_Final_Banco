import React, { useContext } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ScrollToTop from "./component/scrollToTop";
import { BackendURL } from "./component/backendURL";

import { Landingpage } from "./pages/landingpage.js";
import { Login } from "./pages/login";
import { Home } from "./pages/home";
import { Politicas } from "./pages/politicas";
import { Terminos } from "./pages/terminos";
import { Aviso } from "./pages/aviso";
import { Tarifas } from "./pages/tarifas";
import { Educacion } from "./pages/educacion.js";

import { Not_found } from "./pages/not_found.js";

import injectContext, { Context } from "./store/appContext";
import { Navbar } from "./component/navbar.jsx";
import { Footer } from "./component/footer.jsx";
import { Perfil } from "./pages/perfil.js";

//create your first component
const Layout = () => {
  //the basename is used when your project is published in a subdirectory and not in the root of the domain
  // you can set the basename on the .env file located at the root of this project, E.g: BASENAME=/react-hello-webapp/
  const basename = process.env.BASENAME || "";
  const { store, actions } = useContext(Context);

  if (!process.env.BACKEND_URL || process.env.BACKEND_URL == "")
    return <BackendURL />;

  return (
    // app-container, content -> clases para que el footer siempre se encuentre debajo del todo
    <div className={`app-container ${store.fondo} ${store.texto}`}>
      <BrowserRouter basename={basename}>
        <ScrollToTop>
          <Navbar />
          <div className="content">
            <Routes>
              <Route element={<Landingpage />} path="/" />
              <Route element={<Login />} path="/login" />
              <Route element={<Home />} path="/home" />
              <Route element={<Politicas />} path="/politicas" />
              <Route element={<Terminos />} path="/terminos" />
              <Route element={<Aviso />} path="/aviso" />
              <Route element={<Tarifas />} path="/tarifas" />
              <Route element={<Educacion />} path="/educacion" />
              <Route element={<Perfil />} path="/perfil" />
              <Route element={<Not_found />} path="*" />
            </Routes>
          </div>
          <Footer />
        </ScrollToTop>
      </BrowserRouter>
    </div>
  );
};

export default injectContext(Layout);
