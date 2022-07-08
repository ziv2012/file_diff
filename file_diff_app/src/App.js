import { InboxOutlined } from "@ant-design/icons";
import { message, Upload, Button, Table, List, Typography } from "antd";
import "antd/dist/antd.css";
import "./App.css";
import React, { useState, useEffect } from "react";
const { Dragger } = Upload;
const BASE_URL = "http://localhost:8000/";

const columns = [
  {
    title: "trans_id",
    dataIndex: "trans_id",
    key: "trans_id",
  },
  {
    title: "diff_type",
    dataIndex: "diff_type",
    key: "diff_type",
  },
  {
    title: "value_left",
    dataIndex: "value_left",
    key: "value_left",
  },
  {
    title: "value_right",
    dataIndex: "value_right",
    key: "value_right",
  },
];
const App = () => {
  const [files, setFiles] = useState([]);
  const [result, setResult] = useState([]);
  const [comparisonHistory, setComparisonHistory] = useState([]);
  const [transactionsHistory, seTransactionsHistory] = useState([]);
  const props = {
    name: "file",
    multiple: false,
    action: "https://www.mocky.io/v2/5cc8019d300000980a055e76",
    beforeUpload: (file) => {
      const isCSV = file.type === "text/csv";
      debugger;
      if (!isCSV) {
        message.error(`${file.name} is not a csv file`);
      } else if (files.length >= 2) {
        message.error(`can't upload another file - only 2 are allowed`);
        return false || Upload.LIST_IGNORE;
      } else {
        setFiles([...files, file]);
      }

      return isCSV || Upload.LIST_IGNORE;
    },
    onChange(info) {
      const { status } = info.file;

      if (status === "done") {
        message.success(`${info.file.name} file uploaded successfully.`);
      } else if (status === "error") {
        message.error(`${info.file.name} file upload failed.`);
      } else if (status === "removed") {
        removeFile(info.file.uid);
      }
    },
  };
  const removeFile = (uid) => {
    var array = files.filter(function (item) {
      return item.uid !== uid;
    });
    setFiles(array);
  };
  const onSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    files.forEach((file) => {
      formData.append("files", file);
    });
    const requestOptions = {
      method: "POST",
      body: formData,
    };
    await fetch(BASE_URL + "upload", requestOptions)
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw response;
      })
      .then((data) => {
        setResult(data);
      })
      .catch((error) => {
        console.log(error);
        alert(error);
      });
  };
  const loadComparison = (id) => {
    setResult(transactionsHistory[id]);
  };
  useEffect(() => {
    fetch(BASE_URL + "comp/all")
      .then((response) => {
        const json = response.json();
        if (response.ok) {
          return json;
        }
        throw response;
      })
      .then((data) => {
        data.map((anObjectMapped, index) => {
          setComparisonHistory((comparisonHistory) => [
            ...comparisonHistory,
            index,
          ]);
          seTransactionsHistory((transactionsHistory) => [
            ...transactionsHistory,
            anObjectMapped.transactions,
          ]);
        });
        //
      })
      .catch((error) => {
        console.log(error);
        alert(error);
      });
  }, []);
  return (
    <>
      <div className="main">
        <section id="history">
          {/* {comparisonHistory.map((comp) => (
            <div key={comp.id}>
              <label>{comp.date}</label>
            </div>
          ))} */}
          <List
            dataSource={comparisonHistory}
            pagination={{ pageSize: 10 }}
            renderItem={(item) => (
              <List.Item>
                <Typography.Text mark>[COMPARISON ID]</Typography.Text>
                <a onClick={() => loadComparison(item)}>{item}</a>
              </List.Item>
            )}
          />
        </section>
        <section id="table">
          {result.length > 0 && (
            <Table
              pagination={{ pageSize: 5 }}
              dataSource={result}
              columns={columns}
            />
          )}
          <div className="upload_sections">
            <Dragger {...props}>
              <p className="ant-upload-drag-icon">
                <InboxOutlined />
              </p>
              <p className="ant-upload-text">
                Click or drag file to this area to upload
              </p>
            </Dragger>

            <Dragger {...props}>
              <p className="ant-upload-drag-icon">
                <InboxOutlined />
              </p>
              <p className="ant-upload-text">
                Click or drag file to this area to upload
              </p>
            </Dragger>
          </div>
          <div className="button">
            <Button type="primary" onClick={onSubmit}>
              Process
            </Button>
          </div>
        </section>
      </div>
    </>
  );
};

export default App;
