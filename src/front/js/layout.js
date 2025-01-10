import React, { useContext } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ScrollToTop from "./component/scrollToTop";
import { BackendURL } from "./component/backendURL";

import { Login } from "./pages/login";
import { Home } from "./pages/home";
import injectContext, { Context } from "./store/appContext";

import { Navbar } from "./component/navbar.jsx";
import { Footer } from "./component/footer.jsx";

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
              <Route element={<Login />} path="/" />
              <Route element={<Home />} path="/home" />
              <Route element={<h1>Not found!</h1>} />
            </Routes>
          </div>
          <Footer />
        </ScrollToTop>
      </BrowserRouter>
    </div>
  );
};

export default injectContext(Layout);
