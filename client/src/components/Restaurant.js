import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import PizzaForm from "./PizzaForm";

function Home() {
  const [{ data: restaurant, error, status }, setRestaurant] = useState({
    data: null,
    error: null,
    status: "pending",
  });
  const { id } = useParams();

  useEffect(() => {
    fetch(`/restaurants/${id}`).then((r) => {
      if (r.ok) {
        r.json().then((restaurant) =>
          setRestaurant({ data: restaurant, error: null, status: "resolved" })
        );
      } else {
        r.json().then((err) =>
          setRestaurant({ data: null, error: err.error, status: "rejected" })
        );
      }
    });
  }, [id]);

  function handleAddPizza(newPizza) {
    setRestaurant({
      data: {
        ...restaurant,
        pizzas: [...restaurant.pizzas, newPizza],
      },
      error: null,
      status: "resolved",
    });
  }

  if (status === "pending") return <h1>Loading...</h1>;
  if (status === "rejected") return <h1>Error: {error.error}</h1>;

  return (
    <section className="container">
      <div className="card">
        <div className="card-body">
        <h1 className="card-title text-success">{restaurant.name}</h1>
        <p className="card-text">{restaurant.address}</p>
        </div>
      </div>
      
      <div className="card p-3">
        <h3>Add New Pizza</h3>
        <PizzaForm restaurantId={restaurant.id} onAddPizza={handleAddPizza} />
      </div>
    </section>
  );
}

export default Home;
