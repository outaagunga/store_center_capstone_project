import React, { useState, useEffect } from "react";

function TransactionList() {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    // Fetch transactions from the API and update the state
    // Example: fetch('/api/transactions').then(response => response.json()).then(data => setTransactions(data));
  }, []);

  return (
    <div>
      <h2>Transactions</h2>
      {/* Render the list of transactions */}
      {transactions.map((transaction) => (
        <div key={transaction.transaction_id}>
          {transaction.user_id} - {transaction.type} - {transaction.timestamp}
        </div>
      ))}
    </div>
  );
}

export default TransactionList;