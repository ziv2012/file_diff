import React, { useState } from "react";
const TransContext = React.createContext({
  onsetTransactions: (result) => {},
  onSetCompHistory: (compHistory) => {},
});
export const TransContextProvider = (props) => {
  const [transactions, setTransactions] = useState([]);
  const [compHistory, setCompHistory] = useState([]);
  const setTransactionsHandler = (props) => {
    setTransactions(props);
  };
  const setCompHandler = (props) => {
    setCompHistory(props);
  };
  return (
    <TransContext.Provider
      value={{
        onsetTransactions: setTransactionsHandler,
        onSetCompHistory: setCompHandler,
        compHistory: compHistory,
        transactions: transactions,
      }}
    >
      {props.children}
    </TransContext.Provider>
  );
};

export default TransContext;
