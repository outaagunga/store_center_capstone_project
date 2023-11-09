import React from "react";
import TransactionList from "./TransactionList";
import DeliveryList from "./DeliveryList";
import PickupList from "./PickupList";
import ShippingList from "./ShippingList";
import InventoryList from "./InventoryList";

function App() {
  return (
    <div>
      <h1>Storage Management System</h1>
      <TransactionList />
      <DeliveryList />
      <PickupList />
      <ShippingList />
      <InventoryList />
    </div>
  );
}

export default App;