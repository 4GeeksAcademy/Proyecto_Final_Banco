const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      texto: "text-white",
      fondo: "fondo-modo-oscuro",
      borde: "border border-white",
      borde_hover: "enlace-claro",
      hidden: false,
      codeSent: false,
      email: "",
      code: "",
      token: null,
      user: "",
      cliente: "",
      cuentas: "",
      tarjetaCoord: {},
      tarjetaCoordComp:{},
      transacciones: [],
      listaNotificaciones: [],
      simbolos: [],
      grafica: [],
      chartData: [], // Graficas
      stockData: null, // Datos de mercado
      notificacionesHidden: false,
    },
    actions: {
      ObtenerSimbolos: async () => {

        try {
          const response = await fetch(`https://finnhub.io/api/v1/stock/symbol?exchange=US&token=${process.env.FINNHUB_API_KEY}`);
          if (!response.ok) throw new Error('Error fetching data');

          const data = await response.json();

          const resultado = await data.map((item) => {
            return {
              moneda: item.currency,
              simbolo: item.symbol,   // Agregamos el símbolo
              nombre: item.description  // Agregamos la descripción
            };
          });

          setStore({ ...getStore(), simbolos: resultado });
        } catch (error) {
          console.error('Error al obtener datos del backend:', error);
        }
      },
      ActualizarGrafica: (datos) => {
        setStore({ ...getStore(), grafica: datos });
      },

      CambiarIncognito: (estado) => {
        setStore({ ...getStore(), hidden: estado });
      },
      CambiarNotificaciones: () => {
        setStore({ ...getStore(), notificacionesHidden: !getStore().notificacionesHidden });
      },
      Scroll: () => {
        const navbar = document.getElementById("navbar"); // Seleccionamos el elemento por ID
        if (navbar) {
          navbar.scrollIntoView({
            behavior: "smooth", // Desplazamiento suave
            block: "start", // Alinear al inicio del elemento
          });
        }
      },
      CambiarModo: (estado) => {
        if (estado === true) {
          setStore({
            texto: "text-dark",
            fondo: "fondo-modo-claro",
            borde: "border border-secondary",
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

      loginUser: async (name, email, password) => {
        const store = getStore();
        const actions = getActions();


        try {
          const response = await fetch(process.env.BACKEND_URL + "/api/User/Login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password }),
          });

          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.mensaje || "Error en el inicio de sesión");
          }

          const data = await response.json();
          // Guardamos el token en el localStorage
          localStorage.setItem("token", data.token);
          localStorage.setItem("name", data.user.name);
          localStorage.setItem("userId", data.user.id);
          // actions.fetchUserDetails(data.user.id)

          // Actualizamos el store con el token y los datos del usuario
          setStore({
            ...store,
            token: data.token,
            user: data.user, // Ajustar según lo que devuelva tu backend

          });
          console.log("Login exitoso. Token guardado en localStorage.", store.user, store.usuario);
        } catch (error) {
          console.error("Error en loginUser:", error.message);
          throw error; // Lanzamos el error para que HandleLogin lo maneje
        }
      },

      registerUser: (name, email, password) => {
        const actions = getActions();
        console.log("desde flux", name, email, password);

        return fetch(process.env.BACKEND_URL + "/api/User/Register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            password: password,
            email: email,
            name: name,
            is_active: true,
          }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Error en el registro");
            }
            return response.json(); // Parseamos la respuesta JSON
          })
          .then((data) => {
            localStorage.setItem("token", data.token);
            localStorage.setItem("name", data.user.name);
            localStorage.setItem("userId", data.user.id);
            // actions.fetchUserDetails(data.user.id)
            return "success";
          })
          .catch((error) => {
            console.error("Error al registrar usuario:", error);
          });
      },

      fetchUserDetails: (id) => {
        const store = getStore();
        fetch(`${process.env.BACKEND_URL}/api/User/${id}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((response) => {

            if (!response.ok) {
              throw new Error(`Error: ${response.status} - ${response.statusText}`);
            }
            return response.json(); // Convertimos la respuesta a JSON
          })

          .then((data) => {

            // Guardamos los datos del usuario en el store bajo la propiedad "usuario"
            setStore({ ...store, cliente: data.cliente });
            setStore({ ...store, cuentas: data.cuentas });
            setStore({ ...store, user: data.user });
            setStore({ ...store, listaNotificaciones: data.notificaciones });
            setStore({ ...store, tarjetaCoord: data.tarjeta_coordenadas });
            setStore({ ...store, transacciones: data.cuentas.transacciones });

            console.log("user", store.user, "cliente", store.cliente, "cuentas", store.cuentas, "Notificaciones", store.listaNotificaciones, "transacciones", store.transacciones);
          })
          .catch((error) => {
            // Manejamos cualquier error que ocurra durante el fetch
            console.error("Hubo un problema al obtener los detalles del usuario:", error);
          });
      },

      updateClienteProfile: (id, perfil) => {
        const store = getStore();

        fetch(`${process.env.BACKEND_URL}/api/User/${id}/Perfil`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(perfil)
        })
          .then(async (response) => {
            if (response.ok) {
              const data = await response.json(); // Procesar la respuesta como JSON
              setStore({ ...store, cliente: data.cliente });
              console.log("Perfil actualizado:", data);
            } else {
              const errorData = await response.json(); // Procesar el error como JSON
              console.error("Error al actualizar el perfil:", errorData);
            }
          })
          .catch((error) => {
            console.error("Error de red o del servidor:", error);
          });
      },

      sendCoordinatesCard: (userId) => {
        const store = getStore();

        fetch(`${process.env.BACKEND_URL}/api/send-coordinates-card/${userId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Error al enviar la tarjeta de coordenadas");
            }
            return response.json();
          })
          .then((data) => {
            // Si la solicitud es exitosa, actualiza el store
            setStore({
              ...store, coordinatesCardSent: true,
            });
            console.log("Tarjeta de coordenadas enviada exitosamente:", data);
          })
          .catch((error) => {
            // Si hay un error, actualiza el store con el mensaje de error
            setStore({
              ...store, coordinatesCardSent: false,
            });
            console.error("Error al enviar la tarjeta de coordenadas:", error);
          });
      },

      realizarTransferencia: async (cuenta_origen_id, numero_cuenta_destino, nombre_destino, apellidos_destino, monto, descripcion) => {

        try {
            const response = await fetch(`${process.env.BACKEND_URL}/api/transaccion/transferencia`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    // Authorization: `Bearer ${localStorage.getItem("token")}`, // Si usas autenticación
                },
                body: JSON.stringify({
                    cuenta_origen_id,
                    numero_cuenta_destino, // Número de cuenta destino
                    nombre_destino,       // Nombre del cliente destino
                    apellidos_destino,    // Apellidos del cliente destino
                    monto,
                    descripcion,
                }),
            });
    
            const data = await response.json();
            console.log(data)
            if (!response.ok) {
                throw new Error(data.error || "Error al realizar la transferencia");
            }
    
            // Actualizar el store con los nuevos saldos
            // const store = getStore();
            // const updatedCuentas = store.cuentas.map((cuenta) => {
            //     if (cuenta.id === cuenta_origen_id) {
            //         return { ...cuenta, saldo: data.saldo_origen };
            //     }
            //     if (cuenta.numero_cuenta === numero_cuenta_destino) {
            //         return { ...cuenta, saldo: data.saldo_destino };
            //     }
            //     return cuenta;
            // });
    
            // setStore({
            //     ...store,
            //     cuentas: updatedCuentas,
            // });
    
            return data; // Devuelve los datos de la transferencia
        } catch (error) {
            console.error("Error al realizar la transferencia:", error);
            throw error; // Lanza el error para manejarlo en el componente
        }
    },

      marcarNotificacionComoLeida: async (notificacionId) => {
        try {
          const response = await fetch(`${process.env.BACKEND_URL}/api/notificaciones/${notificacionId}/marcar-leida`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
          });

          if (!response.ok) {
            throw new Error("Error al marcar la notificación como leída");
          }

          const data = await response.json();
          return data; // Devuelve la notificación actualizada

        } catch (error) {
          console.error("Error:", error);
          throw error;
        }
      },
      setNotificaciones: (listaNotificaciones) => {
        const store = getStore();
        setStore({ ...store, listaNotificaciones });
      },

      sendCode: (email) => {
        const store = getStore();
        const actions = getActions();
        setStore({ email }); 

        fetch(process.env.BACKEND_URL + "/api/send-code", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: store.email }), 
        })
          .then((response) => response.json())
          .then((response) => console.log(response))
          .then((data) => {
            if (response.ok) { 
              setStore(console.log(Enviado));
            } else {
              alert(data.error);
            }
          });
      },

      verifyCode: (email, code) => {
        const store = getStore();
        setStore({ email });
        setStore({ code });

        fetch(process.env.BACKEND_URL + "/api/verify-code", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: store.email, code: store.code }),
        })
          .then((response) => response.json())
          .then((response) => console.log(response))
          .then((data) => {
            if (response.ok) {
              alert("Código verificado. Ahora puedes cambiar tu contraseña.");
            } else {
              alert(data.error);
            }
          });
      },

      sendCoordinatesCode: (email) => {
        console.log(email)
        const store = getStore();

        fetch(`${process.env.BACKEND_URL}/api/send-coordinates-code`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email: email }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Error al enviar el código");
            }
            return response.json();
          })
          .then((data) => {
            // setStore({
            //   ...store, coordinatesCodeSent: true,
            // });
            console.log("Código enviado:", data);
          })
          .catch((error) => {
            // setStore({
            //   ...store, coordinatesCodeSent: false,
            // });
            console.error("Error:", error);
          });
      },

      // Acción para verificar el código de la tarjeta de coordenadas

      verifyCoordinatesCode: (email, code) => {
        const store = getStore();
    
        return fetch(`${process.env.BACKEND_URL}/api/verify-coordinates-code`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: email, code: code }),
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Código inválido o expirado");
            }
            return response.json();
        })
        .then((data) => {
            setStore({ ...store, tarjetaCoord: data.tarjeta_coordenadas });
            return data; // 🔹 Devolvemos los datos
        })
        .catch((error) => {
            console.error("Error:", error);
            return null; // 🔹 Devolvemos null en caso de error
        });
    },
    

      fetchGraficasData: async () => {
        try {
          const response = await fetch(process.env.BACKEND_URL + "/api/data");
          if (!response.ok) throw new Error('Error fetching data');

          const data = await response.json();

          // Formatear los datos
          const formattedData = data.map((item) => ({
            time: item.date,
            value: item.price,
          }));

          // Guardar los datos en el store
          setStore({ chartData: formattedData });
        } catch (error) {
          console.error('Error al obtener datos del backend:', error);
        }
      },

      fetchStockData: async (symbol) => {
        try {
          const response = await fetch(`${process.env.s}/api/stock/${symbol}`);
          if (!response.ok) throw new Error('Error fetching stock data');
          const data = await response.json();

          // Guardar datos en el store
          setStore({ stockData: data });
        } catch (error) {
          console.error('Error al obtener datos de las acciones:', error);
        }
      },
    },
  };
};



export default getState;
