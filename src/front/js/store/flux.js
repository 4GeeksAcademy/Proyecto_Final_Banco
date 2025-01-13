const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      texto: "text-dark",
      fondo: "fondo-modo-oscuro",
      borde: "border border-danger",
      borde_hover: "enlace-oscuro",
      hidden: false,
    },
    actions: {
      CambiarIncognito: (estado) => {
        setStore({ ...getStore(), hidden: estado });
      },
      CambiarModo: (estado) => {
        if (estado === true) {
          setStore({
            texto: "text-dark",
            fondo: "fondo-modo-claro",
            borde: "border border-dark",
            borde_hover: "enlace-oscuro",
          });
          document.body.classList.remove("fondo-modo-oscuro");
          document.body.classList.add("fondo-modo-claro");
        } else {
          setStore({
            texto: "text-white",
            fondo: "fondo-modo-oscuro",
            borde: "border border-white",
            borde_hover: "enlace-claro",
          });
          document.body.classList.remove("fondo-modo-claro");
          document.body.classList.add("fondo-modo-oscuro");
        }
      },

      ConseguirToken: () => {
        try {
        } catch (error) {
          console.log(error);
        }
      },
      // Funcion Ejemplo
      //   changeColor: (index, color) => {
      //     //get the store
      //     const store = getStore();
      //     //we have to loop the entire demo array to look for the respective index
      //     //and change its color
      //     const demo = store.demo.map((elm, i) => {
      //       if (i === index) elm.background = color;
      //       return elm;
      //     });
      //     //reset the global store
      //     setStore({ demo: demo });
      //   },
    },
  };
};

export default getState;
