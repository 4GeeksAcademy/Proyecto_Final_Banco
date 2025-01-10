const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      texto: "text-dark",
      fondo: "fondo-modo-oscuro",
      borde: "border border-danger",
      borde_hover: "enlace-oscuro",
    },
    actions: {
      CambiarModo: (estado) => {
        if (estado === true) {
          setStore({
            texto: "text-dark",
            fondo: "fondo-modo-claro",
            borde: "border border-dark",
            borde_hover: "enlace-oscuro",
          });
          document.body.style.backgroundColor = "white";
        } else {
          setStore({
            texto: "text-white",
            fondo: "fondo-modo-oscuro",
            borde: "border border-white",
            borde_hover: "enlace-claro",
          });
          document.body.style.backgroundColor = "black";
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
