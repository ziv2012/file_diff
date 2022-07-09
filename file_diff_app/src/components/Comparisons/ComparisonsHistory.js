import React, { useState, useEffect, useContext } from "react";
import { List, Typography } from "antd";
import "./ComparisonsHistory.css";
import TransContext from "../store/trans-context";
import "antd/dist/antd.css";

const ComparisonsHistory = () => {
  const [transactionsHistory, setTransactionsHistory] = useState([]);
  const transCtx = useContext(TransContext);

  useEffect(() => {
    fetch(process.env.REACT_APP_API_URL + "comp/all")
      .then((response) => {
        const json = response.json();
        if (response.ok) {
          return json;
        }
        throw response;
      })
      .then((data) => {
        var arr = data.map((trans, index) => {
          setTransactionsHistory((transactionsHistory) => [
            ...transactionsHistory,
            trans.transactions,
          ]);
          return index;
        });
        transCtx.onSetCompHistory(arr);
      })
      .catch((error) => {
        alert(error);
      });
  }, [transCtx.transactions]);

  return (
    <section id="history">
      <List
        dataSource={transCtx.compHistory}
        pagination={{ pageSize: 10 }}
        renderItem={(item) => (
          <List.Item>
            <Typography.Text mark>[COMPARISON ID]</Typography.Text>
            <a
              onClick={() =>
                transCtx.onsetTransactions(transactionsHistory[item])
              }
            >
              {item}
            </a>
          </List.Item>
        )}
      />
    </section>
  );
};

export default ComparisonsHistory;
