import React, { useContext } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";

export const Home = () => {
  const { store, actions } = useContext(Context);

  return (
    <div className="row">
      <div className="col-12 text-center">
        <h1 className={`hover text-danger fw-bold fs-1 ejemplo ${store.borde_hover}`}>
          Home :) 🍕😉🙋‍♂️🫰💵
        </h1>
      </div>
    </div>
  );
};
